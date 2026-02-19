# Hybrid Agentic Assistant for Raspberry Pi 5 (8GB)

Hybrid assistant with local + cloud inference:
- Local: `llama.cpp` + local RAG (`sentence-transformers` + `hnswlib` + SQLite)
- Cloud: Groq (fast reasoning), Gemini (long context), Kimi/Moonshot (planning)
- APIs: FastAPI + Telegram/Discord/WhatsApp webhooks

## 1) Hardware and OS

Recommended:
- Raspberry Pi 5 (8GB)
- NVMe SSD (>= 128GB)
- Official 27W PSU
- Active cooling
- Ubuntu Server 24.04 LTS ARM64

Why:
- NVMe improves model/RAG I/O
- cooling avoids thermal throttling during inference

## 2) Install on Raspberry Pi

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
chmod 600 .env
```

### Path rules (important)
- On Raspberry Pi/Linux, use Linux paths like `/home/ubuntu/...`
- On Windows local testing, use Windows paths like `C:\Users\...`
- Do not mix Windows and Linux paths in the same runtime

Minimum local runtime values:
- `MODEL_PATH=/home/ubuntu/models/gemma-2-2b-it-Q4_K_M.gguf`
- `LLAMA_MAIN_PATH=/home/ubuntu/llama.cpp/build/bin/llama-cli`

Pi-safe defaults:
- `INFERENCE_THREADS=4`
- `LLM_CONTEXT_TOKENS=2048`
- `MAX_RESPONSE_TOKENS=256`
- `LLM_TEMPERATURE=0.2`

Safety defaults:
- `MAX_INPUT_CHARS=8000`
- `EXPOSE_DELIVERY_ERRORS=false`

## 4) Where to get API keys

### Groq
- Create key: `https://console.groq.com/keys`
- Put in `.env`: `GROQ_API_KEY=...`

### Gemini (Google)
- Create key in Google AI Studio / Gemini API console
- Put in `.env`: `GEMINI_API_KEY=...`

### Kimi (Moonshot)
- Create key in Moonshot developer console
- Put in `.env`: `KIMI_API_KEY=...`
- Keep base URL: `KIMI_BASE_URL=https://api.moonshot.ai/v1`

### Telegram
- Talk to `@BotFather` → `/newbot` → copy token
- Put in `.env`: `TELEGRAM_BOT_TOKEN=...`
- Optional inbound verification token: `TELEGRAM_SECRET=...`

### Discord
- `https://discord.com/developers/applications` → create app/bot → copy token
- Put in `.env`: `DISCORD_BOT_TOKEN=...`
- Optional inbound bearer check: `DISCORD_BEARER_TOKEN=...`

### WhatsApp Cloud API (Meta)
- Create app in Meta for Developers → WhatsApp product
- Get token + phone number id
- Put in `.env`:
  - `WHATSAPP_ACCESS_TOKEN=...`
  - `WHATSAPP_PHONE_NUMBER_ID=...`
  - `WHATSAPP_VERIFY_TOKEN=...` (your chosen verify token)

## 5) Routing behavior

- simple query → local model
- RAG query (docs/source/context intent) → local RAG
- complex reasoning → Groq
- long context (length threshold) → Gemini
- planning/roadmap/workflow intent → Kimi
- cloud failure/missing key → local fallback

`/query` returns `route` and `reason` for explainability.

## 6) Ingest knowledge for RAG

```bash
source /opt/agentic-assistant/.venv/bin/activate
export PYTHONPATH=/opt/agentic-assistant/src
python /opt/agentic-assistant/scripts/ingest_documents.py /opt/agentic-assistant/docs --source knowledge_base
```

## 7) Run and test

### Standard run
```bash
source /opt/agentic-assistant/.venv/bin/activate
export PYTHONPATH=/opt/agentic-assistant/src
python -m assistant.agent
```

### One-command run + check (Pi)
```bash
bash scripts/pi_start_and_check.sh
```

This starts the API in the background, checks `/health`, runs one `/query`, prints results, and stops the process.

### Manual checks
```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d '{"message":"Who is Sayanth?"}'
```

## 8) Service and proxy

```bash
sudo cp deploy/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
sudo systemctl enable --now agent
sudo systemctl status agent --no-pager
```

```bash
sudo cp deploy/nginx-agent.conf /etc/nginx/sites-available/agent
sudo ln -sf /etc/nginx/sites-available/agent /etc/nginx/sites-enabled/agent
sudo nginx -t
sudo systemctl restart nginx
```

## 9) Webhook endpoints

- Telegram: `POST /webhook/telegram`
- Discord: `POST /webhook/discord`
- WhatsApp verify: `GET /webhook/whatsapp`
- WhatsApp events: `POST /webhook/whatsapp`

## 10) Performance notes for Pi 5

- Keep model quantized (`Q4_K_M`)
- Keep `INFERENCE_THREADS=4` initially
- Keep RAG storage on NVMe (`RAG_DATA_DIR`)
- Monitor temperature with `vcgencmd measure_temp`

Target latency bands (from TDD v2):
- Local: 1–5s
- Groq: 0.1–0.5s
- Gemini: 1–3s
- Kimi: 1–4s
