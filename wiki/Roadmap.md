# Roadmap

This page tracks planned features, improvements, and long-term direction for Swarm 2.0.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete and merged |
| 🔄 | In progress |
| 🔜 | Planned — high priority |
| 💡 | Under consideration |

---

## Current Release — v2.0

| Feature | Status |
|---------|--------|
| 4-tier routing cascade (local → keyword → classifier → fallback) | ✅ |
| Local inference via llama.cpp (Gemma 2 2B Q4\_K\_M) | ✅ |
| Groq cloud integration (fast reasoning) | ✅ |
| Google Gemini Flash integration (long context) | ✅ |
| Kimi / Moonshot integration (planning) | ✅ |
| Retrieval-Augmented Generation (HNSW + sentence-transformers + SQLite) | ✅ |
| Per-user conversation memory (SQLite) | ✅ |
| Telegram bot (polling + webhook) | ✅ |
| Discord bot (gateway + interactions webhook) | ✅ |
| YAML personality system | ✅ |
| FastAPI REST endpoints (`/query`, `/health`, `/webhook/*`) | ✅ |
| Raspberry Pi 5 deployment (systemd + Nginx) | ✅ |
| Windows deployment (PowerShell scripts) | ✅ |
| Document ingestion CLI (txt, md, pdf) | ✅ |
| Ed25519 Discord webhook verification | ✅ |
| Telegram webhook secret token verification | ✅ |
| Explainable routing (route + reason in every response) | ✅ |

---

## Upcoming — v2.1

| Feature | Status | Notes |
|---------|--------|-------|
| **Streaming responses** | 🔜 | Server-sent events for `/query`; bot adapters to send progressive messages |
| **Web UI dashboard** | 🔜 | Minimal browser UI for health, recent queries, route stats |
| **Route analytics** | 🔜 | SQLite log of route/reason/latency per request |
| **Per-user RAG namespacing** | 🔜 | Allow each user to have an isolated knowledge base |
| **Configurable RAG chunk size** | 🔜 | Expose `CHUNK_SIZE` and `CHUNK_OVERLAP` in `.env` |

---

## Future — v2.2+

| Feature | Status | Notes |
|---------|--------|-------|
| **Additional cloud providers** | 🔜 | Anthropic Claude, Mistral, OpenAI |
| **Voice / TTS integration** | 🔜 | Text-to-speech output for voice channel support in Discord |
| **Multi-agent swarm coordination** | 💡 | Multiple assistant instances coordinating via message bus |
| **Long-term memory (semantic)** | 💡 | Persistent semantic memory beyond conversation turns |
| **Tool use / function calling** | 💡 | Allow LLM to call external tools (web search, calculator) |
| **On-device fine-tuning** | 💡 | Low-rank adaptation (LoRA) on Pi 5 using collected data |
| **ARM64 llama.cpp Python bindings** | 💡 | Replace subprocess with `llama-cpp-python` if Pi 5 stability improves |
| **Docker / container deployment** | 💡 | OCI image for easy deployment on any Linux host |
| **Slack / Teams bot adapters** | 💡 | Extend `bots/` for enterprise messaging platforms |

---

## Contributing to the Roadmap

Have a feature request or want to work on a planned item? 

1. Check [GitHub Issues](https://github.com/Kaelith69/Swarm2.0/issues) to see if it is already tracked.
2. Open a new issue with the `enhancement` label.
3. Read the [Contributing](Contributing) guide before submitting a PR.

---

## Version History

| Version | Highlights |
|---------|-----------|
| v2.0 | Hybrid routing, RAG, multi-bot, Pi 5 + Windows support |
| v1.x | Initial single-platform assistant (local only) |
