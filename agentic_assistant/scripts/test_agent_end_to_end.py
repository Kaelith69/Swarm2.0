from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, cast

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from assistant.orchestrator import AgentOrchestrator  # noqa: E402


class FakeRag:
    def query(self, text: str, top_k: int = 3):
        if "doc" in text.lower() or "source" in text.lower():
            return [{"source": "kb", "chunk_index": 0, "content": "retrieved context"}]
        return []


class FakeLlama:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        if "Context:" in prompt:
            return "LOCAL_RAG_RESPONSE"
        return "LOCAL_SIMPLE_RESPONSE"


class FakeCloud:
    def __init__(self, fail_groq: bool = False, fail_gemini: bool = False, fail_kimi: bool = False) -> None:
        self.fail_groq = fail_groq
        self.fail_gemini = fail_gemini
        self.fail_kimi = fail_kimi

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


@dataclass
class CaseResult:
    name: str
    route: str
    reason: str
    response: str
    ok: bool


def run() -> tuple[bool, list[CaseResult]]:
    rag = FakeRag()
    llm = FakeLlama()
    cloud = FakeCloud()
    orchestrator = AgentOrchestrator(
        rag=cast(Any, rag),
        llm=cast(Any, llm),
        cloud=cast(Any, cloud),
        top_k=3,
        long_context_threshold_chars=120,
    )

    cases = [
        ("simple", "hello there", "local_simple", "default_simple", "LOCAL_SIMPLE_RESPONSE"),
        ("rag", "based on source docs, explain this", "local_rag", "rag_keywords", "LOCAL_RAG_RESPONSE"),
        ("complex", "analyze tradeoff between A and B", "groq", "complex_reasoning_keywords", "GROQ_RESPONSE"),
        ("long_context", "x" * 130, "gemini", "long_context_threshold", "GEMINI_RESPONSE"),
        ("planning", "create a roadmap plan for rollout", "kimi", "planning_keywords", "KIMI_RESPONSE"),
    ]

    results: list[CaseResult] = []
    all_ok = True

    for name, message, exp_route, exp_reason, exp_resp in cases:
        out = orchestrator.respond_with_route(message)
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

    fallback_orchestrator = AgentOrchestrator(
        rag=cast(Any, rag),
        llm=cast(Any, llm),
        cloud=cast(Any, FakeCloud(fail_groq=True)),
        top_k=3,
        long_context_threshold_chars=120,
    )
    fallback = fallback_orchestrator.respond_with_route("analyze this deeply")
    fallback_ok = fallback.route == "local_fallback" and fallback.reason == "groq_unavailable"
    all_ok = all_ok and fallback_ok
    results.append(
        CaseResult(
            name="fallback_groq",
            route=fallback.route,
            reason=fallback.reason,
            response=fallback.response,
            ok=fallback_ok,
        )
    )

    return all_ok, results


def main() -> int:
    ok, results = run()
    print(
        json.dumps(
            {
                "ok": ok,
                "results": [asdict(item) for item in results],
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
