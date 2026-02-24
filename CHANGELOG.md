# Changelog

All notable changes to Swarm 2.0 are documented here.

Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Planned
- Streaming responses — because waiting 8 seconds in silence is character-building, but we've built enough character.
- Web UI dashboard — for the people who think CLIs are "too much terminal energy."
- Additional cloud providers — moar endpoints, moar routing decisions, moar latency to feel powerful about avoiding.
- Voice / TTS integration — so the Pi can talk back at you in addition to judging you silently.
- Multi-agent swarm coordination — the name "Swarm 2.0" finally starts making sense.

---

## [2.0.0] — 2025

### Added
- **4-tier routing cascade** — the orchestration brain that decides, per message, whether to think locally or phone a cloud friend. Works even when you forget to set `USE_LLM_ROUTING`.
- **Local inference via llama.cpp** — Gemma 2 2B Q4_K_M fits in ~1.6 GB RAM. The Pi is not scared.
- **Groq cloud route** — because sometimes a question deserves 0.3-second reasoning instead of 8-second reasoning.
- **Google Gemini Flash route** — for when someone sends a 1500-character essay into your bot and expects coherent output.
- **Kimi / Moonshot route** — planning, roadmaps, multi-step workflows: the things that make local models quietly weep.
- **LLM-based classifier (Tier 3)** — when keywords aren't enough, ask a smarter model to decide which model to use. Yes, we see the recursion. No, we're not sorry.
- **Automatic Tier 4 fallback** — if every cloud API key is missing or the internet has opinions, local inference picks up the slack without drama.
- **Local RAG pipeline** — HNSW vector search over ingested documents, injected into every prompt. Knowledge base included; omniscience not guaranteed.
- **Per-user SQLite memory** — conversation history that persists across sessions. The bot will remember. This is sometimes convenient and occasionally unsettling.
- **Personality YAML engine** — configure agent identity, character, and expertise without touching source code. Finally, customisation for people who don't want to customise source code.
- **Telegram bot** — polling and webhook modes. Set it, forget it, let it answer questions at 3 AM without waking you up.
- **Discord bot** — Gateway (polling) and interactions webhook. Ed25519 signature verification included so random strangers can't puppet your bot.
- **FastAPI REST API** — `POST /query`, `GET /health`, webhook endpoints. `curl`-friendly by design.
- **Raspberry Pi 5 support** — active cooling recommended. Not because it'll melt, but because it'll throttle at 80 °C and you'll blame the software.
- **Windows support** — PowerShell install script included. Yes, it works. No, you don't need WSL (but WSL is fine too).
- **Document ingestion CLI** — `.txt`, `.md`, `.pdf` ingestion into the RAG store. Feed it your documentation; it will not complain.
- **Explainable routing** — every response includes `route`, `reason`, `rag_used`, and `memory_turns`. Black boxes are for magic acts, not production systems.
- **End-to-end test script** — `scripts/test_agent_end_to_end.py`. Runs real queries against a live server. Green means go; red means coffee first.

### Fixed
- Fixed bug where the orchestrator would attempt cloud routing when no cloud keys were configured. It now correctly concludes that "cloud is unavailable" rather than spending 10 seconds finding out the hard way.
- Fixed Tier 2 keyword matching that would incorrectly trigger on substrings. `"analyze"` now routes to Groq; `"psychoanalyze"` no longer makes the same assumption.
- Fixed memory injection that would occasionally include turns from a different user's session when user IDs were numeric strings that compared equal as integers. SQLite type coercion is a gift that keeps giving.
- Fixed Discord Ed25519 verification that would return HTTP 200 on signature failure when `EXPOSE_DELIVERY_ERRORS=true`. It now correctly returns HTTP 401 regardless of your feelings about error transparency.
- Fixed RAG store that would panic on empty document collections at startup. It now quietly initialises an empty index and moves on, like a professional.
- Fixed bug where reality stopped working if `PYTHONPATH` wasn't set before importing `assistant`. Added this to every setup script so it's harder to forget.

### Changed
- Moved all configuration to a `Settings` dataclass in `config.py`. If you were accessing `os.environ` directly in your fork, sorry about that.
- Separated bot adapters into `telegram_polling.py` and `discord_bot.py`. Previously they were entangled in `api.py` in a way that made testing require a Telegram account.
- Renamed `reason` field values to be human-readable strings (`short_message`, `kw_reasoning`, `llm_classifier`) instead of internal integer codes. If you were parsing integer codes, that's on you.

### Security
- Added `PyNaCl` for Discord Ed25519 interaction signature verification.
- Added configurable `TELEGRAM_SECRET` token validation on the webhook endpoint.
- Set `EXPOSE_DELIVERY_ERRORS=false` as default — internal tracebacks no longer travel to end users.

---

## [1.0.0] — 2024

### Added
- Initial release. Single-tier routing. Local inference only. One bot. It worked. Mostly.
- README that was technically accurate and aesthetically neutral.
- LICENSE that legally protects us from being blamed when the Pi overheats.

---

*The format of this changelog is intentionally human-readable. Machines have the source code; humans deserve prose.*
