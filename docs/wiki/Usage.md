# Usage

How to actually use Swarm2.0 once it's running.

---

## REST API

The FastAPI server exposes four endpoints. All are on port 8000 by default (set `PORT` in `.env` to change).

---

### `GET /health`

Returns server status, configuration summary, and cloud provider availability.

```bash
curl http://127.0.0.1:8000/health
```

**Response:**
```json
{
  "ok": true,
  "model_path": "/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf",
  "llama_main_path": "/home/pi/llama.cpp/build/bin/llama-cli",
  "use_llm_routing": true,
  "bot_mode": "polling",
  "agent_name": "Aria",
  "hybrid": {
    "groq_enabled": true,
    "gemini_enabled": false,
    "kimi_enabled": true
  }
}
```

- `ok: true` means the server is up. It does not verify that local inference actually works.
- `groq_enabled: false` means `GROQ_API_KEY` is not set or is empty.
- `agent_name` reflects the loaded personality name.

---

### `POST /query`

Main query endpoint. Accepts a message and returns a response with routing metadata.

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze the tradeoffs between SQL and NoSQL databases"}'
```

**Request body:**
```json
{
  "message": "your message here"
}
```

**Response:**
```json
{
  "route": "groq",
  "reason": "kw_reasoning",
  "response": "Great question. SQL databases offer ACID compliance..."
}
```

**Fields:**

| Field | Description |
|---|---|
| `route` | Which backend was used: `local_simple`, `local_rag`, `local_fallback`, `groq`, `gemini`, `kimi` |
| `reason` | Why that route was chosen — see table below |
| `response` | The assistant's response text |

**Route reasons:**

| `reason` | Meaning |
|---|---|
| `short_message` | Message ≤ 150 chars, no complex signals → local instantly |
| `kw_planning` | Contains: plan, roadmap, strategy, workflow, project steps |
| `kw_long_context` | Message ≥ 1200 chars |
| `kw_reasoning` | Contains: analyze, compare, tradeoff, root cause, etc. |
| `kw_rag` | Contains: docs, document, knowledge base, retrieve, etc. |
| `llm_classifier` | Local Gemma classified it → cloud |
| `llm_classifier_local` | Local Gemma classified it → local |
| `default` | No signal found, no LLM routing → local |
| `groq_unavailable` | Groq failed or no key → fell back to local |
| `gemini_unavailable` | Gemini failed or no key → fell back to local |
| `kimi_unavailable` | Kimi failed or no key → fell back to local |
| `cloud_unavailable` | Generic cloud fallback |

**Error responses:**
- `400` — empty message
- `413` — message exceeds `MAX_INPUT_CHARS` (default: 8000)

> **Pro tip:** The `reason` field is your debugging best friend. If a message is routing somewhere unexpected, the reason tells you exactly which tier made the decision and why.

---

### `POST /webhook/telegram`

Receives Telegram webhook updates. You only need this if `BOT_MODE=webhook`.

**Request:** Standard Telegram Update object (JSON).

**Optional verification header:** `X-Telegram-Bot-Api-Secret-Token` (checked against `TELEGRAM_SECRET`).

**Response:**
```json
{
  "status": "ok",
  "route": "groq",
  "reason": "kw_reasoning",
  "response": "...",
  "delivery": {"sent": true}
}
```

If `chat_id` is missing from the payload: `{"status": "ignored"}`.

Register your webhook:
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://your-domain.com/webhook/telegram" \
  -d "secret_token=your_optional_secret"
```

---

### `POST /webhook/discord`

Receives Discord webhook interactions. You only need this if `BOT_MODE=webhook`.

**Discord PING (type 1):** Automatically handled with `{"type": 1}` PONG — no user message is processed.

**Discord Interaction (type 2):** Returns `{"type": 4, "data": {"content": "..."}}` directly (avoids "Interaction Failed" in the client).

**Signature verification:** When `DISCORD_PUBLIC_KEY` is set, verifies `X-Signature-Ed25519` + `X-Signature-Timestamp` headers using Ed25519 via PyNaCl.

Set the Interactions Endpoint URL in the Discord Developer Portal to `https://your-domain.com/webhook/discord`.

---

## Bot Modes

### Polling Mode (`BOT_MODE=polling`)

Both bots start as async background tasks when the FastAPI server starts. No public URL required.

**Telegram polling:**
- Calls `getUpdates` API with a 30-second long-polling timeout
- Tracks the message offset automatically
- Works behind NAT, firewalls, and university WiFi

**Discord gateway:**
- Connects to Discord's WebSocket gateway via `discord.py`
- Requires "Message Content Intent" to be enabled in the Developer Portal
- Reconnects automatically on disconnect

**When to use:** Windows development, home networks, any setup without a public HTTPS URL.

### Webhook Mode (`BOT_MODE=webhook`)

Telegram and Discord POST events to your server. Requires a publicly reachable HTTPS URL.

**Without a public URL on Windows:**
- [ngrok](https://ngrok.com): `ngrok http 8000` gives you `https://xxxx.ngrok.io`
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/): free, permanent HTTPS tunnel

**When to use:** Production servers, always-on deployments, anywhere you have a real domain.

---

## RAG Knowledge Ingestion

Drop documents in `data/knowledge/` (`.txt`, `.md`, or `.pdf`), then run the ingestion script.

