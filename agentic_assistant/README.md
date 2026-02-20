# Hybrid Agentic Assistant — Windows & Raspberry Pi 5

Hybrid assistant with local + cloud inference, Discord & Telegram bots, and a configurable personality:
- Local: `llama.cpp` + local RAG (`sentence-transformers` + `hnswlib` + SQLite)
- Cloud: Groq (fast reasoning), Gemini (long context), Kimi/Moonshot (planning)
- APIs: FastAPI + Telegram/Discord webhooks **or polling bots** (recommended for Windows)
- Personality: configurable agent name, character, response style, humor, and expertise

## 1) Quick Start — Windows

```powershell
# 1. Clone / copy this repository to a local folder, e.g.:
#    C:\agentic-assistant\
cd C:\agentic-assistant

# 2. Install dependencies (creates .venv, copies .env and personality.yaml)
powershell -ExecutionPolicy Bypass -File deploy\install_windows.ps1

# 3. Edit .env — set bot tokens, cloud API keys, model path
notepad .env

# 4. (Optional) Customise the assistant's personality
notepad personality.yaml

# 5. Start the server (includes health + smoke-test)
powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1
```

See [GUIDE.md](GUIDE.md) for the full Windows setup walkthrough.

## 2) Quick Start — Raspberry Pi 5

```bash
sudo mkdir -p /opt/agentic-assistant
sudo chown -R $USER:$USER /opt/agentic-assistant
cd /opt/agentic-assistant
# copy this repo here first
bash deploy/install_pi.sh
```

## 3) Configure `.env`

```bash
cp .env.example .env
# Linux: chmod 600 .env
```

### Key settings

| Variable | Windows example | Pi/Linux example |
|---|---|---|
| `MODEL_PATH` | `C:\llama.cpp\models\gemma-2-2b-it-Q4_K_M.gguf` | `/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf` |
| `LLAMA_MAIN_PATH` | `C:\llama.cpp\build\bin\llama-cli.exe` | `/home/pi/llama.cpp/build/bin/llama-cli` |
| `BOT_MODE` | `polling` (no public URL needed) | `webhook` |
| `TELEGRAM_BOT_TOKEN` | from BotFather | same |
| `DISCORD_BOT_TOKEN` | from Discord Dev Portal | same |

> **Windows tip**: Set `BOT_MODE=polling` — bots will pull messages directly from Telegram/Discord without needing a public HTTPS URL.

## 4) Personality Configuration

Copy `personality.yaml.example` to `personality.yaml` and edit it:

```yaml
name: Aria
personality: friendly, witty, and deeply knowledgeable
response_style: warm and conversational, concise without being curt
humor: clever puns and light tech humour when appropriate
expertise: software engineering, artificial intelligence, creative writing
```

Or use environment variables in `.env`:

```env
AGENT_NAME=Aria
AGENT_PERSONALITY=friendly, witty, and deeply knowledgeable
AGENT_RESPONSE_STYLE=warm and conversational
AGENT_HUMOR=clever puns
AGENT_EXPERTISE=software engineering, AI, creative writing
```

## 5) Bot Modes

### Polling mode (`BOT_MODE=polling`) — recommended for Windows
- Telegram: polls `getUpdates` API (no public URL required)
- Discord: connects via WebSocket gateway (requires `discord.py`, included in `requirements.txt`)
- Both bots start automatically when `BOT_MODE=polling` and the tokens are set

