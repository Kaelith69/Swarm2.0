# Hybrid Agentic Assistant — Complete Guide (Windows & Raspberry Pi 5)

This guide covers how to develop, configure, deploy, and operate the Hybrid Agentic Assistant on **Windows** and **Raspberry Pi 5**. It includes hardware recommendations, software prerequisites, credentials, personality customisation, and troubleshooting.

Table of contents
- Overview
- Architecture
- Windows Setup (Quick Start)
- Raspberry Pi 5 Setup
- Path conventions (Windows vs Linux)
- Configuration reference
- Personality configuration
- Bot modes: polling vs webhook
- Discord and Telegram setup
- Cloud credentials
- RAG knowledge ingestion
- Running the server
- Service / auto-start
- Nginx reverse proxy (Linux)
- Security best-practices
- Troubleshooting & debugging
- Publishing to GitHub

---

## Overview

This project provides a hybrid AI assistant:
- **Local path**: `llama.cpp` inference + local RAG (`sentence-transformers`, `hnswlib`, SQLite).
- **Cloud path**: Groq, Gemini, and Kimi providers routed automatically by query type.
- **Bots**: Telegram and Discord — polling mode (no public URL needed) or webhook mode.
- **Personality**: configurable agent name, character, response style, humor, and expertise.

Why hybrid?
- Local handles routine tasks and RAG cheaply on-device.
- Cloud handles complex reasoning, long context, and planning.
- Fail-safe fallback to local when cloud keys are missing or API calls fail.

---

## Architecture

```
User Message
     │
     ▼
Discord Bot / Telegram Bot   (polling or webhook)
     │
     ▼
FastAPI Server  (port 8000)
     │
     ▼
AgentOrchestrator
  ├─ RAG context retrieval (sentence-transformers + hnswlib + SQLite)
  ├─ Conversation memory  (SQLite per user_id)
  ├─ Routing decision     (short-circuit / keyword / LLM classifier)
  │
  ├─ LOCAL  → LlamaCppRunner  (llama-cli subprocess)
  ├─ GROQ   → Groq API       (complex reasoning)
  ├─ GEMINI → Gemini API     (long context)
  └─ KIMI   → Kimi/Moonshot  (planning)
     │
     ▼
Response → Bot sends reply to user
```

Single-worker constraint: SQLite stores (memory, RAG index) are not safe across processes.
**Do NOT run with `uvicorn --workers N`.**

---

## Windows Setup (Quick Start)

### Prerequisites
- Windows 10 or Windows 11 (64-bit)
- Python 3.10 or later — download from https://python.org (tick "Add to PATH")
- (Optional) `llama.cpp` binary for local inference — see build instructions below
- At least one cloud API key (Groq / Gemini / Kimi) OR a local model

