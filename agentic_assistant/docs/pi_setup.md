# Raspberry Pi 5 (8GB) — Production Setup Guide

Full step-by-step guide to deploy the agentic assistant on **Raspberry Pi 5 (8GB) with Raspberry Pi OS (64-bit)**.

## Architecture

```
Telegram / Discord
        │
        ▼
  FastAPI webhooks  (api.py)
        │ user_id threaded through for per-user memory
        ▼
  AgentOrchestrator  (orchestrator.py)
   │
   ├─ 1. Short message (≤150 chars, no complex signal) ─► Local Gemma  (llama.cpp)
   ├─ 2. Planning / roadmap keyword ────────────────────► Kimi / Moonshot
   ├─ 2. Input > 1200 chars ───────────────────────────► Gemini
   ├─ 2. Reasoning / analyze keyword ──────────────────► Groq
   ├─ 2. RAG / doc / source keyword ───────────────────► Local Gemma + RAG context
   ├─ 3. Ambiguous → local Gemma classifies → cloud ───► GROQ / GEMINI / KIMI
   ├─ 4. Cloud failure → always falls back ────────────► Local Gemma
   │
   ├─ RAG store queried for every route (context injected into ALL prompts)
   └─ ConversationMemory (SQLite) — last 10 turns per user threaded into prompts
```

## 0) Prerequisites

Hardware and OS
- Raspberry Pi 5 (8GB)
- NVMe SSD (>= 128GB) recommended
- Active cooling + official 27W PSU
- Raspberry Pi OS (64-bit)

Access and tooling
- SSH access to the Pi
- A second machine for copying files (optional but convenient)

## 1) OS update and base packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git build-essential cmake python3-venv python3-pip
```

## 2) Project directory

```bash
sudo mkdir -p /opt/agentic-assistant
sudo chown -R $USER:$USER /opt/agentic-assistant
cd /opt/agentic-assistant
```

Copy this repository into `/opt/agentic-assistant` (via `scp`, `rsync`, or `git clone`).

## 3) Install Python deps (Pi script)

```bash
bash deploy/install_pi.sh
```

This creates a venv at `.venv` and installs dependencies.

## 4) Build llama.cpp

```bash
cd /home/pi
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

Verify the CLI exists at:
- `/home/pi/llama.cpp/build/bin/llama-cli`

## 5) Download a GGUF model

Recommended for Pi 5:
- Gemma 2 2B Q4_K_M (or similar quantized GGUF)

Example location:
- `/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf`

## 6) Configure .env

```bash
cd /opt/agentic-assistant
cp .env.example .env
chmod 600 .env
```

Edit `.env` (Linux paths only on the Pi):

```ini
# --- Local model (required) ---
MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli
INFERENCE_THREADS=4          # Pi 5 has 4 cores; use all
LLM_CONTEXT_TOKENS=2048
MAX_RESPONSE_TOKENS=256
LLM_TEMPERATURE=0.2

# --- Pi tuning (new settings) ---
LLAMA_TIMEOUT_SECONDS=120    # raise to 180 if inference times out on heavy queries
MEMORY_MAX_TURNS=10          # lower to 6 to save RAM
USE_LLM_ROUTING=true         # Gemma-based tier-3 routing (disable to save inference time)
LOCAL_SHORT_THRESHOLD_CHARS=150

# --- Cloud routing keys (optional — any subset works) ---
GROQ_API_KEY=
GEMINI_API_KEY=
KIMI_API_KEY=

# --- Messaging webhooks (optional) ---
TELEGRAM_BOT_TOKEN=
TELEGRAM_SECRET=
DISCORD_BOT_TOKEN=
DISCORD_PUBLIC_KEY=
```

## 7) Activate venv and run local server

```bash
source /opt/agentic-assistant/.venv/bin/activate
export PYTHONPATH=/opt/agentic-assistant/src
python -m assistant.agent
```

Test the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

## 8) RAG ingestion (optional but recommended)

Ingest documents for local retrieval:

```bash
source /opt/agentic-assistant/.venv/bin/activate
export PYTHONPATH=/opt/agentic-assistant/src
python /opt/agentic-assistant/scripts/ingest_documents.py /opt/agentic-assistant/docs --source knowledge_base
```

This creates embeddings in `RAG_DATA_DIR` and a SQLite metadata database.

## 9) One-command API smoke test

```bash
bash scripts/pi_start_and_check.sh
```

This starts the server in the background, checks `/health`, runs a `/query`, prints results, and shuts down.

## 10) Webhook smoke tests (Telegram / Discord)

Start the API first, then send a test HTTP request to each activated webhook:

```bash
# Telegram (replace <TOKEN> with your bot token)
curl -s -X POST http://localhost:8000/webhook/telegram \
  -H 'Content-Type: application/json' \
  -d '{"message":{"message_id":1,"from":{"id":123,"is_bot":false,"first_name":"Test"},"chat":{"id":123,"type":"private"},"date":0,"text":"hello"}}'

# Discord PING/PONG verification check (type:1 must return type:1)
curl -s -X POST http://localhost:8000/webhook/discord \
  -H 'Content-Type: application/json' \
  -d '{"type":1}'
# Expected: {"type":1}

# Discord message
curl -s -X POST http://localhost:8000/webhook/discord \
  -H 'Content-Type: application/json' \
  -d '{"type":0,"content":"hello","channel_id":"123","author":{"id":"456","username":"testuser"}}'
```