### Webhook mode (`BOT_MODE=webhook`) — for servers with a public URL
- Telegram: `POST /webhook/telegram`
- Discord: `POST /webhook/discord` (handles PING/PONG verification automatically)
- On Windows without a public URL: use [ngrok](https://ngrok.com) or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

## 6) Where to get API keys

### Cloud inference
| Provider | URL | `.env` key |
|---|---|---|
| Groq | https://console.groq.com/keys | `GROQ_API_KEY` |
| Gemini | Google AI Studio | `GEMINI_API_KEY` |
| Kimi/Moonshot | Moonshot developer console | `KIMI_API_KEY` |

### Bots
| Bot | How | `.env` key |
|---|---|---|
| Telegram | Talk to `@BotFather` → `/newbot` | `TELEGRAM_BOT_TOKEN` |
| Discord | discord.com/developers → Bot → Create | `DISCORD_BOT_TOKEN` |

> **Discord polling mode**: Also enable **Message Content Intent** in the Discord Developer Portal (Bot → Privileged Gateway Intents).

## 7) Routing behavior — 4-tier cascade

Every message passes through a priority cascade. **RAG context and conversation history are injected into every prompt regardless of route.**

| Tier | Trigger | Route | Provider | `reason` |
|------|---------|-------|----------|----------|
| 1 | len ≤ `LOCAL_SHORT_THRESHOLD_CHARS` (150) and no complex signal | `local_simple` | Local Gemma | `short_message` |
| 2 | `plan / roadmap / strategy / workflow` keywords | `kimi` | Moonshot Kimi | `kw_planning` |
| 2 | Message length ≥ `LONG_CONTEXT_THRESHOLD_CHARS` (1200) | `gemini` | Gemini Flash | `kw_long_context` |
| 2 | `analyze / compare / tradeoff / root cause` keywords | `groq` | Groq LLaMA | `kw_reasoning` |
| 2 | `docs / document / knowledge base / retrieve` keywords | `local_rag` | Local Gemma + RAG | `kw_rag` |
| 3 | Ambiguous → local Gemma classifies → cloud | varies | Groq / Gemini / Kimi | `llm_classifier` |
| 3 | Ambiguous → local Gemma classifies → local | `local_simple` | Local Gemma | `llm_classifier_local` |
| 4 | Cloud key missing or API error | `local_fallback` | Local Gemma | `*_unavailable` |

Set `USE_LLM_ROUTING=false` for faster keyword-only routing (useful on slow hardware).

## 8) Ingest knowledge for RAG

Place your documents (`.txt`, `.md`, `.pdf`) in `data/knowledge/`, then run:

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe scripts\ingest_documents.py data\knowledge --source knowledge_base
```

**Linux / Pi:**
```bash
source .venv/bin/activate
export PYTHONPATH=src
python scripts/ingest_documents.py data/knowledge --source knowledge_base
```

## 9) Run and test

### Windows
```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1
# or:
scripts\start_windows.bat
```

### Linux / Pi
```bash
bash scripts/pi_start_and_check.sh
```

### Manual checks
```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d '{"message":"Hello, who are you?"}'
```

## 10) Service / auto-start

### Windows — Task Scheduler
```powershell
# Run once as Administrator:
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File C:\agentic-assistant\scripts\start_windows.ps1"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "AgenticAssistant" -Action $action -Trigger $trigger -RunLevel Highest
```

### Linux — systemd
```bash
sudo cp deploy/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
sudo systemctl enable --now agent
sudo systemctl status agent --no-pager
```

## 11) Performance notes

| Platform | Model | Typical latency |
|---|---|---|
| Windows (CPU, e.g. Core i7) | Local Gemma Q4_K_M | 2–15 s |
| Raspberry Pi 5 8GB | Local Gemma Q4_K_M | 4–10 s |
| Any platform | Groq (cloud) | 0.3–1 s |
| Any platform | Gemini (cloud) | 1–3 s |
| Any platform | Kimi/Moonshot (cloud) | 1–4 s |

- **Single-worker only**: Do NOT use `uvicorn --workers N` — SQLite is not safe across processes.
- On Windows, `llama.cpp` uses all available CPU threads by default (`INFERENCE_THREADS` env var).
- If only using cloud routes, you can leave `MODEL_PATH` and `LLAMA_MAIN_PATH` unset (local inference will error gracefully and fall back to cloud).
