from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, cast

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.assistant.orchestrator import AgentOrchestrator  # noqa: E402


class FakeRag:
    def query(self, text: str, top_k: int = 3):
        if "doc" in text.lower() or "source" in text.lower():
            return [{"source": "kb", "chunk_index": 0, "content": "retrieved context"}]
        return []


class FakeLlama:
    """Local LLM stub. Returns a routing label (groq/gemini/kimi) for routing prompts."""

    def __init__(self, routing_response: str = "groq", fail: bool = False) -> None:
        self.calls: list[str] = []
        self.routing_response = routing_response
        self.fail = fail

    def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        if self.fail:
            raise RuntimeError("llama not available")
        return self.routing_response


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


def _make_orchestrator(
    llm_response: str = "groq",
    llm_fail: bool = False,
    fail_groq: bool = False,
    fail_gemini: bool = False,
    fail_kimi: bool = False,
    threshold: int = 120,
) -> AgentOrchestrator:
    return AgentOrchestrator(
        rag=cast(Any, FakeRag()),
        llm=cast(Any, FakeLlama(routing_response=llm_response, fail=llm_fail)),
        cloud=cast(Any, FakeCloud(fail_groq=fail_groq, fail_gemini=fail_gemini, fail_kimi=fail_kimi)),
        top_k=3,
        long_context_threshold_chars=threshold,
    )


def run() -> tuple[bool, list[CaseResult]]:
    results: list[CaseResult] = []
    all_ok = True

    def check(name: str, out: Any, exp_route: str, exp_reason: str, exp_resp: str) -> None:
        nonlocal all_ok
        ok = out.route == exp_route and out.reason == exp_reason and out.response == exp_resp
        all_ok = all_ok and ok
        results.append(CaseResult(name=name, route=out.route, reason=out.reason, response=out.response, ok=ok))

    # Local LLM returns "groq" → GROQ_RESPONSE via cloud
    check(
        "llm_routes_groq",
        _make_orchestrator(llm_response="groq").respond_with_route("hello there"),
        "groq", "local_llm_routing", "GROQ_RESPONSE",
    )

    # Local LLM returns "gemini" → GEMINI_RESPONSE via cloud
    check(
        "llm_routes_gemini",
        _make_orchestrator(llm_response="gemini").respond_with_route("summarise this long article"),
        "gemini", "local_llm_routing", "GEMINI_RESPONSE",
    )

    # Local LLM returns "kimi" → KIMI_RESPONSE via cloud
    check(
        "llm_routes_kimi",
        _make_orchestrator(llm_response="kimi").respond_with_route("create a roadmap plan for rollout"),
        "kimi", "local_llm_routing", "KIMI_RESPONSE",
    )

    # Local LLM unavailable → keyword fallback: "plan" keyword → kimi
    check(
        "llm_unavailable_keyword_kimi",
        _make_orchestrator(llm_fail=True).respond_with_route("build a plan for the project"),
        "kimi", "keyword_fallback_routing", "KIMI_RESPONSE",
    )

    # Local LLM unavailable → keyword fallback: long message → gemini
    check(
        "llm_unavailable_keyword_gemini",
        _make_orchestrator(llm_fail=True, threshold=10).respond_with_route("x" * 20),
        "gemini", "keyword_fallback_routing", "GEMINI_RESPONSE",
    )

    # Local LLM unavailable → keyword fallback: default → groq
    check(
        "llm_unavailable_keyword_groq",
        _make_orchestrator(llm_fail=True).respond_with_route("hello"),
        "groq", "keyword_fallback_routing", "GROQ_RESPONSE",
    )

    # Cloud API failure → automatic fallback to next available API
    out = _make_orchestrator(llm_response="groq", fail_groq=True).respond_with_route("hello")
    ok = out.route in ("gemini", "kimi") and out.reason.startswith("fallback_from_groq")
    all_ok = all_ok and ok
    results.append(CaseResult(name="cloud_fallback_groq_fails", route=out.route, reason=out.reason, response=out.response, ok=ok))

    # All cloud APIs fail → error result
    check(
        "all_cloud_fail",
        _make_orchestrator(fail_groq=True, fail_gemini=True, fail_kimi=True).respond_with_route("hello"),
        "error", "all_cloud_apis_unavailable",
        "I'm sorry, I couldn't process your request at this time. All cloud AI services are currently unavailable.",
    )

    # RAG context is prepended to the cloud prompt (rag FakeRag returns chunks for "source")
    orch = _make_orchestrator(llm_response="groq")
    out = orch.respond_with_route("based on source docs, what is X?")
    ok = out.route == "groq" and out.response == "GROQ_RESPONSE"
    all_ok = all_ok and ok
    results.append(CaseResult(name="rag_enrichment_to_cloud", route=out.route, reason=out.reason, response=out.response, ok=ok))

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
