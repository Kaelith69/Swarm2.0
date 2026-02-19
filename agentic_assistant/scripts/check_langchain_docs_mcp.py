from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Iterable

LLMS_INDEX_URL = "https://docs.langchain.com/llms.txt"
MCP_URL = "https://docs.langchain.com/mcp"

CRITICAL_PAGES = [
    "https://docs.langchain.com/oss/python/langchain/overview.md",
    "https://docs.langchain.com/oss/python/langchain/quickstart.md",
    "https://docs.langchain.com/oss/python/langchain/retrieval.md",
    "https://docs.langchain.com/oss/python/integrations/providers/groq.md",
    "https://docs.langchain.com/oss/python/langchain/mcp.md",
]


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def _http_get(url: str, timeout: int = 20) -> tuple[int, str]:
    req = urllib.request.Request(url=url, method="GET", headers={"User-Agent": "agentic-assistant-doc-check/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        status = int(response.getcode() or 0)
        body = response.read().decode("utf-8", errors="replace")
    return status, body


def _reachable(url: str, acceptable_statuses: Iterable[int] | None = None, timeout: int = 20) -> tuple[bool, str]:
    statuses = set(acceptable_statuses or {200})
    req = urllib.request.Request(url=url, method="GET", headers={"User-Agent": "agentic-assistant-doc-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = int(response.getcode() or 0)
            if status in statuses:
                return True, f"HTTP {status}"
            return False, f"HTTP {status} (unexpected)"
    except urllib.error.HTTPError as exc:
        status = int(exc.code)
        if status in statuses:
            return True, f"HTTP {status}"
        return False, f"HTTP {status}"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def _extract_urls(markdown_text: str) -> set[str]:
    links = re.findall(r"\((https?://[^)\s]+)\)", markdown_text)
    return set(links)


def run_checks() -> tuple[bool, list[CheckResult], dict]:
    results: list[CheckResult] = []
    metadata: dict = {}

    try:
        status, body = _http_get(LLMS_INDEX_URL)
        ok = status == 200 and len(body) > 0
        results.append(CheckResult("llms_index_fetch", ok, f"HTTP {status}, bytes={len(body)}"))
        if not ok:
            return False, results, metadata
    except Exception as exc:  # noqa: BLE001
        results.append(CheckResult("llms_index_fetch", False, f"{type(exc).__name__}: {exc}"))
        return False, results, metadata

    index_urls = _extract_urls(body)
    metadata["index_url_count"] = len(index_urls)

    missing = [url for url in CRITICAL_PAGES if url not in index_urls]
    if missing:
        results.append(CheckResult("critical_pages_in_index", False, f"missing={missing}"))
    else:
        results.append(CheckResult("critical_pages_in_index", True, f"all {len(CRITICAL_PAGES)} found"))

    mcp_ok, mcp_detail = _reachable(MCP_URL, acceptable_statuses={200, 400, 401, 404, 405})
    results.append(CheckResult("mcp_endpoint_reachable", mcp_ok, mcp_detail))

    for url in CRITICAL_PAGES:
        ok, detail = _reachable(url, acceptable_statuses={200})
        results.append(CheckResult(f"page_reachable:{url}", ok, detail))

    success = all(item.ok for item in results)
    return success, results, metadata


def main() -> int:
    success, checks, metadata = run_checks()
    output = {
        "ok": success,
        "metadata": metadata,
        "checks": [{"name": c.name, "ok": c.ok, "detail": c.detail} for c in checks],
    }
    print(json.dumps(output, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
