# Architecture

> **Swarm 2.0** is built around a single-worker FastAPI process that owns all subsystems as in-process singletons. This choice is deliberate: SQLite is not safe across multiple OS processes, and a Pi 5 workload does not require horizontal scaling at the API level.

---

## System Diagram

<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 560" width="820" height="560">
  <defs>
    <linearGradient id="aBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0F0A1E"/>
      <stop offset="100%" style="stop-color:#0D1B2A"/>
    </linearGradient>
    <linearGradient id="boxP" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#4C1D95"/><stop offset="100%" style="stop-color:#2D1B69"/>
    </linearGradient>
    <linearGradient id="boxB" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#1E3A8A"/><stop offset="100%" style="stop-color:#1E2A5A"/>
    </linearGradient>
    <linearGradient id="boxC" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#0E4A5C"/><stop offset="100%" style="stop-color:#083344"/>
    </linearGradient>
    <marker id="aArr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7C3AED"/>
    </marker>
    <marker id="aArrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563EB"/>
    </marker>
    <marker id="aArrC" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#06B6D4"/>
    </marker>
  </defs>
  <rect width="820" height="560" fill="url(#aBg)" rx="10"/>
  <text x="410" y="28" font-family="'Segoe UI',Arial,sans-serif" font-size="15" font-weight="700" fill="#E2E8F0" text-anchor="middle">Swarm 2.0 — Detailed System Architecture</text>

  <!-- CLIENTS -->
  <text x="60" y="60" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#475569">CLIENTS</text>
  <rect x="60" y="66" width="120" height="46" rx="7" fill="url(#boxB)" stroke="#2563EB" stroke-width="1.5"/>
  <text x="120" y="86" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="600" fill="#93C5FD" text-anchor="middle">Telegram</text>
  <text x="120" y="102" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#60A5FA" text-anchor="middle">Polling / Webhook</text>
  <rect x="210" y="66" width="120" height="46" rx="7" fill="url(#boxP)" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="270" y="86" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="600" fill="#C4B5FD" text-anchor="middle">Discord</text>
  <text x="270" y="102" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A78BFA" text-anchor="middle">Gateway / Webhook</text>
  <rect x="360" y="66" width="120" height="46" rx="7" fill="url(#boxC)" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="420" y="86" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="600" fill="#67E8F9" text-anchor="middle">REST Client</text>
  <text x="420" y="102" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#22D3EE" text-anchor="middle">curl / HTTP</text>

  <!-- Down arrows to API -->
  <line x1="120" y1="112" x2="120" y2="148" stroke="#2563EB" stroke-width="1.5" marker-end="url(#aArrB)"/>
  <line x1="270" y1="112" x2="270" y2="148" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#aArr)"/>
  <line x1="420" y1="112" x2="420" y2="148" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#aArrC)"/>

  <!-- API layer -->
  <text x="60" y="146" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#475569">API LAYER</text>
  <rect x="60" y="150" width="540" height="76" rx="7" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>
  <text x="330" y="174" font-family="'Segoe UI',Arial,sans-serif" font-size="13" font-weight="700" fill="#E2E8F0" text-anchor="middle">FastAPI Application — api.py</text>
  <rect x="75" y="182" width="110" height="28" rx="4" fill="#1E293B" stroke="#334155"/>
  <text x="130" y="200" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#94A3B8" text-anchor="middle">POST /query</text>
  <rect x="200" y="182" width="110" height="28" rx="4" fill="#1E293B" stroke="#334155"/>
  <text x="255" y="200" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#94A3B8" text-anchor="middle">GET /health</text>
  <rect x="325" y="182" width="130" height="28" rx="4" fill="#1E293B" stroke="#334155"/>
  <text x="390" y="200" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#94A3B8" text-anchor="middle">POST /webhook/telegram</text>
  <rect x="470" y="182" width="116" height="28" rx="4" fill="#1E293B" stroke="#334155"/>
  <text x="528" y="200" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#94A3B8" text-anchor="middle">POST /webhook/discord</text>

  <!-- Down arrow to orchestrator -->
  <line x1="330" y1="226" x2="330" y2="258" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#aArr)"/>

  <!-- Orchestrator -->
  <text x="60" y="256" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#475569">ORCHESTRATION</text>
  <rect x="60" y="260" width="540" height="80" rx="7" fill="#0F172A" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="330" y="282" font-family="'Segoe UI',Arial,sans-serif" font-size="13" font-weight="700" fill="#C4B5FD" text-anchor="middle">Orchestrator — orchestrator.py</text>
  <text x="330" y="298" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#64748B" text-anchor="middle">Tier-1 length check → Tier-2 keyword match → Tier-3 LLM classify → Tier-4 fallback</text>
  <text x="330" y="312" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#64748B" text-anchor="middle">Injects RAG context + memory history + personality system prompt into every inference call</text>
  <text x="330" y="328" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#475569" text-anchor="middle">Returns: response · route · reason · rag_used · memory_turns</text>

  <!-- Supporting modules row -->
  <line x1="160" y1="340" x2="110" y2="375" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#aArrC)"/>
  <line x1="260" y1="340" x2="240" y2="375" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#aArrC)"/>
  <line x1="330" y1="340" x2="370" y2="375" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#aArr)"/>
  <line x1="460" y1="340" x2="510" y2="375" stroke="#2563EB" stroke-width="1.5" marker-end="url(#aArrB)"/>
  <line x1="540" y1="340" x2="590" y2="375" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#aArr)"/>

  <!-- Support modules -->
  <rect x="60" y="375" width="110" height="46" rx="6" fill="url(#boxC)" stroke="#06B6D4" stroke-width="1"/>
  <text x="115" y="397" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#67E8F9" text-anchor="middle">RAG Store</text>
  <text x="115" y="411" font-family="'Segoe UI',Arial,sans-serif" font-size="8" fill="#22D3EE" text-anchor="middle">rag/store.py</text>

  <rect x="185" y="375" width="110" height="46" rx="6" fill="url(#boxC)" stroke="#06B6D4" stroke-width="1"/>
  <text x="240" y="397" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#67E8F9" text-anchor="middle">Memory</text>
  <text x="240" y="411" font-family="'Segoe UI',Arial,sans-serif" font-size="8" fill="#22D3EE" text-anchor="middle">memory.py</text>

  <rect x="310" y="375" width="120" height="46" rx="6" fill="url(#boxP)" stroke="#7C3AED" stroke-width="1"/>
  <text x="370" y="397" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#C4B5FD" text-anchor="middle">Personality</text>
  <text x="370" y="411" font-family="'Segoe UI',Arial,sans-serif" font-size="8" fill="#A78BFA" text-anchor="middle">personality.py</text>

  <rect x="445" y="375" width="110" height="46" rx="6" fill="url(#boxB)" stroke="#2563EB" stroke-width="1"/>
  <text x="500" y="397" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#93C5FD" text-anchor="middle">Config</text>
  <text x="500" y="411" font-family="'Segoe UI',Arial,sans-serif" font-size="8" fill="#60A5FA" text-anchor="middle">config.py</text>

  <rect x="570" y="375" width="110" height="46" rx="6" fill="url(#boxP)" stroke="#7C3AED" stroke-width="1"/>
  <text x="625" y="393" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#C4B5FD" text-anchor="middle">Messaging</text>
  <text x="625" y="407" font-family="'Segoe UI',Arial,sans-serif" font-size="8" fill="#A78BFA" text-anchor="middle">parsers / senders</text>

  <!-- Backends -->
  <line x1="115" y1="421" x2="115" y2="460" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#aArrC)"/>
  <line x1="370" y1="421" x2="330" y2="460" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#aArr)"/>
  <line x1="500" y1="421" x2="570" y2="460" stroke="#2563EB" stroke-width="1.5" marker-end="url(#aArrB)"/>

  <text x="60" y="458" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#475569">STORAGE / INFERENCE</text>
  <rect x="60" y="462" width="150" height="58" rx="7" fill="url(#boxC)" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="135" y="484" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#67E8F9" text-anchor="middle">SQLite + HNSW</text>
  <text x="135" y="499" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#22D3EE" text-anchor="middle">RAG vectors + metadata</text>
  <text x="135" y="513" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#22D3EE" text-anchor="middle">Conversation memory</text>

  <rect x="240" y="462" width="170" height="58" rx="7" fill="url(#boxP)" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="325" y="484" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#C4B5FD" text-anchor="middle">llama.cpp</text>
  <text x="325" y="499" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A78BFA" text-anchor="middle">Gemma 2 2B Q4_K_M</text>
  <text x="325" y="513" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A78BFA" text-anchor="middle">llama_cpp_runner.py</text>

  <rect x="440" y="462" width="200" height="58" rx="7" fill="url(#boxB)" stroke="#2563EB" stroke-width="1.5"/>
  <text x="540" y="484" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#93C5FD" text-anchor="middle">Cloud Providers</text>
  <text x="540" y="499" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#60A5FA" text-anchor="middle">Groq · Gemini · Kimi</text>
  <text x="540" y="513" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#60A5FA" text-anchor="middle">cloud_router.py</text>
