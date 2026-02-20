"""AgentOrchestrator — routes every incoming message to the right backend.

Routing priority (highest → lowest):
  1. Very short messages  → local model (no routing overhead)
  2. Keyword fast-path    → well-known signal words route immediately
  3. Local LLM classifier → Gemma decides the best backend for ambiguous queries
  4. Default              → local simple

RAG context is fetched and injected into *every* backend prompt, so cloud
models also benefit from the stored knowledge base.

Conversation memory (per user_id) is prepended to prompts and updated
after every turn.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from assistant.llm.cloud_router import CloudRouter
from assistant.llm.llama_cpp_runner import LlamaCppRunner
from assistant.memory import ConversationMemory
from assistant.personality import Personality
from assistant.rag.store import RagStore

logger = logging.getLogger(__name__)

# Routing labels returned by the LLM classifier
_ROUTE_LOCAL = "LOCAL"
_ROUTE_GROQ = "GROQ"
_ROUTE_GEMINI = "GEMINI"
_ROUTE_KIMI = "KIMI"
_VALID_LLM_ROUTES = {_ROUTE_LOCAL, _ROUTE_GROQ, _ROUTE_GEMINI, _ROUTE_KIMI}

# Gemma instruction-tuned token format
_GEMMA_CLS_PROMPT = """\
<start_of_turn>user
Classify this request. Reply with exactly one word.

Categories:
- LOCAL  : short chat, simple question, quick fact
- GROQ   : analysis, comparison, step-by-step reasoning, deep explanation
- GEMINI : long text summary, large document processing
- KIMI   : planning, roadmap, strategy, workflow, project steps