## 11) systemd service (optional)

```bash
sudo cp deploy/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
sudo systemctl enable --now agent
sudo systemctl status agent --no-pager
```

Logs:

```bash
journalctl -u agent -b --no-pager
```

## 12) Reverse proxy (optional)

```bash
sudo apt install -y nginx
sudo cp deploy/nginx-agent.conf /etc/nginx/sites-available/agent
sudo ln -sf /etc/nginx/sites-available/agent /etc/nginx/sites-enabled/agent
sudo nginx -t
sudo systemctl restart nginx
```

Add HTTPS with Certbot or your preferred TLS setup before exposing public webhooks.

## 13) Routing reference

The orchestrator applies a four-tier decision cascade for every incoming message:

| # | Trigger | Route | Provider | `reason` code |
|---|---------|-------|----------|---------------|
| 1 | Message ≤ `LOCAL_SHORT_THRESHOLD_CHARS` (default 150) and no complex signal | `local_simple` | Local Gemma | `short_message` |
| 2 | Keywords: `plan / roadmap / strategy / milestone / schedule / timeline` | `kimi` | Moonshot Kimi | `kw_planning` |
| 2 | Message length > `LONG_CONTEXT_THRESHOLD_CHARS` (default 1200) | `gemini` | Gemini Flash | `kw_long_context` |
| 2 | Keywords: `analyze / compare / reason / explain / evaluate / assess` | `groq` | Groq LLaMA | `kw_reasoning` |
| 2 | Keywords: `document / docs / source / knowledge / retrieve / reference` | `local_rag` | Local Gemma + RAG | `kw_rag` |
| 3 | Ambiguous → Gemma classifies → cloud target | `groq / gemini / kimi` | Respective | `llm_classifier` |
| 3 | Ambiguous → Gemma classifies → local | `local_simple` | Local Gemma | `llm_classifier_local` |
| 4 | Cloud key missing or API call fails | `local_fallback` | Local Gemma | `groq_unavailable` / `gemini_unavailable` / `kimi_unavailable` |

> Tier 3 runs only when `USE_LLM_ROUTING=true` (default). RAG context is **always** retrieved and injected into
> every prompt regardless of the route taken. Conversation history (last `MEMORY_MAX_TURNS` turns) is also always
> prepended.

To validate routing locally before deploying:

```bash
source /opt/agentic-assistant/.venv/bin/activate
python scripts/test_agent_end_to_end.py
```

All six cases should print `"ok": true`.

## 14) Quick checklist

- [ ] Model file exists at `MODEL_PATH`
- [ ] `LLAMA_MAIN_PATH` points to built `llama-cli` (verify with `"$LLAMA_MAIN_PATH" --version`)
- [ ] `.env` uses Linux paths only (no Windows drive letters)
- [ ] `python -m assistant.agent` starts without errors
- [ ] `/health` returns `200` with `"ok": true` and `"use_llm_routing": true`
- [ ] `/query` returns a response with a `route` and `reason` field
- [ ] `python scripts/test_agent_end_to_end.py` → all 6 cases `"ok": true`
- [ ] Telegram webhook accepts messages (check logs for `status: ok`)
- [ ] Discord webhook responds with `{"type":1}` to a `{"type":1}` PING (automatic)
- [ ] `systemctl status agent` shows `active (running)` after `systemctl enable --now agent`
- [ ] Nginx reverse proxy passes `/health` through

## 15) Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `Model not found` on startup | Wrong `MODEL_PATH` | Confirm with `ls -lh "$MODEL_PATH"` |
| `llama-cli: not found` | `LLAMA_MAIN_PATH` wrong or build failed | Run `ls /home/pi/llama.cpp/build/bin/llama-cli`; rebuild if absent |
| Inference hangs / timeout | `LLAMA_TIMEOUT_SECONDS` too low or Pi thermal throttling | Increase `LLAMA_TIMEOUT_SECONDS` to `180`; check `vcgencmd measure_temp` |
| Discord webhook registration fails (403) | Missing PING/PONG handler | Upgrade to latest `api.py` (handler already present); re-register webhook URL in Discord dev portal |
| RAG returns no results | Index not built or wrong `RAG_DATA_DIR` | Re-run `ingest_documents.py`; check that `RAG_DATA_DIR` matches `.env` |
| Cloud routes never activate | Keys missing or availability helpers return false | Check `GROQ_API_KEY` / `GEMINI_API_KEY` / `KIMI_API_KEY` in `.env`; confirm `/health` shows `groq_enabled: true` |
| `ProtectHome` blocking model reads | Old `agent.service` with `ProtectHome=true` | Ensure `deploy/agent.service` has `ProtectHome=false`; run `systemctl daemon-reload && systemctl restart agent` |
| `ModuleNotFoundError: assistant` | `PYTHONPATH` not set | Confirm `agent.service` has `Environment=PYTHONPATH=/opt/agentic-assistant/src` |
| Memory not persisting between restarts | SQLite DB not writable | `RAG_DATA_DIR/memory.sqlite3` is the memory store — ensure `RAG_DATA_DIR` is writable by the service user (check `ls -la data/rag/`) |
| High RAM usage on Pi | Large context window | Reduce `LLM_CONTEXT_TOKENS` to `1024` and `MEMORY_MAX_TURNS` to `6` |
