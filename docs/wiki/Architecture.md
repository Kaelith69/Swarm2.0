# Architecture

Swarm2.0 is built around a central orchestrator that routes messages to the best available inference backend. This page explains every component and how they connect.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Message                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ Telegram Bot │  │ Discord Bot  │  │  REST API    │
  │  (polling or │  │  (gateway or │  │  POST /query │
  │   webhook)   │  │   webhook)   │  │              │
  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
         └─────────────────┼──────────────────┘
                           │
              ┌────────────▼────────────┐
              │      FastAPI Server      │
              │  :8000  (single worker)  │
              │  /health /query          │
              │  /webhook/telegram       │
              │  /webhook/discord        │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │    AgentOrchestrator    │◄── RAG Store ──► hnswlib + SQLite
              │                         │◄── ConvMemory ──► SQLite
              │  4-tier routing cascade │
              └────────────┬────────────┘
                           │
        ┌──────────────────┼──────────────────────┐
        ▼                  ▼          ▼            ▼
 ┌───────────┐   ┌──────────────┐ ┌────────┐ ┌────────┐
 │  Local    │   │   Groq API   │ │Gemini  │ │ Kimi   │
 │  Gemma 2B │   │ LLaMA 3.1 8B │ │1.5 Flash│ │v1-8k  │
 │ llama.cpp │   │  (reasoning) │ │(long   │ │(plan.) │
 │subprocess │   │              │ │context)│ │        │
 └───────────┘   └──────────────┘ └────────┘ └────────┘
```

---

## Components

### FastAPI Server (`api.py`)

The entry point for all traffic. A single-worker `uvicorn` server listens on port 8000 (configurable via `PORT`).

**Endpoints:**

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Server status, cloud availability, bot mode |
| `/query` | POST | Main query endpoint — returns `route`, `reason`, `response` |
| `/webhook/telegram` | POST | Telegram webhook receiver |
| `/webhook/discord` | POST | Discord webhook / interactions receiver |

**Lifespan management:** When `BOT_MODE=polling`, the server starts Telegram and Discord bots as async background tasks in the same process via `asyncio.create_task`. On shutdown, tasks are cancelled cleanly.

### AgentOrchestrator (`orchestrator.py`)

The brain. Every message passes through `respond_with_route(message, user_id)` which:

1. Retrieves RAG context (always)
2. Loads conversation history (always)
3. Runs the 4-tier routing decision
4. Dispatches to the selected backend
5. Records the turn in memory
6. Returns a `RouteResult(route, reason, response)`

The `route` and `reason` fields provide full explainability for every response.

### 4-Tier Routing Cascade

The routing logic lives in `_route()`:

**Tier 1 — Short message fast-path:**
```
if len(message) ≤ LOCAL_SHORT_THRESHOLD_CHARS (150)
   AND no reasoning signal
   AND no planning signal:
     → local_simple (reason: short_message)
```
No routing overhead. Zero latency hit for simple queries.

**Tier 2 — Keyword fast-path:**
```
planning keywords (plan, roadmap, strategy, workflow, …)  → kimi
len ≥ LONG_CONTEXT_THRESHOLD_CHARS (1200)                 → gemini
reasoning keywords (analyze, compare, tradeoff, …)        → groq
RAG keywords (docs, document, knowledge base, retrieve, …)→ local_rag
```

**Tier 3 — LLM classifier (when `USE_LLM_ROUTING=true`):**
Local Gemma is asked to classify the query as `LOCAL`, `GROQ`, `GEMINI`, or `KIMI`. The classification uses a short system prompt and only the first 500 characters of the message to minimize latency.

**Tier 4 — Cloud fallback:**
If a cloud API key is missing or the API call fails, the orchestrator falls back to local inference transparently. The response is returned with `reason: groq_unavailable` (or `gemini_unavailable`, `kimi_unavailable`).

### LlamaCppRunner (`llm/llama_cpp_runner.py`)

Wraps the `llama-cli` binary as a subprocess. Two modes:
- `generate(prompt)` — full inference for response generation
- `classify(prompt)` — short inference for routing classification (called by Tier 3)

The subprocess is given `LLAMA_TIMEOUT_SECONDS` (default: 120s) before being killed. On Pi 5, set this generously — a 256-token response can take up to 10 seconds.

### CloudRouter (`llm/cloud_router.py`)

Wraps the three cloud SDKs:
- **Groq** — uses the official `groq` Python SDK
- **Gemini** — uses `google-generativeai`
- **Kimi** — uses the OpenAI-compatible `openai` SDK pointed at `KIMI_BASE_URL`

Each provider has an `is_<provider>_available()` check that returns `True` only if the API key is non-empty.

### RagStore (`rag/store.py`)

The knowledge base engine. It stares at your documents until text confesses its secrets.

- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` — a 22 MB model that turns text into 384-dimensional vectors
- **Index:** `hnswlib` HNSW graph — approximate nearest neighbor search, sub-millisecond query time even for large indexes
- **Metadata:** SQLite — stores chunk content, source label, and chunk index alongside the vector IDs
- **Ingestion:** `scripts/ingest_documents.py` splits documents into ~500-word chunks, embeds each chunk, and stores vectors + metadata

On every query, the top-k=3 most relevant chunks are retrieved and formatted as a context block injected into the prompt.

### ConversationMemory (`memory.py`)

SQLite-backed per-user conversation history.

- Stores `(user_id, role, content, timestamp)` rows
- Retrieves the last `MEMORY_MAX_TURNS * 2` rows (N turns = N user + N assistant messages)
- Trims old rows after each `add_turn` to keep the table bounded
- Formatted as a "Previous conversation" block prepended to prompts

Thread-safety: fresh connection per operation. No shared connection objects. Safe for single-threaded async FastAPI.

### Personality (`personality.py`)

Loads at startup from `personality.yaml` (takes precedence) or `AGENT_*` environment variables. Exposes `system_prompt(is_local: bool)` which returns a system instruction block injected into every prompt.

- `is_local=True`: compact prompt to save tokens on Pi 5
- `is_local=False`: full prompt with all personality fields for cloud models

### Bots

**TelegramPoller (`bots/telegram_polling.py`):**  
Long-polls the Telegram `getUpdates` API (30-second timeout). Tracks the offset to avoid replaying old messages. Runs as an `asyncio` task inside the main server process.

**DiscordBot (`bots/discord_bot.py`):**  
Full `discord.py` WebSocket gateway bot. Responds to messages in channels where it has been added. Requires "Message Content Intent" to be enabled in the Discord Developer Portal.

---

## Storage Layout

```
data/rag/                    ← RAG_DATA_DIR
├── index.bin                ← hnswlib HNSW index
├── metadata.sqlite3         ← RAG chunk metadata
└── memory.sqlite3           ← per-user conversation history
```

Both SQLite files share the same directory. **Do not access these files with multiple processes simultaneously.**

---

## Deployment Targets

| Target | Notes |
|---|---|
| Raspberry Pi 5 (8 GB, aarch64) | Primary target. Runs 4 × Cortex-A76 cores. NVMe strongly recommended for I/O. |
| Windows 10/11 (x86_64, CPU) | Full support. Polling mode recommended (no public URL needed). |
| Linux server (x86_64) | Supported. Use webhook mode with nginx reverse proxy. |