Request: {message}
<end_of_turn>
<start_of_turn>model
"""


@dataclass(frozen=True)
class RouteResult:
    route: str
    reason: str
    response: str


class AgentOrchestrator:
    def __init__(
        self,
        rag: RagStore,
        llm: LlamaCppRunner,
        cloud: CloudRouter,
        memory: ConversationMemory | None = None,
        personality: Personality | None = None,
        top_k: int = 3,
        long_context_threshold_chars: int = 1200,
        short_message_threshold_chars: int = 150,
        use_llm_routing: bool = True,
    ) -> None:
        self.rag = rag
        self.llm = llm
        self.cloud = cloud
        self.memory = memory
        self.personality = personality
        self.top_k = top_k
        self.long_context_threshold_chars = long_context_threshold_chars
        self.short_message_threshold_chars = short_message_threshold_chars
        self.use_llm_routing = use_llm_routing

    # ------------------------------------------------------------------
    # RAG helpers
    # ------------------------------------------------------------------

    def _rag_context(self, message: str) -> str:
        """Retrieve relevant chunks and format as a context block."""
        chunks = self.rag.query(message, top_k=self.top_k)
        if not chunks:
            return ""
        lines = [
            f"[{item['source']} chunk#{item['chunk_index']}]\n{item['content']}"
            for item in chunks
        ]
        return "\n\n".join(lines)

    # ------------------------------------------------------------------
    # Memory helpers
    # ------------------------------------------------------------------

    def _history_block(self, user_id: str) -> str:
        if self.memory is None or not user_id:
            return ""
        return self.memory.format_for_prompt(user_id)

    def _record(self, user_id: str, message: str, response: str) -> None:
        if self.memory is None or not user_id:
            return
        self.memory.add_turn(user_id, "user", message)
        self.memory.add_turn(user_id, "assistant", response)

    # ------------------------------------------------------------------
    # Prompt builders
    # ------------------------------------------------------------------

    def _local_prompt(self, message: str, rag_ctx: str, history: str) -> str:
        """Build a Gemma-format prompt for the local model."""
        if self.personality:
            system_text = self.personality.system_prompt(is_local=True)
        else:
            system_text = (
                "You are a concise, helpful assistant. "
                "Use the context and conversation history when relevant. Be brief."
            )
        parts: list[str] = [
            "<start_of_turn>system",
            system_text,
            "<end_of_turn>",
        ]
        if history:
            parts += ["<start_of_turn>context", history, "<end_of_turn>"]
        if rag_ctx:
            parts += ["<start_of_turn>context", "Retrieved knowledge:\n" + rag_ctx, "<end_of_turn>"]
        parts += [
            "<start_of_turn>user",
            message,
            "<end_of_turn>",
            "<start_of_turn>model",
        ]
        return "\n".join(parts)

    def _cloud_prompt(self, message: str, rag_ctx: str, history: str) -> str:
        """Build a plain-text prompt suitable for all cloud models."""
        sections: list[str] = []
        if self.personality:
            sections.append(self.personality.system_prompt(is_local=False))
        else:
            sections.append(
                "You are a helpful assistant. Use the provided context and history when relevant."
            )
        if history:
            sections.append(history)
        if rag_ctx:
            sections.append("=== Retrieved Knowledge ===\n" + rag_ctx)
        sections.append(f"User: {message}\nAssistant:")
        return "\n\n".join(sections)

    # ------------------------------------------------------------------
    # Keyword fast-path classifiers
    # ------------------------------------------------------------------

    def _has_rag_signal(self, msg: str) -> bool:
        # Deliberately narrower than the original: excludes over-broad words like
        # "context" (matches any conversational "in this context…") and "based on"
        # (matches reasoning queries).  "docs" / "document" are kept because they
        # unambiguously signal retrieval intent.
        tokens = (
            "docs", "document", "documentation",
            "from file", "knowledge base", "retrieve", "retrieval",
            "look up", "find in", "according to the",
            "from the knowledge", "cite the source",
        )
        lower = msg.lower()
        return any(t in lower for t in tokens)

    def _has_planning_signal(self, msg: str) -> bool:
        tokens = ("plan", "roadmap", "strategy", "orchestrate", "workflow", "project steps")
        lower = msg.lower()
        return any(t in lower for t in tokens)

    def _has_reasoning_signal(self, msg: str) -> bool:
        tokens = (
            "analyze", "analyse", "compare", "tradeoff", "reason", "justify",
            "deep dive", "pros and cons", "step by step", "root cause", "explain in detail",
        )
        lower = msg.lower()
        return any(t in lower for t in tokens)

    # ------------------------------------------------------------------
    # Local LLM routing classifier
    # ------------------------------------------------------------------

    def _classify_with_local_llm(self, message: str) -> str | None:
        """Ask the local Gemma model to classify the routing target.

        Returns one of LOCAL / GROQ / GEMINI / KIMI, or None on failure.
        """
        prompt = _GEMMA_CLS_PROMPT.format(message=message[:500])
        try:
            raw = self.llm.classify(prompt).upper()
        except Exception as exc:  # noqa: BLE001
            logger.warning("LLM routing classification failed: %s", exc)
            return None

        # The model may prefix with whitespace or include punctuation.
        for token in raw.split():
            candidate = token.strip(".,!?:")
            if candidate in _VALID_LLM_ROUTES:
                return candidate
        return None

    # ------------------------------------------------------------------
    # Private response dispatchers
    # ------------------------------------------------------------------

    def _local_simple(self, message: str, rag_ctx: str, history: str) -> str:
        return self.llm.generate(self._local_prompt(message, rag_ctx, history)).strip()

    def _safe_cloud_fallback(self, message: str, rag_ctx: str, history: str) -> RouteResult:
        """Last-resort fallback: generate locally."""
        response = self._local_simple(message, rag_ctx, history)
        return RouteResult(route="local_fallback", reason="cloud_unavailable", response=response)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def respond_with_route(self, message: str, user_id: str = "") -> RouteResult:
        """Route *message* to the best backend and return a RouteResult.

        Args:
            message: The cleaned user input.
            user_id: Optional stable identifier for conversation memory
                     (telegram user id, discord user id, …).
        """
        rag_ctx = self._rag_context(message)
        history = self._history_block(user_id)
        cloud_prompt = self._cloud_prompt(message, rag_ctx, history)

        result = self._route(message, rag_ctx, history, cloud_prompt)
        self._record(user_id, message, result.response)
        return result

    def _route(
        self,
        message: str,
        rag_ctx: str,
        history: str,
        cloud_prompt: str,
    ) -> RouteResult:
        # ── 1. Short-message fast path → local, no LLM routing overhead ─────
        if len(message) <= self.short_message_threshold_chars and not self._has_reasoning_signal(message) and not self._has_planning_signal(message):
            response = self._local_simple(message, rag_ctx, history)
            return RouteResult(route="local_simple", reason="short_message", response=response)

        # ── 2. Keyword fast path ─────────────────────────────────────────────
        if self._has_planning_signal(message):
            target = _ROUTE_KIMI
            reason = "kw_planning"
        elif len(message) >= self.long_context_threshold_chars:
            target = _ROUTE_GEMINI
            reason = "kw_long_context"
        elif self._has_reasoning_signal(message):
            target = _ROUTE_GROQ
            reason = "kw_reasoning"
        elif self._has_rag_signal(message):
            # RAG queries stay local — no need for expensive cloud call
            response = self._local_simple(message, rag_ctx, history)
            return RouteResult(route="local_rag", reason="kw_rag", response=response)
        else:
            target = None
            reason = ""

        # ── 3. LLM classifier for ambiguous messages ─────────────────────────
        if target is None and self.use_llm_routing:
            llm_route = self._classify_with_local_llm(message)
            if llm_route and llm_route != _ROUTE_LOCAL:
                target = llm_route
                reason = "llm_classifier"
            else:
                # LLM said LOCAL or classification failed
                response = self._local_simple(message, rag_ctx, history)
                return RouteResult(route="local_simple", reason="llm_classifier_local", response=response)

        if target is None:
            # No signal found → default local
            response = self._local_simple(message, rag_ctx, history)
            return RouteResult(route="local_simple", reason="default", response=response)

        # ── 4. Dispatch to cloud ─────────────────────────────────────────────
        if target == _ROUTE_GROQ:
            try:
                if not self.cloud.is_groq_available():
                    raise RuntimeError("GROQ_API_KEY not configured")
                return RouteResult(
                    route="groq",
                    reason=reason,
                    response=self.cloud.groq_generate(cloud_prompt),
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("Groq route failed (%s), falling back to local", exc)
                return RouteResult(
                    route="local_fallback",
                    reason="groq_unavailable",
                    response=self._local_simple(message, rag_ctx, history),
                )

        if target == _ROUTE_GEMINI:
            try:
                if not self.cloud.is_gemini_available():
                    raise RuntimeError("GEMINI_API_KEY not configured")
                return RouteResult(
                    route="gemini",
                    reason=reason,
                    response=self.cloud.gemini_generate(cloud_prompt),
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("Gemini route failed (%s), falling back to local", exc)
                return RouteResult(
                    route="local_fallback",
                    reason="gemini_unavailable",
                    response=self._local_simple(message, rag_ctx, history),
                )

        if target == _ROUTE_KIMI:
            try:
                if not self.cloud.is_kimi_available():
                    raise RuntimeError("KIMI_API_KEY not configured")
                return RouteResult(
                    route="kimi",
                    reason=reason,
                    response=self.cloud.kimi_generate(cloud_prompt),
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("Kimi route failed (%s), falling back to local", exc)
                return RouteResult(
                    route="local_fallback",
                    reason="kimi_unavailable",
                    response=self._local_simple(message, rag_ctx, history),
                )

        # Fallthrough (should not be reached)
        response = self._local_simple(message, rag_ctx, history)
        return RouteResult(route="local_simple", reason="unmatched_target", response=response)

    # ------------------------------------------------------------------
    # Convenience alias
    # ------------------------------------------------------------------

    def respond(self, message: str, user_id: str = "") -> str:
        return self.respond_with_route(message, user_id).response

