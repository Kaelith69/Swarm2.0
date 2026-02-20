from __future__ import annotations

import logging
from dataclasses import dataclass

from assistant.llm.cloud_router import CloudRouter
from assistant.llm.llama_cpp_runner import LlamaCppRunner
from assistant.rag.store import RagStore

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RouteResult:
    route: str
    reason: str
    response: str


# Maximum characters of the user message forwarded to the local LLM for routing.
_MAX_ROUTING_MESSAGE_CHARS = 500

# Prompt sent to the local LLM to decide which cloud API should answer.
_ROUTE_PROMPT = (
    "You are a routing assistant. Your only job is to decide which AI API to use "
    "for the following user message. Reply with EXACTLY one word from this list: "
    "groq, gemini, kimi. No punctuation, no explanation.\n\n"
    "Guidelines:\n"
    "- groq: general questions, reasoning, analysis, step-by-step explanations\n"
    "- gemini: long documents, large context, summaries of lengthy content\n"
    "- kimi: planning, roadmaps, strategies, workflows, project organisation\n\n"
    "User message: {message}\n"
    "Route:"
)

_VALID_ROUTES = frozenset({"groq", "gemini", "kimi"})
_ALL_ROUTES = ("groq", "gemini", "kimi")


class AgentOrchestrator:
    def __init__(
        self,
        rag: RagStore,
        llm: LlamaCppRunner,
        cloud: CloudRouter,
        top_k: int = 3,
        long_context_threshold_chars: int = 1200,
    ) -> None:
        self.rag = rag
        self.llm = llm
        self.cloud = cloud
        self.top_k = top_k
        self.long_context_threshold_chars = long_context_threshold_chars

    # ------------------------------------------------------------------
    # Routing: local LLM decides which cloud API to call
    # ------------------------------------------------------------------

    def _decide_route(self, message: str) -> tuple[str, str]:
        """Ask the local LLM to choose a cloud API.

        Returns (route, reason) where route is 'groq', 'gemini', or 'kimi'.
        Falls back to keyword-based routing when the local LLM is unavailable.
        """
        try:
            prompt = _ROUTE_PROMPT.format(message=message[:_MAX_ROUTING_MESSAGE_CHARS])
            raw = self.llm.generate(prompt).strip().lower()
            first_word = raw.split()[0] if raw.split() else ""
            if first_word in _VALID_ROUTES:
                return first_word, "local_llm_routing"
        except Exception as exc:
            logger.warning("Local LLM routing failed, using keyword fallback: %s", exc)
        return self._keyword_route(message), "keyword_fallback_routing"

    def _keyword_route(self, message: str) -> str:
        """Keyword-based routing used when the local LLM is unavailable."""
        lowered = message.lower()
        if any(t in lowered for t in ("plan", "roadmap", "strategy", "orchestrate", "workflow")):
            return "kimi"
        if len(message) >= self.long_context_threshold_chars:
            return "gemini"
        return "groq"

    # ------------------------------------------------------------------
    # RAG context enrichment
    # ------------------------------------------------------------------

    def _enrich_with_rag(self, message: str) -> str:
        """Prepend relevant RAG context chunks to the message for the cloud API."""
        context_chunks = self.rag.query(message, top_k=self.top_k)
        if not context_chunks:
            return message
        context = "\n\n".join(
            f"[{item['source']} #{item['chunk_index']}] {item['content']}"
            for item in context_chunks
        )
        return (
            "Answer using the following context when useful.\n\n"
            f"Context:\n{context}\n\n"
            f"User: {message}"
        )

    # ------------------------------------------------------------------
    # Cloud API dispatch
    # ------------------------------------------------------------------

    def _call_cloud(self, route: str, prompt: str) -> str:
        if route == "gemini":
            return self.cloud.gemini_generate(prompt)
        if route == "kimi":
            return self.cloud.kimi_generate(prompt)
        return self.cloud.groq_generate(prompt)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def respond_with_route(self, message: str) -> RouteResult:
        """Route via local LLM, call the chosen cloud API, send back the response."""
        route, reason = self._decide_route(message)

        # Enrich the user message with any relevant RAG context.
        prompt = self._enrich_with_rag(message)

        # Try the chosen API first, then fall back to the remaining ones.
        fallback_order = [r for r in _ALL_ROUTES if r != route]
        for candidate in [route] + fallback_order:
            try:
                response = self._call_cloud(candidate, prompt)
                if candidate != route:
                    reason = f"fallback_from_{route}"
                    route = candidate
                return RouteResult(route=route, reason=reason, response=response)
            except Exception as exc:
                logger.warning("Cloud API '%s' failed: %s", candidate, exc)
                continue

        return RouteResult(
            route="error",
            reason="all_cloud_apis_unavailable",
            response=(
                "I'm sorry, I couldn't process your request at this time. "
                "All cloud AI services are currently unavailable."
            ),
        )

    def respond(self, message: str) -> str:
        return self.respond_with_route(message).response