### Step 1 — Get the code
Download or clone this repository to a local folder, for example `C:\agentic-assistant\`.

```powershell
# Or copy manually to C:\agentic-assistant\
git clone <repo-url> C:\agentic-assistant
cd C:\agentic-assistant
```

### Step 2 — Run the installer
```powershell
powershell -ExecutionPolicy Bypass -File deploy\install_windows.ps1
```

This creates `.venv\`, installs all dependencies, copies `.env.example` → `.env`, and copies `personality.yaml.example` → `personality.yaml`.

### Step 3 — Configure `.env`
```powershell
notepad .env
```

Minimum required values (cloud-only, no local model):
```env
BOT_MODE=polling
GROQ_API_KEY=your_groq_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token
DISCORD_BOT_TOKEN=your_discord_token
```

With a local model:
```env
MODEL_PATH=C:\llama.cpp\models\gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=C:\llama.cpp\build\bin\llama-cli.exe
```

### Step 4 — (Optional) Build llama.cpp on Windows

Requirements: Visual Studio Build Tools (C++ workload) and CMake.

```powershell
git clone https://github.com/ggerganov/llama.cpp C:\llama.cpp
cd C:\llama.cpp
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j4
# Binary: C:\llama.cpp\build\bin\Release\llama-cli.exe
```

Download a quantized model (e.g., `gemma-2-2b-it-Q4_K_M.gguf`) from Hugging Face and place it at `MODEL_PATH`.

### Step 5 — (Optional) Customise personality
```powershell
notepad personality.yaml
```

See [Personality configuration](#personality-configuration) below.

### Step 6 — Start the server
```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1
```

Or using the batch file:
```
scripts\start_windows.bat
```

The startup script:
1. Starts the FastAPI server in the background.
2. Polls `/health` until the server is ready (up to 30 s).
3. Runs a `/query` smoke test.
4. Prints the server PID so you can stop it later.

---

## Raspberry Pi 5 Setup

### Hardware
- Raspberry Pi 5 (8 GB RAM)
- NVMe SSD (≥ 128 GB) via PCIe HAT — reduces I/O bottlenecks for model and RAG files
- Official 27 W USB-C PSU — required for stable operation
- Active cooling (fan + heatsink) — prevents thermal throttling during inference

### Step 1 — Install OS
Flash Raspberry Pi OS (64-bit) using Raspberry Pi Imager.  Enable SSH.

### Step 2 — Install
```bash
sudo mkdir -p /opt/agentic-assistant
sudo chown -R $USER:$USER /opt/agentic-assistant
cp -r /path/to/agentic_assistant/* /opt/agentic-assistant/
cd /opt/agentic-assistant
bash deploy/install_pi.sh
```

`install_pi.sh` installs system packages, creates a venv, installs Python deps, and builds `llama.cpp`.

### Step 3 — Configure
```bash
cp .env.example .env
chmod 600 .env
nano .env
```

### Step 4 — Start
```bash
bash scripts/pi_start_and_check.sh
```

---

## Path conventions (Windows vs Linux)

| Setting | Windows example | Linux / Pi example |
|---|---|---|
| `MODEL_PATH` | `C:\llama.cpp\models\gemma-2-2b-it-Q4_K_M.gguf` | `/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf` |
| `LLAMA_MAIN_PATH` | `C:\llama.cpp\build\bin\llama-cli.exe` | `/home/pi/llama.cpp/build/bin/llama-cli` |
| `RAG_DATA_DIR` | `C:\agentic-assistant\data\rag` | `./data/rag` |
| `PERSONALITY_FILE` | `C:\agentic-assistant\personality.yaml` | `./personality.yaml` |

**Important**: Do not mix Windows and Linux paths in the same `.env` file.  The application auto-detects the OS and sets sensible defaults, but the paths you set in `.env` must match the OS you run on.

---

## Configuration reference

All settings are read from `.env` (loaded by `python-dotenv`).

| Variable | Default | Description |
|---|---|---|
| `HOST` | `0.0.0.0` | Bind address for the FastAPI server |
| `PORT` | `8000` | Bind port |
| `MODEL_PATH` | OS-dependent | Path to the GGUF model file |
| `LLAMA_MAIN_PATH` | OS-dependent | Path to `llama-cli` / `llama-cli.exe` |
| `INFERENCE_THREADS` | `nCPU-1` | Threads for llama.cpp inference |
| `LLM_CONTEXT_TOKENS` | `2048` | Context window size |
| `MAX_RESPONSE_TOKENS` | `256` | Max tokens in generated response |
| `LLM_TEMPERATURE` | `0.2` | Inference temperature (0 = deterministic) |
| `LLAMA_TIMEOUT_SECONDS` | `120` | Subprocess timeout |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model for RAG |
| `RAG_TOP_K` | `3` | Number of RAG chunks to retrieve |
| `RAG_DATA_DIR` | `./data/rag` | Directory for RAG index + SQLite files |
| `MAX_INPUT_CHARS` | `8000` | Hard limit on incoming message length |
| `EXPOSE_DELIVERY_ERRORS` | `false` | Expose bot delivery errors in responses |
| `MEMORY_MAX_TURNS` | `10` | Conversation turns kept per user |
| `USE_LLM_ROUTING` | `true` | Use local LLM to classify ambiguous queries |
| `LOCAL_SHORT_THRESHOLD_CHARS` | `150` | Short-message threshold (→ local, no routing) |
| `LONG_CONTEXT_THRESHOLD_CHARS` | `1200` | Long-message threshold (→ Gemini) |
| `CLOUD_TIMEOUT_SECONDS` | `25` | Cloud API request timeout |
| `BOT_MODE` | `webhook` | `polling` or `webhook` |
| `GROQ_API_KEY` | `` | Groq API key |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq model name |
| `GEMINI_API_KEY` | `` | Google Gemini API key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model name |
| `KIMI_API_KEY` | `` | Moonshot Kimi API key |
| `KIMI_BASE_URL` | `https://api.moonshot.ai/v1` | Kimi endpoint |
| `KIMI_MODEL` | `moonshot-v1-8k` | Kimi model name |
| `TELEGRAM_BOT_TOKEN` | `` | Telegram bot token from BotFather |
| `TELEGRAM_SECRET` | `` | Webhook secret token (webhook mode only) |
| `DISCORD_BOT_TOKEN` | `` | Discord bot token |
| `DISCORD_PUBLIC_KEY` | `` | Discord app public key (webhook/interactions) |
| `DISCORD_BEARER_TOKEN` | `` | Legacy bearer token (webhook mode only) |
| `AGENT_NAME` | `Assistant` | Display name for the assistant |
| `AGENT_PERSONALITY` | `helpful, knowledgeable, and professional` | Character adjectives |
| `AGENT_RESPONSE_STYLE` | `concise, clear, and accurate` | Response tone guidance |
| `AGENT_HUMOR` | `subtle and professional` | Humor style |
| `AGENT_EXPERTISE` | `general knowledge, technology, and problem-solving` | Expertise domains |
| `PERSONALITY_FILE` | `./personality.yaml` | Path to optional YAML personality config |

---

## Personality configuration

The assistant's identity and communication style are fully configurable.

### Method 1 — YAML file (recommended)

Copy `personality.yaml.example` to `personality.yaml` and edit:

```yaml
name: Aria
personality: friendly, witty, and deeply knowledgeable
response_style: warm and conversational, concise without being curt
humor: clever puns and light tech humour when appropriate
expertise: software engineering, artificial intelligence, creative writing
```

The YAML file is loaded at startup.  Edit it and restart to apply changes.

### Method 2 — Environment variables

Set these in `.env`:

```env
AGENT_NAME=Aria
AGENT_PERSONALITY=friendly, witty, and deeply knowledgeable
AGENT_RESPONSE_STYLE=warm and conversational
AGENT_HUMOR=clever puns and light tech humour
AGENT_EXPERTISE=software engineering, AI, creative writing
```

**Priority**: YAML file values override environment variables when the file exists.

### What personality affects

The personality block is injected as a system instruction into every prompt — both local and cloud routes — so all responses will reflect the configured identity.

---

## Bot modes: polling vs webhook

### Polling mode (`BOT_MODE=polling`) — recommended for Windows

Both bots start automatically as async background tasks within the FastAPI server process.

**Telegram polling**: Calls the `getUpdates` API with long-polling (30-second timeout). No public URL required. Works behind NAT/firewalls.

**Discord gateway**: Connects to Discord's WebSocket gateway via `discord.py`.  No public URL required.  Requires `MESSAGE CONTENT INTENT` to be enabled (see Discord setup below).

### Webhook mode (`BOT_MODE=webhook`)

Telegram and Discord POST events to your server.  Requires a publicly reachable HTTPS URL.

**On Windows without a public URL**, use:
- [ngrok](https://ngrok.com): `ngrok http 8000` → gives you `https://xxxx.ngrok.io`
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/): free, permanent HTTPS tunnel

Register the webhook:
```bash
# Telegram
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://your-domain.com/webhook/telegram"

# Discord: set the Interactions Endpoint URL in the Developer Portal
# to https://your-domain.com/webhook/discord
```

---

## Discord and Telegram setup

### Telegram

1. Message `@BotFather` on Telegram → `/newbot` → follow prompts.
2. Copy the token and add to `.env` as `TELEGRAM_BOT_TOKEN=<token>`.
3. If using `BOT_MODE=polling`, no further setup needed — the bot starts automatically.
4. If using `BOT_MODE=webhook`, register the webhook URL (see above).

### Discord

1. Go to https://discord.com/developers/applications → "New Application".
2. Navigate to **Bot** → **Create a Bot** → copy the token → add to `.env` as `DISCORD_BOT_TOKEN=<token>`.
3. Under **Bot → Privileged Gateway Intents**, enable:
   - **Message Content Intent** (required for polling mode to read messages)
4. Under **OAuth2 → URL Generator**, select scopes `bot` with permissions:
   - `Send Messages`, `Read Message History`, `View Channels`
5. Use the generated URL to invite the bot to your server.
6. **Webhook mode only**: Copy the **Public Key** from "General Information" → add to `.env` as `DISCORD_PUBLIC_KEY=<key>`.

---

## Cloud credentials

### Groq (fast reasoning)
- Portal: https://console.groq.com/keys
- `.env`: `GROQ_API_KEY=...`
- Used when the message contains reasoning keywords or the LLM classifier routes to Groq.

### Gemini (long context)
- Portal: Google AI Studio → https://aistudio.google.com/app/apikey
- `.env`: `GEMINI_API_KEY=...`
- Used for long messages (> `LONG_CONTEXT_THRESHOLD_CHARS` characters).

### Kimi / Moonshot (planning)
- Portal: Moonshot AI developer console
- `.env`: `KIMI_API_KEY=...`, `KIMI_BASE_URL=https://api.moonshot.ai/v1`
- Used when the message contains planning/workflow keywords.

---

## RAG knowledge ingestion

Place documents (`.txt`, `.md`, `.pdf`) in `data/knowledge/`, then run the ingest script.

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts\ingest_documents.py data\knowledge --source knowledge_base
```

**Linux / Pi:**
```bash
source .venv/bin/activate
export PYTHONPATH=src
python scripts/ingest_documents.py data/knowledge --source knowledge_base
```

This reads files, splits them into ~500-word chunks, creates embeddings, stores vectors in `hnswlib`, and saves metadata in SQLite.  The RAG store is queried on every message to provide relevant context.

Options:
- `--source <label>` — label for this batch of documents
- `--chunk-size <N>` — words per chunk (default 500)

---

## Running the server

### Windows — PowerShell script
```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1
```

### Windows — Batch file
```
scripts\start_windows.bat
```

### Windows — Manual
```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m assistant.agent
```

### Linux / Pi — Shell script
```bash
bash scripts/pi_start_and_check.sh
```

### Linux / Pi — Manual
```bash
source .venv/bin/activate
export PYTHONPATH=src
python -m assistant.agent
```

---

## Service / auto-start

### Windows — Task Scheduler

Run the following once from an **Administrator** PowerShell prompt:

```powershell
$action  = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File C:\agentic-assistant\scripts\start_windows.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask `
    -TaskName "AgenticAssistant" `
    -Action $action `
    -Trigger $trigger `
    -RunLevel Highest `
    -Force
```

### Linux — systemd

```bash
sudo cp deploy/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
sudo systemctl enable --now agent
sudo systemctl status agent -l
```

---

## Nginx reverse proxy (Linux)

```bash
sudo cp deploy/nginx-agent.conf /etc/nginx/sites-available/agent
sudo ln -sf /etc/nginx/sites-available/agent /etc/nginx/sites-enabled/agent
sudo nginx -t
sudo systemctl restart nginx
```

---

## Security best-practices

- **Never commit `.env`** or model files to git.  `.gitignore` prevents this by default.
- On Linux: `chmod 600 .env` to restrict read access.
- On Windows: set NTFS permissions on `.env` so only your user can read it.
- Use HTTPS for all webhook endpoints (ngrok / Cloudflare Tunnel / nginx with TLS).
- Rotate bot tokens and API keys regularly.
- `EXPOSE_DELIVERY_ERRORS=false` (default) — prevents raw provider error payloads leaking through webhook responses.
- Set `MAX_INPUT_CHARS` to a reasonable value to prevent abuse and runaway cloud costs.

---

## Troubleshooting & debugging

### Server won't start
- Check the log file: `%TEMP%\agentic-assistant.log` (Windows) or `/tmp/agentic-assistant.log` (Linux).
- Verify `MODEL_PATH` and `LLAMA_MAIN_PATH` exist (or leave them blank for cloud-only mode).
- On Windows: check `PYTHONPATH` is set to the `src\` directory.

### Bots not responding
- **Polling mode**: Check that `TELEGRAM_BOT_TOKEN` / `DISCORD_BOT_TOKEN` are set.
- **Discord polling**: Verify "Message Content Intent" is enabled in the Developer Portal.
- **Webhook mode**: Verify your webhook URL is registered and the server is reachable from the internet.
- Check `/health` response: `curl http://127.0.0.1:8000/health` — confirms bot mode and cloud availability.

### Cloud routes not working
- Run `/health` and check `groq_enabled`, `gemini_enabled`, `kimi_enabled` — all must be `true` for the cloud key to be active.
- Check for typos or trailing spaces in API keys in `.env`.

### HNSW index corrupted
```bash
# Linux / Pi:
rm -rf data/rag && python scripts/ingest_documents.py data/knowledge --source knowledge_base
# Windows:
Remove-Item -Recurse -Force data\rag; .\.venv\Scripts\python.exe scripts\ingest_documents.py data\knowledge --source knowledge_base
```

### Unexpected routing
- The `/query` endpoint returns `route` and `reason` fields — check these to understand which path was taken.
- Use `USE_LLM_ROUTING=false` for fully deterministic keyword-only routing.

### Performance (Pi 5)
- Monitor temperature: `vcgencmd measure_temp` (throttling begins at 80 °C).
- Lower `LLM_CONTEXT_TOKENS=1024` and `MEMORY_MAX_TURNS=6` if RAM is tight.
- Place `RAG_DATA_DIR` on NVMe, not SD card.

---

## Publishing to GitHub

Two helper scripts are provided:

**Linux / macOS:**
```bash
bash scripts/publish_to_github.sh --repo-name agentic-assistant --private
```

**Windows (PowerShell):**
```powershell
.\scripts\publish_to_github.ps1 -RepoName agentic-assistant -Private
```

Both require the [GitHub CLI](https://cli.github.com/) (`gh`) to be installed and authenticated (`gh auth login`).
