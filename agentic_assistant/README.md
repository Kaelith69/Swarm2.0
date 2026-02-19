# Hybrid Agentic Assistant for Raspberry Pi 5 (8GB)

Hybrid assistant with local + cloud inference:
- Local: `llama.cpp` (`gemma2b.gguf`) + local RAG (`sentence-transformers` + `hnswlib` + SQLite)
- Cloud: Groq (fast reasoning), Gemini (long context), Kimi (planning)
- FastAPI webhooks for Telegram, Discord, WhatsApp

## 1) Raspberry Pi 5 preparation

Recommended hardware:
- Raspberry Pi 5 (8GB)
- NVMe SSD (>=128GB)
- Official 27W PSU
- Active cooler

OS:
- Ubuntu Server 24.04 LTS ARM64

## 2) Install

```bash
sudo mkdir -p /opt/agentic-assistant
sudo chown -R $USER:$USER /opt/agentic-assistant
cd /opt/agentic-assistant
# copy this project here first
bash deploy/install_pi.sh
```

## 3) Configure

```bash
cp .env.example .env
```

Set at minimum in `.env`:
- `MODEL_PATH=/home/ubuntu/models/gemma2b.gguf`
- `LLAMA_MAIN_PATH=/home/ubuntu/llama.cpp/build/bin/llama-cli`

Set cloud keys for hybrid routing:
- `GROQ_API_KEY=...`
- `GEMINI_API_KEY=...`
- `KIMI_API_KEY=...`

For outbound bot replies:
- `TELEGRAM_BOT_TOKEN=<telegram bot token>`
- `DISCORD_BOT_TOKEN=<discord bot token>`
- `WHATSAPP_ACCESS_TOKEN=<meta cloud api access token>`
- `WHATSAPP_PHONE_NUMBER_ID=<meta phone number id>`

Routing logic (v2):
- simple query -> local Gemma
- RAG query -> local RAG pipeline
- complex reasoning -> Groq
- long context -> Gemini
- planning tasks -> Kimi

Pi 5 tuning defaults are already set:
- `INFERENCE_THREADS=4`
- `LLM_CONTEXT_TOKENS=2048`
- `MAX_RESPONSE_TOKENS=256`

Safety defaults:
- `MAX_INPUT_CHARS=8000` (reject oversized inputs)
- `EXPOSE_DELIVERY_ERRORS=false` (redacts verbose provider error bodies)

## 4) Ingest documents for RAG

```bash
source /opt/agentic-assistant/.venv/bin/activate
export PYTHONPATH=/opt/agentic-assistant/src
python /opt/agentic-assistant/scripts/ingest_documents.py /opt/agentic-assistant/docs --source knowledge_base
```

## 5) Run locally

```bash
source /opt/agentic-assistant/.venv/bin/activate
export PYTHONPATH=/opt/agentic-assistant/src
python -m assistant.agent
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Test query:

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message":"What can you do?"}'

The query response includes `route` and `reason` to show which model path handled the request and why.
```

## 6) Systemd service

```bash
sudo cp deploy/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
sudo systemctl enable agent
sudo systemctl start agent
sudo systemctl status agent --no-pager
```

## 7) Nginx reverse proxy

```bash
sudo cp deploy/nginx-agent.conf /etc/nginx/sites-available/agent
sudo ln -sf /etc/nginx/sites-available/agent /etc/nginx/sites-enabled/agent
sudo nginx -t
sudo systemctl restart nginx
```

## 8) Webhook endpoints

- Telegram: `POST /webhook/telegram`
- Discord: `POST /webhook/discord`
- WhatsApp verify: `GET /webhook/whatsapp`
- WhatsApp events: `POST /webhook/whatsapp`

This service receives webhook events, generates a local response, and also sends outbound replies to the same platform when the corresponding credentials are set.

## 9) Performance + stability notes for Pi 5

- Keep model quantized (`Q4_K_M`) for smooth inference.
- Store RAG files on NVMe (`RAG_DATA_DIR`).
- Keep active cooling and monitor CPU temp (`vcgencmd measure_temp`).
- Use small-to-mid embedding models for responsiveness.

Hybrid target latencies (from TDD v2):
- Local inference: 1 to 5 seconds
- Groq inference: 0.1 to 0.5 seconds
- Gemini inference: 1 to 3 seconds
- Kimi inference: 1 to 4 seconds
