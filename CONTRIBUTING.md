# Contributing to Swarm 2.0

Welcome, brave soul. You've decided to contribute to a hybrid AI assistant that runs on a $80 single-board computer and somehow handles multi-platform bot routing with local RAG. Respect.

This document is your map. It covers the developer workflow, code conventions, and how to submit changes without causing a distributed incident.

---

## Ground Rules

1. **Be kind.** We're all here because we like building things, not because we enjoy arguing in GitHub comments.
2. **Be specific.** "It broke" is not a bug report. "It broke when I sent a 1400-character message in Tier 2 with `USE_LLM_ROUTING=false`" is a bug report.
3. **Keep it small.** PRs that change 40 files are PRs that never get merged. One concern per PR, always.
4. **Don't commit `.env`.** Seriously. We will haunt you.

---

## Development Environment Setup

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/Swarm2.0.git
cd Swarm2.0/agentic_assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure your environment

```bash
cp .env.example .env
# Edit .env — add your model path at minimum. Cloud keys are optional.
chmod 600 .env
```

### 4. Set PYTHONPATH

```bash
export PYTHONPATH=$(pwd)/src   # Windows: $env:PYTHONPATH = "$(pwd)\src"
```

### 5. Verify the server starts

```bash
python -m assistant.agent &
sleep 5
curl http://127.0.0.1:8000/health
kill %1
```

If you see `{"status":"ok"}`, you're in business. If you see a traceback, welcome to the club — check the [Troubleshooting wiki](wiki/Troubleshooting.md).

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| New feature | `feat/<short-description>` | `feat/streaming-responses` |
| Bug fix | `fix/<issue-or-description>` | `fix/tier2-keyword-matching` |
| Documentation | `docs/<topic>` | `docs/rag-ingestion-guide` |
| Refactor | `refactor/<scope>` | `refactor/cloud-router-cleanup` |

---

## Code Style

- Follow **PEP 8**. We're not monsters.
- Use **type annotations** on every function signature — Pyright is configured in `pyproject.toml`.
- Keep functions focused. If your function needs a table of contents, split it.
- Use `logging` — not `print`. Nobody wants your debug output in prod.
- No secrets in source code. All configuration lives in `.env`.

### Type checking

```bash
pip install pyright
pyright src/
```

Pyright should exit cleanly. If it doesn't, fix it before opening a PR or explain why the violation is acceptable in your PR description.

---

## Architectural Rules (Read These Before Touching Anything)

| Rule | Why |
|------|-----|
| **Single Uvicorn worker only** | SQLite is not safe across multiple processes. Do not add `--workers N` or any multiprocessing. |
| **No multi-threaded SQLite writes** | One writer at a time. Memory and RAG metadata are SQLite; keep them that way. |
| **Cloud is optional, never required** | Every code path must degrade gracefully to local inference if all cloud keys are absent. |
| **Routing logic lives in `orchestrator.py`** | Don't add routing decisions in `api.py` or bot adapters. |
| **Bot adapters are thin** | Bots parse events, call the orchestrator, deliver responses. No business logic in `bots/`. |

---

## How to Add a New Cloud Provider

1. Open `src/assistant/llm/cloud_router.py`.
2. Add `_call_<provider>(self, prompt: str) -> str`.
3. Register the provider in `route()` with keyword triggers or a new routing tier.
4. Add the API key env var to `src/assistant/config.py`.
5. Document it in `.env.example`.
6. Make sure `Tier 4` fallback still routes to local if your provider raises an exception.

---

## How to Add a New Routing Keyword

Routing keywords live in `src/assistant/orchestrator.py`. Adding to Tier 2 is as simple as extending a set:

```python
# Route "debug" / "trace" / "stack trace" to groq
REASONING_KEYWORDS = {
    "analyze", "compare", "tradeoff", "root cause",
    "debug", "trace", "stack trace",   # ← add here
}
```

Add a test case in `scripts/test_agent_end_to_end.py` that verifies the new keyword routes correctly.

---

## How to Add a New Bot Platform

1. Create `src/assistant/bots/<platform>_bot.py`.
2. Implement a function that:
   - Listens for platform events.
   - Extracts `(user_id, message_text)`.
   - Calls the orchestrator (directly or via `/query`).
   - Delivers the response using `messaging/senders.py`.
3. Register the startup coroutine in `src/assistant/api.py` lifespan.

---

## Testing

Run the end-to-end suite before opening a PR:

```bash
python scripts/test_agent_end_to_end.py
```

If you're touching LangChain MCP integration:

```bash
python scripts/check_langchain_docs_mcp.py
```

When adding features, extend `scripts/test_agent_end_to_end.py` with representative cases for your change. Untested code is just a bug that hasn't introduced itself yet.

---

## Pull Request Checklist

Before hitting "Create Pull Request", confirm:

- [ ] `pyright src/` exits cleanly (or I've explained the exception).
- [ ] `scripts/test_agent_end_to_end.py` passes.
- [ ] `.env` is **not** committed.
- [ ] Relevant wiki page is updated if behaviour changed.
- [ ] `.env.example` is updated if a new env var was added.
- [ ] PR description explains *what* and *why*, not just *what*.
- [ ] PR touches one logical concern only.

---

## Commit Message Style

Use imperative mood. Write what the commit *does*, not what you *did*:

| ✅ Good | ❌ Bad |
|--------|-------|
| `Add streaming response support` | `Added streaming` |
| `Fix Tier 2 keyword matching for long inputs` | `fixes bug` |
| `Update RAG store to support PDF ingestion` | `pdf stuff` |

---

## Reporting Bugs

When filing a bug report, include:

- **Platform**: Raspberry Pi 5 / Windows / Linux / other
- **Python version**: `python3 --version`
- **Relevant `.env` settings** — redact all actual keys, show the key names
- **Full traceback** from the server log
- **Steps to reproduce** — if we can't reproduce it, we can't fix it

Bonus points for a minimal reproduction case. Double bonus points if you've already identified the line where it breaks.

---

## Licensing

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

You get credit in the commit history. That's the deal. It's a good deal.
