# Contributing

Thank you for your interest in contributing to Swarm 2.0! This page covers the developer workflow, code style, and how to submit changes.

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
# Edit .env with local model path and any API keys you want to test with
```

### 4. Set PYTHONPATH

```bash
export PYTHONPATH=$(pwd)/src   # Windows: $env:PYTHONPATH = "$(pwd)\src"
```

### 5. Verify the setup

```bash
python -m assistant.agent &
sleep 5
curl http://127.0.0.1:8000/health
kill %1
```

---

## Project Structure

Key directories and their purpose:

```
src/assistant/
├── agent.py          — entry point; do not add business logic here
├── api.py            — FastAPI app; add new endpoints here
├── config.py         — all config via Settings dataclass; add new env vars here
├── orchestrator.py   — routing logic; modify for new routing tiers
├── personality.py    — identity system; extend for new personality fields
├── memory.py         — conversation history; extend for new memory strategies
├── llm/              — LLM backends; add new providers here
├── rag/              — vector store; extend for new retrieval strategies
├── messaging/        — platform parsers and senders; add new platforms here
└── bots/             — bot adapters; add new bot integrations here
```

---

## Adding a New Cloud Provider

1. Open `src/assistant/llm/cloud_router.py`.
2. Add a new method `_call_<provider>(self, prompt: str) -> str`.
3. Register the provider in `route()` with appropriate keyword triggers.
4. Add environment variable handling to `src/assistant/config.py`.
5. Document the new env var in `.env.example`.

---

## Adding a New Routing Keyword

Routing keywords are defined in `src/assistant/orchestrator.py` in the Tier 2 section. To add a new keyword group:

```python
# Example: route "debug" / "trace" / "stack trace" to groq
REASONING_KEYWORDS = {
    "analyze", "compare", "tradeoff", "root cause",
    "debug", "trace", "stack trace",   # ← add here
}
```

---

## Adding a New Bot Platform

1. Create `src/assistant/bots/<platform>_bot.py`.
2. Implement a function that:
   - Receives platform events.
   - Extracts `(user_id, message_text)`.
   - Calls the orchestrator via the FastAPI `/query` endpoint or directly.
   - Delivers the response using `messaging/senders.py`.
3. Register the bot startup in `src/assistant/api.py` lifespan.

---

## Code Style

- Follow **PEP 8** for all Python code.
- Use **type annotations** on all function signatures (Pyright is configured in `pyproject.toml`).
- Keep functions focused and small; prefer composition over inheritance.
- Do not add print statements; use `logging` module.
- No secrets in source code — all configuration via `.env`.

### Type checking

```bash
pip install pyright
pyright src/
```

---

## Testing

Run the end-to-end test suite:

```bash
python scripts/test_agent_end_to_end.py
```

Validate LangChain MCP integration (if applicable):

```bash
python scripts/check_langchain_docs_mcp.py
```

When adding new features, extend `scripts/test_agent_end_to_end.py` with representative test cases.

---

## Pull Request Guidelines

1. **Branch naming:** `feat/<short-description>`, `fix/<issue>`, `docs/<topic>`.
2. **Commit messages:** Use imperative mood: `Add streaming response support`, `Fix Tier 2 keyword matching`.
3. **One concern per PR:** Keep PRs small and focused.
4. **Update documentation:** If you change behaviour, update the relevant wiki page and `.env.example`.
5. **Do not commit `.env`** or any file containing secrets.
6. **SQLite discipline:** Never add multi-process or multi-threaded SQLite access.

---

## Issue Reporting

When opening a bug report, include:

- Platform (Pi 5 / Windows / other)
- Python version (`python3 --version`)
- Relevant `.env` settings (redact all secrets)
- Full traceback from server logs
- Steps to reproduce

---

## Licensing

By contributing, you agree that your contributions will be licensed under the [MIT License](https://github.com/Kaelith69/Swarm2.0/blob/main/LICENSE).
