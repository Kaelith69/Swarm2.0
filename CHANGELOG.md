# Changelog

All notable changes to Swarm2.0 are documented here.

Format: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.  
Change categories: `Added`, `Changed`, `Fixed`, `Removed`, `Security`, `Performance`.

---

## [2.0.0] — 2024 (Current)

The Big One. Version 2.0 is basically a full rebuild that actually works on both Windows and a credit-card-sized computer simultaneously.

### Added

- **Windows support** — PowerShell installer (`deploy/install_windows.ps1`), start script (`scripts/start_windows.ps1`), `.bat` launcher, and Task Scheduler integration. Windows users are now first-class citizens.
- **Polling bot mode** (`BOT_MODE=polling`) — Telegram long-polling and Discord WebSocket gateway run as async background tasks inside the FastAPI process. No public URL, no ngrok, no suffering.
- **Discord polling bot** — Full `discord.py` WebSocket gateway bot with Message Content Intent support.
- **Telegram polling bot** — `getUpdates` long-polling with automatic offset tracking.
- **Configurable personality system** — Load agent identity, tone, humor, and expertise from `personality.yaml` or environment variables (`AGENT_NAME`, `AGENT_PERSONALITY`, `AGENT_RESPONSE_STYLE`, `AGENT_HUMOR`, `AGENT_EXPERTISE`). YAML takes precedence when present.
- **`personality.yaml.example`** — Template for the personality configuration file.
- **LLM routing classifier** (`USE_LLM_ROUTING=true`) — Local Gemma classifies ambiguous queries and routes them to the best cloud backend before falling back to local. Disable for pure keyword routing.
- **`llm_classifier` and `llm_classifier_local` routing reasons** — Full explainability for LLM-classified routes.
- **Platform-aware path defaults** — `config.py` auto-detects Windows vs Linux and sets sensible default paths for `MODEL_PATH` and `LLAMA_MAIN_PATH`.
- **`LLAMA_TIMEOUT_SECONDS`** — Configurable subprocess timeout for llama.cpp (default: 120s).
- **Discord Ed25519 signature verification** — Via `PyNaCl` when `DISCORD_PUBLIC_KEY` is set. Proper cryptographic verification for webhook interactions.
- **Discord Interaction type 2 support** — Returns `{"type": 4}` response directly, preventing "Interaction Failed" errors in the Discord client.
- **`/health` endpoint enhancements** — Now reports `bot_mode`, `agent_name`, and individual cloud provider availability.
- **`publish_to_github.ps1`** — Windows PowerShell script for publishing to GitHub via the `gh` CLI.
- **Narrowed RAG keyword signals** — Removed over-broad keywords (`context`, `based on`) that caused false RAG routing. Retrieval intent is now more precisely detected.
- **`pi_start_and_check.sh`** — One-command Pi start + health check + smoke test script.

### Changed

- **`AgentOrchestrator`** now accepts an optional `Personality` instance and injects it into both local and cloud prompts.
- **`ConversationMemory`** and **`RagStore`** unified under `RAG_DATA_DIR` — same directory, same SQLite discipline.
- **Routing table** updated: Tier 2 RAG signal now stays local (`local_rag`) instead of routing to cloud. Rationale: RAG queries are retrieval-focused and the local model with context is sufficient.
- **Single-worker constraint** formally documented — `uvicorn --workers N` is explicitly unsupported and warned against throughout the codebase and docs.

### Fixed

- **Discord webhook PING before signature check** — PING (type 1) messages are now returned immediately before any auth processing, preventing 401 errors during Discord webhook registration.
- **Windows path handling** — `config.py` uses `pathlib.Path` throughout, avoiding mixed-separator issues.
- **`_env_bool` parsing** — Accepts `"1"`, `"true"`, `"yes"`, `"on"` (case-insensitive). No more `USE_LLM_ROUTING=True` silently being treated as False.

### Security

- `EXPOSE_DELIVERY_ERRORS=false` default prevents raw provider error messages from leaking through webhook responses.
- `.env` excluded from git via `.gitignore` in both root and `agentic_assistant/` scopes.
- `MAX_INPUT_CHARS=8000` default prevents abuse and surprise cloud bills.
- Discord `X-Signature-Ed25519` + `X-Signature-Timestamp` verification via PyNaCl.
- Telegram `X-Telegram-Bot-Api-Secret-Token` header verification.

---

## [1.0.0] — 2024

The original Pi-only build. It worked. Mostly. If you squinted.

### Added

- **Hybrid routing** — local `llama.cpp` + Groq + Gemini + Kimi with keyword-based fast-path.
- **RAG store** — `sentence-transformers` embeddings, `hnswlib` ANN index, SQLite metadata store.
- **Per-user conversation memory** — SQLite backend with configurable turn limit.
- **FastAPI server** — `/health`, `/query`, `/webhook/telegram`, `/webhook/discord`.
- **Telegram webhook** — With optional secret token verification.
- **Discord webhook** — With optional bearer token verification.
- **4-tier routing cascade** — Short message → keyword → (no LLM classifier yet) → local fallback.
- **Raspberry Pi 5 install script** (`deploy/install_pi.sh`) — Installs system packages, builds llama.cpp, creates venv.
- **systemd service file** (`deploy/agent.service`).
- **Nginx config** (`deploy/nginx-agent.conf`).
- **Document ingestion script** (`scripts/ingest_documents.py`) — Supports `.txt`, `.md`, `.pdf`.

---

*For unreleased changes, check the [open PRs](https://github.com/Kaelith69/Swarm2.0/pulls) or the [commit log](https://github.com/Kaelith69/Swarm2.0/commits/main).*
