from __future__ import annotations

from dataclasses import dataclass

from assistant.llm.cloud_router import CloudRouter
from assistant.llm.llama_cpp_runner import LlamaCppRunner
from assistant.rag.store import RagStore


@dataclass(frozen=True)
class RouteResult:
    route: str
    response: str


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

    def _is_rag_query(self, message: str) -> bool:
        tokens = ("doc", "document", "source", "knowledge", "from file", "based on")
        lowered = message.lower()
        return any(token in lowered for token in tokens)

    def _is_planning_query(self, message: str) -> bool:
        tokens = ("plan", "roadmap", "strategy", "orchestrate", "workflow")
        lowered = message.lower()
        return any(token in lowered for token in tokens)

    def _is_complex_reasoning_query(self, message: str) -> bool:
        tokens = ("analyze", "compare", "tradeoff", "reason", "justify", "deep")
        lowered = message.lower()
        return any(token in lowered for token in tokens)

    def _is_long_context_query(self, message: str) -> bool:
        return len(message) >= self.long_context_threshold_chars

    def _prompt(self, message: str) -> str:
        context_chunks = self.rag.query(message, top_k=self.top_k)
        if context_chunks:
            context = "\n\n".join(
                f"[{item['source']} #{item['chunk_index']}] {item['content']}"
                for item in context_chunks
            )
        else:
            context = "No retrieved context available."

        return (
            "You are a concise assistant running locally on Raspberry Pi. "
            "Answer using the provided context when useful.\n\n"
            f"Context:\n{context}\n\n"
            f"User: {message}\n"
            "Assistant:"
        )

    def _local_simple(self, message: str) -> str:
        return self.llm.generate(f"User: {message}\nAssistant:").strip()

    def _local_rag(self, message: str) -> str:
        return self.llm.generate(self._prompt(message)).strip()

    def respond_with_route(self, message: str) -> RouteResult:
        if self._is_planning_query(message):
            try:
                return RouteResult(route="kimi", response=self.cloud.kimi_generate(message))
            except Exception:
                return RouteResult(route="local_fallback", response=self._local_rag(message))

        if self._is_long_context_query(message):
            try:
                return RouteResult(route="gemini", response=self.cloud.gemini_generate(message))
            except Exception:
                return RouteResult(route="local_fallback", response=self._local_rag(message))

        if self._is_complex_reasoning_query(message):
            try:
                return RouteResult(route="groq", response=self.cloud.groq_generate(message))
            except Exception:
                return RouteResult(route="local_fallback", response=self._local_rag(message))

        if self._is_rag_query(message):
            return RouteResult(route="local_rag", response=self._local_rag(message))

        return RouteResult(route="local_simple", response=self._local_simple(message))

    def respond(self, message: str) -> str:
        return self.respond_with_route(message).response