</svg>

</div>

---

## Module Reference

### `src/assistant/agent.py` — Entry Point

Starts Uvicorn on port 8000 (configurable via `API_HOST` / `API_PORT`). Must be run with **single worker** to preserve SQLite thread safety.

```bash
python -m assistant.agent
# equiv: uvicorn assistant.api:app --host 0.0.0.0 --port 8000 --workers 1
```

---

### `src/assistant/api.py` — FastAPI Application

Creates the FastAPI `app` instance and mounts all routes. At startup it initialises all singletons:

| Singleton | Type | Purpose |
|-----------|------|---------|
| `settings` | `Settings` | Runtime config from `.env` |
| `personality` | `Personality` | Agent identity from YAML or env |
| `rag_store` | `RAGStore` | HNSW + SQLite vector store |
| `memory` | `ConversationMemory` | SQLite turn store |
| `local_llm` | `LlamaCppRunner` | Subprocess wrapper for llama-cli |
| `cloud_router` | `CloudRouter` | Multi-provider cloud client |

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness probe |
| `POST` | `/query` | Main inference endpoint |
| `POST` | `/webhook/telegram` | Telegram update ingestion |
| `POST` | `/webhook/discord` | Discord interaction ingestion |

---

### `src/assistant/orchestrator.py` — 4-Tier Routing Engine

