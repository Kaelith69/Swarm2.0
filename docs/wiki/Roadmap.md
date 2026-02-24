# Roadmap

Where Swarm2.0 is going — features that are planned, features that are dreamed about, and the honest assessment of each.

---

## Status Legend

| Symbol | Meaning |
|---|---|
| ✅ | Done — ships in v2.0 |
| 🔨 | In progress |
| 📋 | Planned — has a path |
| 💭 | Dreamed — no path yet |
| 🪦 | Probably never — but listed for honesty |

---

## Core Infrastructure

| Status | Feature | Notes |
|---|---|---|
| ✅ | 4-tier routing cascade | keyword + LLM classifier + fallback |
| ✅ | Local llama.cpp inference | subprocess-based, Gemma 2B Q4_K_M |
| ✅ | Cloud routing (Groq, Gemini, Kimi) | with graceful fallback |
| ✅ | RAG with hnswlib + SQLite | sentence-transformers embeddings |
| ✅ | Per-user conversation memory | SQLite, configurable N turns |
| ✅ | Configurable personality | YAML or env vars |
| ✅ | Telegram bot (polling + webhook) | |
| ✅ | Discord bot (gateway + webhook) | |
| ✅ | Windows support | PowerShell installer, polling mode |
| ✅ | Raspberry Pi 5 support | install_pi.sh, systemd, nginx |
| 📋 | Streaming responses | Stop waiting for full generation; stream tokens |
| 📋 | `/memory/clear` API endpoint | User-facing memory reset without SQLite access |
| 📋 | `/ingest` API endpoint | Trigger RAG ingestion via HTTP instead of CLI |

---

## Interface & Integrations

| Status | Feature | Notes |
|---|---|---|
| 📋 | Web UI | Simple browser-based chat interface. React or Svelte. No login required for local use. |
| 📋 | OpenAI-compatible API layer | `POST /v1/chat/completions` — drop-in replacement for OpenAI SDK integrations |
| 💭 | Voice interface | Whisper STT → orchestrator → TTS. The Pi 5 might handle it. Might. |
| 💭 | Matrix/Element bot | For the three people who use Matrix. You know who you are. |
| 💭 | Slack bot | Requires a paid Slack workspace for most orgs. Deprioritized. |
| 💭 | WhatsApp | Their unofficial API situation is a nightmare. No promises. |

---

## Intelligence & Routing

| Status | Feature | Notes |
|---|---|---|
| 📋 | Tool use / function calling | Let the agent call external functions (web search, calculator, weather, etc.) |
| 📋 | Better routing metrics | Log routing decisions to SQLite for analysis and tuning |
| 📋 | Per-user routing preferences | Let users opt in/out of cloud routes |
| 💭 | Multi-agent orchestration | Multiple specialized agents collaborating. The "Swarm" part starts making sense. |
| 💭 | Fine-tuned routing classifier | Train a tiny model specifically for routing decisions instead of repurposing Gemma |
| 💭 | Context-aware model selection | Track which model gives better answers per user/topic and route accordingly |

---

## Operations & Deployment

| Status | Feature | Notes |
|---|---|---|
| 📋 | Rate limiting | Per-user request limits to prevent API bill shocks |
| 📋 | Prometheus metrics endpoint | `/metrics` for Grafana dashboards |
| 📋 | Docker / docker-compose | Containerized deployment |
| 📋 | Model hot-swap | Change `MODEL_PATH` without server restart |
| 💭 | Kubernetes helm chart | For when someone deploys this at scale. Respect. |
| 💭 | ARM64 Docker image | Pre-built image for Pi |

---

## Privacy & Security

| Status | Feature | Notes |
|---|---|---|
| ✅ | Ed25519 Discord verification | Via PyNaCl |
| ✅ | Telegram secret token verification | |
| ✅ | `EXPOSE_DELIVERY_ERRORS=false` | |
| 📋 | Encrypted memory storage | SQLite-level encryption for conversation history |
| 📋 | Per-user data export | GDPR-friendly conversation history dump |
| 📋 | Audit log | Record which messages went to which provider |
| 💭 | E2E encrypted API | TLS is table stakes; this would require client-side key management |

---

## Hardware Targets

| Status | Target | Notes |
|---|---|---|
| ✅ | Raspberry Pi 5 (8 GB) | Primary target — tuned defaults, install script |
| ✅ | Windows 10/11 (x86_64 CPU) | Fully supported with polling mode |
| ✅ | Linux server (x86_64) | Works; webhook mode recommended |
| 📋 | Raspberry Pi 5 (4 GB) | Needs tighter defaults; requires smaller model |
| 💭 | Raspberry Pi Zero 2W | It has 512 MB RAM. Local inference: no. Cloud-only relay: maybe? |
| 💭 | Orange Pi / other SBCs | Should work with manual llama.cpp build but untested |
| 🪦 | Original Raspberry Pi 4 | 4 cores of A72, single-channel RAM, SD card I/O. You'll be there tomorrow. |

---

## Known Limitations (Won't Fix)

These are design tradeoffs, not bugs:

| Limitation | Reason | Workaround |
|---|---|---|
| Single worker only | SQLite not safe across processes | Use a single `uvicorn` worker; it's sufficient for Pi workloads |
| No async llama.cpp | `llama-cli` is a blocking subprocess | Entire request/response is synchronous during local inference |
| Memory not shared across bots | user_ids differ by platform (`tg:` vs `dc:`) | Intentional — users are distinct on each platform |
| No GPU support | This is designed for CPU inference on a Pi | If you have a GPU, use a real inference server and point cloud routes at it |

---

## Contributing to the Roadmap

Want to work on something from this list? Check if there's an open issue for it, or open one. PRs for `📋 Planned` items are very welcome. PRs for `💭 Dreamed` items need a discussion first — architecture decisions matter.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to get started.