**Linux / Pi:**
```bash
source .venv/bin/activate
export PYTHONPATH=src
python scripts/ingest_documents.py data/knowledge --source knowledge_base
```

**Windows:**
```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe scripts\ingest_documents.py data\knowledge --source knowledge_base
```

**Options:**
```
--source <label>     Label for this batch (stored in metadata)
--chunk-size <N>     Words per chunk (default: 500)
```

**What happens:**
1. Documents are read and split into ~500-word chunks
2. Each chunk is embedded with `sentence-transformers/all-MiniLM-L6-v2`
3. Vectors are stored in an `hnswlib` HNSW index
4. Chunk content + metadata saved to SQLite

After ingestion, every query automatically retrieves the top-3 most relevant chunks and includes them in the prompt. Cloud models and local models both benefit.

---

## Personality Configuration

The assistant's identity is configurable. It affects every single response, on every route.

### Method 1 — YAML File (recommended)

```yaml
# personality.yaml
name: Aria
personality: friendly, witty, and deeply knowledgeable
response_style: warm and conversational, concise without being curt
humor: clever puns and light tech humour when appropriate
expertise: software engineering, artificial intelligence, creative writing
```

Copy `personality.yaml.example` → `personality.yaml` and edit. The file is loaded at startup. Restart to apply changes.

### Method 2 — Environment Variables

```env
AGENT_NAME=Aria
AGENT_PERSONALITY=friendly, witty, and deeply knowledgeable
AGENT_RESPONSE_STYLE=warm and conversational
AGENT_HUMOR=clever puns and light tech humour
AGENT_EXPERTISE=software engineering, AI, creative writing
```

The YAML file takes precedence when it exists.

---

## Conversation Memory

Memory is per-user and stored in SQLite. The `user_id` is:
- `tg:<telegram_user_id>` for Telegram messages
- `dc:<discord_user_id>` for Discord messages
- `api` for direct REST API calls

The last `MEMORY_MAX_TURNS` (default: 10) turns are prepended to every prompt. Users effectively have a continuous conversation with the assistant across multiple sessions (memory persists across server restarts).

**To clear memory for a user:** There is no API endpoint for this yet (it's on the roadmap). Clear it directly:
```python
from assistant.memory import ConversationMemory
m = ConversationMemory("data/rag")
m.clear("tg:123456789")
```

---

## Configuration Reference

All settings are read from `.env` (via `python-dotenv`).

| Variable | Default | Description |
|---|---|---|
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Bind port |
| `MODEL_PATH` | OS-dependent | Path to `.gguf` model file |
| `LLAMA_MAIN_PATH` | OS-dependent | Path to `llama-cli` binary |
| `INFERENCE_THREADS` | `nCPU-1` | Threads for llama.cpp |
| `LLM_CONTEXT_TOKENS` | `2048` | Context window size |
| `MAX_RESPONSE_TOKENS` | `256` | Max tokens in response |
| `LLM_TEMPERATURE` | `0.2` | Inference temperature |
| `LLAMA_TIMEOUT_SECONDS` | `120` | Subprocess timeout |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model |
| `RAG_TOP_K` | `3` | Chunks retrieved per query |
| `RAG_DATA_DIR` | `./data/rag` | Directory for index + SQLite |
| `MAX_INPUT_CHARS` | `8000` | Hard limit on message length |
| `EXPOSE_DELIVERY_ERRORS` | `false` | Expose raw bot errors in responses |
| `MEMORY_MAX_TURNS` | `10` | Conversation turns per user |
| `USE_LLM_ROUTING` | `true` | Use Gemma to classify ambiguous queries |
| `LOCAL_SHORT_THRESHOLD_CHARS` | `150` | Short-message threshold |
| `LONG_CONTEXT_THRESHOLD_CHARS` | `1200` | Long-message threshold (→ Gemini) |
| `CLOUD_TIMEOUT_SECONDS` | `25` | Cloud API timeout |
| `BOT_MODE` | `webhook` | `polling` or `webhook` |
| `GROQ_API_KEY` | `` | Groq API key |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq model |
| `GEMINI_API_KEY` | `` | Google Gemini API key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model |
| `KIMI_API_KEY` | `` | Moonshot Kimi API key |
| `KIMI_BASE_URL` | `https://api.moonshot.ai/v1` | Kimi endpoint |
| `KIMI_MODEL` | `moonshot-v1-8k` | Kimi model |
| `TELEGRAM_BOT_TOKEN` | `` | Telegram bot token |
| `TELEGRAM_SECRET` | `` | Webhook secret (webhook mode) |
| `DISCORD_BOT_TOKEN` | `` | Discord bot token |
| `DISCORD_PUBLIC_KEY` | `` | Discord Ed25519 public key |
| `DISCORD_BEARER_TOKEN` | `` | Legacy Discord bearer token |
| `AGENT_NAME` | `Assistant` | Agent display name |
| `AGENT_PERSONALITY` | `helpful, knowledgeable, and professional` | Character adjectives |
| `AGENT_RESPONSE_STYLE` | `concise, clear, and accurate` | Response tone |
| `AGENT_HUMOR` | `subtle and professional` | Humor style |
| `AGENT_EXPERTISE` | `general knowledge, technology, and problem-solving` | Expertise domains |
| `PERSONALITY_FILE` | `./personality.yaml` | Path to YAML personality file |
