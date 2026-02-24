# Usage

This page covers day-to-day operation of Swarm 2.0: starting the server, sending queries, bot configuration, and advanced usage patterns.

---

## Starting the Server

### Raspberry Pi (recommended)

```bash
cd /opt/agentic-assistant/agentic_assistant
bash scripts/pi_start_and_check.sh
```

This starts the server, waits for it to be ready, runs a health check, and prints the result.

### Windows

```powershell
cd agentic_assistant
.\scripts\start_windows.ps1
```

### Manual (any platform)

```bash
cd agentic_assistant
source .venv/bin/activate          # Windows: .venv\Scripts\activate
export PYTHONPATH=$(pwd)/src       # Windows: $env:PYTHONPATH = "$(pwd)\src"
python -m assistant.agent
```

The server listens on `http://0.0.0.0:8000` by default. Override with:

```env
API_HOST=127.0.0.1
API_PORT=8080
```

---

## REST API

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

```json
{"status": "ok"}
```

---

### POST /query

The main inference endpoint.

**Request body:**

```json
{
  "message": "Your question or instruction here",
  "user_id": "optional-user-identifier"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | The user's input text |
| `user_id` | string | No | Identifies the conversation thread (defaults to `"default"`) |

**Response:**

```json
{
  "response": "The assistant's answer",
  "route": "local_simple",
  "reason": "short_message",
  "rag_used": false,
  "memory_turns": 4
}
```

| Field | Description |
|-------|-------------|
| `response` | The assistant's reply text |
| `route` | Which inference backend was used |
| `reason` | Why that route was selected |
| `rag_used` | Whether RAG context was retrieved and injected |
| `memory_turns` | Number of prior turns loaded from memory |

**Route values:**

| `route` | Backend |
|---------|---------|
| `local_simple` | Local llama.cpp |
| `local_rag` | Local llama.cpp + RAG context |
| `local_fallback` | Local llama.cpp (cloud failed) |
| `groq` | Groq API |
| `gemini` | Google Gemini API |
| `kimi` | Kimi / Moonshot API |

---

### Example curl calls

```bash
# Short conversational message → local_simple
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! How are you?", "user_id": "alice"}'

# Planning question → kimi
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a roadmap for building a REST API", "user_id": "alice"}'

# Knowledge retrieval → local_rag
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "retrieve docs about our product setup", "user_id": "alice"}'

# Deep analysis → groq
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "analyze the tradeoffs between HNSW and FAISS", "user_id": "alice"}'
```

---

## Telegram Bot

### Polling mode (Windows / local dev)

Set in `.env`:

```env
BOT_MODE=polling
TELEGRAM_BOT_TOKEN=123456:ABC...
```

The bot starts automatically when the server starts. It long-polls the Telegram Bot API and processes updates.

### Webhook mode (Pi / server with public HTTPS)

```env
BOT_MODE=webhook
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_SECRET=my-webhook-secret
```

Register the webhook with Telegram:

```bash
curl "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://yourdomain.com/webhook/telegram" \
  -d "secret_token=my-webhook-secret"
```

---

## Discord Bot

### Gateway polling mode

```env
DISCORD_BOT_TOKEN=MTI...
```

The bot connects to the Discord gateway and receives messages via the event stream.

### Interactions webhook mode

```env
DISCORD_BOT_TOKEN=MTI...
DISCORD_PUBLIC_KEY=abcdef...   # from Discord Developer Portal → General Information
```

In the Discord Developer Portal, set the **Interactions Endpoint URL** to:

```
https://yourdomain.com/webhook/discord
```

Discord will send a PING to verify the endpoint. The server responds automatically with PONG.

---

## Personality Configuration

### Using YAML (recommended)

Copy the template and customise:

```bash
cp personality.yaml.example personality.yaml
```

```yaml
name: Aria
persona: A helpful and knowledgeable AI assistant specialising in software engineering
tone: friendly and professional
expertise:
  - software engineering
  - raspberry pi
  - machine learning
response_style: concise but thorough
```

### Using environment variables

```env
AGENT_NAME=Aria
AGENT_PERSONA=A helpful AI assistant
AGENT_TONE=friendly and professional
```

The personality system prompt is prepended to every inference call, giving the model consistent identity across routes.

---

## Document Ingestion (RAG)

Add any `.txt`, `.md`, or `.pdf` files to the knowledge base:

```bash
source .venv/bin/activate
export PYTHONPATH=src

# Ingest a directory
python scripts/ingest_documents.py data/knowledge --source knowledge_base

# Ingest a single file
python scripts/ingest_documents.py myfile.pdf --source product_manual
```

The `--source` tag is stored in SQLite metadata and can be used for filtering.

To trigger RAG in a query, include keywords such as: `docs`, `document`, `knowledge base`, `retrieve`, or set `USE_LLM_ROUTING=true` for the classifier to determine this automatically.

---

## Performance Tuning

### Low-RAM configuration (< 6 GB available)

```env
LLM_CONTEXT_TOKENS=1024
MAX_RESPONSE_TOKENS=128
MEMORY_MAX_TURNS=4
```

### Disable LLM routing (fastest)

```env
USE_LLM_ROUTING=false
```

This skips Tier 3 (LLM classifier) and relies only on keyword matching. Saves one inference call per Tier-3-eligible message.

### Reduce cloud latency

```env
# Use only Groq (fastest cloud)
# Remove or leave blank GEMINI_API_KEY and KIMI_API_KEY
```

With only `GROQ_API_KEY` set, all cloud routes default to Groq.

---

## End-to-End Test

```bash
source .venv/bin/activate
export PYTHONPATH=src
python scripts/test_agent_end_to_end.py
```

The script sends a series of messages covering all tiers and prints the route and reason for each.

---

## Logging

Swarm 2.0 logs to stdout by default. In systemd mode, view logs with:

```bash
sudo journalctl -u agent -f
```

For development, run with `--log-level debug`:

```bash
uvicorn assistant.api:app --host 0.0.0.0 --port 8000 --log-level debug
```