The orchestrator is the core decision-making component. For each incoming message it:

1. Loads conversation history from `ConversationMemory`.
2. Retrieves relevant RAG chunks from `RAGStore`.
3. Runs the 4-tier routing cascade (see below).
4. Builds the full prompt (personality system prompt + memory + RAG + user query).
5. Calls the selected inference backend.
6. Saves the new turn to `ConversationMemory`.
7. Returns `{response, route, reason, rag_used, memory_turns}`.

**4-Tier Cascade:**

```
Tier 1  len(message) <= LOCAL_SHORT_THRESHOLD_CHARS (150) AND no complex signal
         → route: local_simple   reason: short_message

Tier 2  keyword match (evaluated in order):
         plan/roadmap/strategy/workflow  → kimi         reason: kw_planning
         len >= LONG_CONTEXT_THRESHOLD_CHARS (1200)     → gemini  reason: kw_long_context
         analyze/compare/tradeoff/…     → groq         reason: kw_reasoning
         docs/document/knowledge base/… → local_rag    reason: kw_rag

Tier 3  USE_LLM_ROUTING=true → local Gemma classifies intent → cloud or local
         → reason: llm_classifier / llm_classifier_local

Tier 4  Cloud API key missing or API error
         → route: local_fallback  reason: *_unavailable
```

---

### `src/assistant/llm/llama_cpp_runner.py` — Local Inference

Wraps the `llama-cli` binary as a subprocess. Key configuration:

| Env Var | Default | Purpose |
|---------|---------|---------|
| `MODEL_PATH` | — | Path to `.gguf` model file |
| `LLAMA_MAIN_PATH` | — | Path to `llama-cli` binary |
| `INFERENCE_THREADS` | 4 | CPU threads (Pi 5 has 4 cores) |
| `LLM_CONTEXT_TOKENS` | 2048 | Context window size |
| `MAX_RESPONSE_TOKENS` | 256 | Max tokens to generate |
| `LLM_TEMPERATURE` | 0.2 | Sampling temperature |

---

### `src/assistant/llm/cloud_router.py` — Cloud LLM Client

Routes to one of three cloud providers. Falls back to local on any API error or missing key.

| Provider | Library | Env Key | Model |
|---------|---------|---------|-------|
| Groq | `groq` | `GROQ_API_KEY` | llama-3-8b-8192 (default) |
| Gemini | `google-generativeai` | `GEMINI_API_KEY` | gemini-1.5-flash |
| Kimi | `openai` (compat) | `KIMI_API_KEY` + `KIMI_BASE_URL` | moonshot-v1-8k |

---

### `src/assistant/rag/store.py` — Vector Store

Manages document embeddings using `sentence-transformers` and an HNSW index (`hnswlib`). SQLite stores document metadata (source, chunk index, original text).

**Ingestion flow:**

```
document file (.txt/.md/.pdf)
    → chunk into segments
    → encode with sentence-transformers
    → insert vector into HNSW index
    → insert metadata into SQLite
```

**Retrieval flow:**

```
query string
    → encode with sentence-transformers
    → HNSW k-nearest-neighbour search
    → fetch metadata from SQLite
    → return top-k text chunks
```

---

### `src/assistant/memory.py` — Conversation Memory

Stores per-user conversation turns in SQLite. Table schema: `(user_id, role, content, timestamp)`. The orchestrator loads the last `MEMORY_MAX_TURNS` turns and appends them as chat history in the prompt.

---

### `src/assistant/personality.py` — Personality System

Loads agent identity from `personality.yaml` (if present) or falls back to environment variables. Exposes a `get_system_prompt()` method that is prepended to every inference call.

```yaml
# personality.yaml.example
name: Aria
persona: A helpful and knowledgeable AI assistant
tone: friendly and professional
expertise:
  - general knowledge
  - software engineering
  - raspberry pi hardware
```

---

### `src/assistant/bots/` — Bot Adapters

| Module | Mode | Description |
|--------|------|-------------|
| `telegram_polling.py` | Polling | Long-polls Telegram Bot API; parses updates |
| `discord_bot.py` | Gateway + Webhook | Discord gateway (polling) or interactions endpoint |

Bot modules use `messaging/parsers.py` to extract `(user_id, message_text)` from platform-specific payloads and `messaging/senders.py` to deliver responses.

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Single-worker Uvicorn | SQLite connections are per-thread, not process-safe |
| Subprocess llama-cli | Avoids Python binding complexity; llama.cpp CLI is stable |
| HNSW over FAISS | Lighter dependency; sufficient for Pi 5 scale |
| SQLite for memory | Zero infrastructure; sufficient for single-device deployment |
| Fallback before error | User never sees a raw exception; graceful degradation |
