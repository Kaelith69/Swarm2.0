"""End-to-end routing unit tests.

Runs entirely offline using stub implementations of RagStore,
LlamaCppRunner, and CloudRouter.  No real model or API key required.
"""
from __future__ import annotations

import json
import sys
import unittest.mock
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, cast

# Support both `python scripts/test_agent_end_to_end.py` (from project root)
# and `PYTHONPATH=src python scripts/test_agent_end_to_end.py`
_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
for _p in (_SRC, _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

# ---------------------------------------------------------------------------
# Mock heavy optional dependencies before importing any assistant code so the
# test runs without the full ML stack (sentence-transformers, hnswlib, etc.).
# ---------------------------------------------------------------------------
for _mod in (
    "sentence_transformers",
    "hnswlib",
    "numpy",
    "groq",
    "openai",
    "google",
    "google.generativeai",
):
    if _mod not in sys.modules:
        sys.modules[_mod] = unittest.mock.MagicMock()  # type: ignore[assignment]

from assistant.orchestrator import AgentOrchestrator  # noqa: E402


# ---------------------------------------------------------------------------
# Stubs
# ---------------------------------------------------------------------------

class FakeRag:
    """Returns a result only for messages that contain 'doc' or 'source'."""

    def query(self, text: str, top_k: int = 3) -> list[dict]:
        if "doc" in text.lower() or "source" in text.lower():
            return [{"source": "kb", "chunk_index": 0, "content": "retrieved context"}]
        return []


class FakeLlama:
    """Mimics LlamaCppRunner without spawning a subprocess."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def generate(self, prompt: str, max_tokens_override: int | None = None) -> str:
        self.calls.append(prompt)
        # New prompt format uses 'Retrieved knowledge:' for RAG context
        if "Retrieved knowledge:" in prompt:
            return "LOCAL_RAG_RESPONSE"
        return "LOCAL_SIMPLE_RESPONSE"

    def classify(self, prompt: str) -> str:
        """Always returns LOCAL (tests use use_llm_routing=False anyway)."""
        return "LOCAL"


class FakeCloud:
    """Mimics CloudRouter, with optional failure injection per provider."""

    def __init__(
        self,
        fail_groq: bool = False,
        fail_gemini: bool = False,
        fail_kimi: bool = False,
    ) -> None:
        self.fail_groq = fail_groq
        self.fail_gemini = fail_gemini
        self.fail_kimi = fail_kimi

    def is_groq_available(self) -> bool:
        return True

    def is_gemini_available(self) -> bool:
        return True

    def is_kimi_available(self) -> bool:
        return True

    def groq_generate(self, prompt: str) -> str:
        if self.fail_groq:
            raise RuntimeError("groq fail")
        return "GROQ_RESPONSE"

    def gemini_generate(self, prompt: str) -> str:
        if self.fail_gemini:
            raise RuntimeError("gemini fail")
        return "GEMINI_RESPONSE"

    def kimi_generate(self, prompt: str) -> str:
        if self.fail_kimi:
            raise RuntimeError("kimi fail")
        return "KIMI_RESPONSE"


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------

@dataclass
class CaseResult:
    name: str
    route: str
    reason: str
    response: str
    ok: bool


def _make_orchestrator(cloud: Any, *, fail_routing_llm: bool = False) -> AgentOrchestrator:
    """Build an orchestrator tuned for deterministic keyword-only tests."""
    return AgentOrchestrator(
        rag=cast(Any, FakeRag()),
        llm=cast(Any, FakeLlama()),
        cloud=cloud,
        memory=None,
        top_k=3,
        long_context_threshold_chars=120,
        short_message_threshold_chars=10,   # only messages ≤ 10 chars are "short"
        use_llm_routing=False,              # pure keyword routing for determinism
    )


def run() -> tuple[bool, list[CaseResult]]:
    cloud = cast(Any, FakeCloud())
    orchestrator = _make_orchestrator(cloud)

    # (name, message, expected_route, expected_reason, expected_response)
    cases = [
        (
            "short_message",
            "hi",                                        # 2 chars ≤ 10 → local
            "local_simple", "short_message",
            "LOCAL_SIMPLE_RESPONSE",
        ),
        (
            "rag",
            "based on source docs, explain this",        # rag keyword
            "local_rag", "kw_rag",
            "LOCAL_RAG_RESPONSE",
        ),
        (
            "complex_reasoning",
            "analyze tradeoff between A and B",          # reasoning keyword
            "groq", "kw_reasoning",
            "GROQ_RESPONSE",
        ),
        (
            "long_context",
            "x" * 130,                                   # 130 >= 120 threshold
            "gemini", "kw_long_context",
            "GEMINI_RESPONSE",
        ),
        (
            "planning",
            "create a roadmap plan for our rollout",     # planning keyword
            "kimi", "kw_planning",
            "KIMI_RESPONSE",
        ),
    ]

    results: list[CaseResult] = []
    all_ok = True

    for name, message, exp_route, exp_reason, exp_resp in cases:
        out = orchestrator.respond_with_route(message, user_id="test")
        ok = out.route == exp_route and out.reason == exp_reason and out.response == exp_resp
        all_ok = all_ok and ok
        results.append(
            CaseResult(
                name=name,
                route=out.route,
                reason=out.reason,
                response=out.response,
                ok=ok,
            )
        )

    # Fallback test: groq fails → should fall back to local
    fallback_orch = _make_orchestrator(cast(Any, FakeCloud(fail_groq=True)))
    fb = fallback_orch.respond_with_route("analyze this deeply", user_id="test")
    fb_ok = fb.route == "local_fallback" and fb.reason == "groq_unavailable"
    all_ok = all_ok and fb_ok
    results.append(
        CaseResult(
            name="fallback_groq",
            route=fb.route,
            reason=fb.reason,
            response=fb.response,
            ok=fb_ok,
        )
    )

    return all_ok, results


def main() -> int:
    ok, results = run()
    print(
        json.dumps(
            {"ok": ok, "results": [asdict(item) for item in results]},
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

