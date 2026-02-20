# Raspberry Pi 5 (8GB) Setup Guide

This guide walks through a full, clean setup on a Raspberry Pi 5 (8GB), including local + hybrid routing, RAG ingestion, and webhook smoke tests.

## 0) Prerequisites

Hardware and OS
- Raspberry Pi 5 (8GB)
- NVMe SSD (>= 128GB) recommended
- Active cooling + official 27W PSU
- Raspberry Pi OS 64-bit (Bookworm) **or** Ubuntu Server 24.04 LTS (ARM64)

> **Note on the default user:**
> - Raspberry Pi OS uses `pi` as the default user (`/home/pi`).
> - Ubuntu Server uses `ubuntu` as the default user (`/home/ubuntu`).
> Replace `pi` with your actual username in all paths below if needed.

Access and tooling
- SSH access to the Pi
- A second machine for copying files (optional but convenient)

## 1) OS update and base packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git build-essential cmake python3-venv python3-pip \
    python3-dev libopenblas-dev pkg-config
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

This creates a venv at `.venv`, installs all Python dependencies, and builds llama.cpp automatically.

## 4) Build llama.cpp

`install_pi.sh` handles the build automatically. To rebuild manually:

```bash
cd "$HOME/llama.cpp"
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON
cmake --build build -j4
```

Verify the CLI exists at:
- `$HOME/llama.cpp/build/bin/llama-cli`

## 5) Download a GGUF model

Recommended for Pi 5:
- Gemma 2 2B Q4_K_M (or similar quantized GGUF)

Example location:
- `$HOME/models/gemma-2-2b-it-Q4_K_M.gguf`

## 6) Configure .env

```bash
cd /opt/agentic-assistant
cp .env.example .env
chmod 600 .env
```

Edit `.env` (Linux paths only on the Pi; `.env` files do not expand shell variables, use literal paths):
- `MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf`
- `LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli`
- `INFERENCE_THREADS=4`
- `LLM_CONTEXT_TOKENS=2048`
- `MAX_RESPONSE_TOKENS=256`
- `LLM_TEMPERATURE=0.2`

Optional cloud routing keys:
- `GROQ_API_KEY=...`
- `GEMINI_API_KEY=...`
- `KIMI_API_KEY=...`

Optional messaging keys:
- `TELEGRAM_BOT_TOKEN=...`
- `DISCORD_BOT_TOKEN=...`
- `WHATSAPP_ACCESS_TOKEN=...`
- `WHATSAPP_PHONE_NUMBER_ID=...`

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

## 10) Webhook smoke tests (Telegram/Discord/WhatsApp)

Start the API first, then run:

```bash
python scripts/webhook_smoke_test.py --base-url http://localhost:8000
```

If your webhook secrets are enabled, pass them to the script:

```bash
python scripts/webhook_smoke_test.py \
  --base-url http://localhost:8000 \
  --telegram-secret "$TELEGRAM_SECRET" \
  --discord-token "$DISCORD_BEARER_TOKEN" \
  --whatsapp-verify-token "$WHATSAPP_VERIFY_TOKEN"
```

## 11) systemd service (optional)

> **Note:** `deploy/agent.service` uses `User=pi`. Change this to your actual username (e.g. `ubuntu`) if needed before copying.

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

## 13) Quick checklist

- Model file exists at `MODEL_PATH`
- `LLAMA_MAIN_PATH` points to built `llama-cli`
- `.env` uses Linux paths only on the Pi
- `python -m assistant.agent` starts without errors
- `/health` and `/query` respond
- Webhook smoke tests pass

## 14) Troubleshooting

- Model not found: check `MODEL_PATH` and file permissions.
- llama.cpp not found: verify `LLAMA_MAIN_PATH`.
- RAG errors: delete `RAG_DATA_DIR` and re-run ingestion.
- Cloud routes not used: check `/health` for `groq_enabled`, `gemini_enabled`, `kimi_enabled`.
- `hnswlib` build fails: ensure `python3-dev`, `libopenblas-dev`, and `pkg-config` are installed.
