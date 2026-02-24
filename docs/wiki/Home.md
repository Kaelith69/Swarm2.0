# Swarm2.0 Wiki — Home

Welcome to the Swarm2.0 wiki. If you're here, you either want to understand how this thing works, or something broke and you're looking for answers. Either way, you're in the right place.

---

## 🗺️ Wiki Pages

| Page | What's in it |
|---|---|
| [Architecture](Architecture.md) | How the system is built — components, routing, storage |
| [Installation](Installation.md) | Step-by-step setup for Raspberry Pi 5 and Windows |
| [Usage](Usage.md) | API endpoints, routing behavior, RAG, bots, personality |
| [Privacy](Privacy.md) | Where your data goes (and where it doesn't) |
| [Troubleshooting](Troubleshooting.md) | When things go sideways — common failures and fixes |
| [Roadmap](Roadmap.md) | What's planned, what's dreamed, what's probably never happening |

---

## 🧠 The 30-Second Pitch

Swarm2.0 is a **hybrid AI assistant** that runs on:

- 🥧 Raspberry Pi 5 (8 GB) — a $100 computer you can hold in one hand
- 🪟 Windows 10/11 — your normal human computer

It routes every incoming message to the best available inference backend:

1. **Local Gemma 2B** via `llama.cpp` — fast, private, on-device
2. **Groq** — cloud, fast, for reasoning queries
3. **Gemini** — cloud, for long context
4. **Kimi/Moonshot** — cloud, for planning and strategy

The routing decision is made per-message by a 4-tier cascade: message length → keyword signals → local LLM classifier → fallback to local. RAG context and conversation history are injected into every prompt regardless of which backend is used.

It talks to users via **Telegram** and **Discord** bots, in either polling mode (no public URL needed) or webhook mode (for servers with a public HTTPS endpoint).

---

## 🏁 Quick Navigation

- **First time here?** Start with [Installation](Installation.md).
- **Want to understand the system?** Read [Architecture](Architecture.md).
- **Something broke?** Check [Troubleshooting](Troubleshooting.md).
- **Curious about data privacy?** See [Privacy](Privacy.md).
- **Want to contribute?** Read [CONTRIBUTING.md](../CONTRIBUTING.md) in the repo root.

---

## 🔑 Key Concepts

### Hybrid Inference

The system doesn't commit to one inference strategy. It keeps a local model for cheap, private, always-available responses, and routes to cloud APIs for queries that benefit from more capable models. When cloud APIs are unavailable or misconfigured, it falls back to local gracefully.

### RAG (Retrieval-Augmented Generation)

Before any prompt is sent to any backend, the orchestrator queries a local vector store for relevant content from your ingested documents. That content gets injected as context. The local model and all cloud models benefit equally from this — every backend gets the same retrieved knowledge.

The RAG store uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings, `hnswlib` for approximate nearest neighbor search, and SQLite for metadata. Everything lives on your device.

### Conversation Memory

Per-user conversation history is stored in SQLite and prepended to every prompt. The `user_id` is derived from the bot platform (`tg:<id>`, `dc:<id>`, or `api` for direct API calls). Memory persists across server restarts.

### Personality

The assistant's identity — name, character, response style, humor, and expertise — is loaded from `personality.yaml` or environment variables at startup and injected as a system instruction into every prompt (local and cloud). This makes every backend sound like the same character.

---

## ⚠️ Important Constraints

- **Single-worker only.** The application uses SQLite for both RAG and memory. Running with `uvicorn --workers N` (N > 1) will cause data corruption. This is a known, accepted design tradeoff.
- **`llama.cpp` is optional.** If you don't set `MODEL_PATH` and `LLAMA_MAIN_PATH`, local inference will fail gracefully and the system falls back to whatever cloud providers are configured.
- **Cloud keys are optional.** If no cloud keys are set, all routes fall back to local inference.
