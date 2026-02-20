# Hybrid Agentic Assistant — Complete Guide

This guide explains how to develop, configure, deploy, and operate the Hybrid Agentic Assistant on a Raspberry Pi 5 (8GB). It includes hardware recommendations, software prerequisites, where to obtain credentials (API keys and tokens), where to place them, and why each choice matters.

Table of contents
- Overview
- Hardware & OS
- Project layout
- Development setup (local)
- Packaging for Raspberry Pi 5
- Installing on Raspberry Pi 5 (step-by-step)
- Path conventions (Windows vs Pi)
- Models and storage
- RAG data ingestion
- Messaging credentials: where to get them and how to place them
- Cloud credentials: where to get them and how to place them
- Configuration and tuning values (what and why)
- One-command start + smoke test
- Security best-practices
- Publishing this repository to GitHub
- Troubleshooting & debugging

---

## Overview

This project provides a hybrid assistant:
- Local path: `llama.cpp` inference + local RAG (`sentence-transformers`, `hnswlib`, SQLite).
- Cloud path: Groq, Gemini, and Kimi providers routed by query type.
- API surface: `FastAPI` with Telegram/Discord webhook handlers.

Why hybrid?
- Local handles routine tasks and RAG cheaply on-device.
- Cloud handles complex reasoning, long context, and planning.
- Fail-safe fallback to local path when cloud keys are missing or cloud calls fail.

## Hardware & OS

- Recommended device: Raspberry Pi 5 (8GB RAM) with NVMe SSD (>= 128GB).
- Power: Official 27W USB-C power supply.
- Cooling: active cooling (fan + heatsink) to sustain CPU frequency during inference.
- OS: Raspberry Pi OS (64-bit). Use Raspberry Pi Imager.

Why NVMe SSD?
- Embeddings, models, and SQLite/HNSW files can be large; NVMe reduces I/O bottlenecks.

## Project layout (important files)
- `src/assistant` — Python package with API, orchestrator, RAG store, and LLM runner.
- `scripts/ingest_documents.py` — tool to ingest PDFs/TXT/MD into the RAG store.
- `.env.example` — environment variables and configuration defaults.
- `deploy/install_pi.sh` — bootstrap script for Pi installation.
- `deploy/agent.service` — `systemd` service unit for running the assistant.
- `deploy/nginx-agent.conf` — example reverse-proxy config.
- `GUIDE.md` — this guide.

## Development setup (local machine)

1. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2. Run a local server for testing:

```bash
export PYTHONPATH=src
python -m assistant.agent
# then open http://127.0.0.1:8000/health
```

3. Unit testing & linting (optional)
- Add tests under `tests/` and run with `pytest`.

## Packaging for Raspberry Pi 5

- Copy the full repository to the Pi (via `scp`, `rsync`, or `git clone`).
- On the Pi, run `bash deploy/install_pi.sh` which creates a virtualenv and installs dependencies.

## Installing on Raspberry Pi 5 (step-by-step)

1. Flash Raspberry Pi OS (64-bit), enable SSH, and boot the Pi.
2. Update OS:

```bash
sudo apt update && sudo apt upgrade -y
```

3. Copy project to `/opt/agentic-assistant` (or clone directly):

```bash
sudo mkdir -p /opt/agentic-assistant
sudo chown -R $USER:$USER /opt/agentic-assistant
cp -r /path/to/local/agentic_assistant/* /opt/agentic-assistant/
cd /opt/agentic-assistant
bash deploy/install_pi.sh
```

4. Edit `.env` (copy `.env.example` to `.env`) and set the variables described below.
5. Place your quantized model at `MODEL_PATH` (see Models and storage).
6. Build `llama.cpp` (see below) and verify the CLI works.
7. Enable `systemd` service:

```bash
sudo cp deploy/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
sudo systemctl enable --now agent
sudo systemctl status agent -l
```

8. (Optional) Configure Nginx as a reverse proxy using `deploy/nginx-agent.conf` and restart nginx.

## Path conventions (Windows vs Pi)

- Raspberry Pi runtime must use Linux paths (example: `/home/pi/models/model.gguf`).
- Windows local runtime must use Windows paths (example: `C:\Users\name\Downloads\model.gguf`).
- Avoid mixed values. If `MODEL_PATH` is Windows but app runs on Linux, model loading fails.
- Recommended Pi values:
	- `MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf`
	- `LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli`

## Models and storage

- Models: Use a quantized GGUF model (e.g., Gemma 2 2B Q4_K_M) for smoother inference on Pi.
- Place models under the path specified by `MODEL_PATH` in `.env` (e.g., `/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf`).
- RAG storage: `RAG_DATA_DIR` holds `hnswlib` index files and a SQLite DB; place it on NVMe.

Why quantized models?
- Memory and CPU footprints are reduced drastically, enabling inference on limited hardware.

## RAG data ingestion

Use `scripts/ingest_documents.py` to ingest a directory of documents.

Example:

```bash
source /opt/agentic-assistant/.venv/bin/activate
export PYTHONPATH=/opt/agentic-assistant/src
python /opt/agentic-assistant/scripts/ingest_documents.py /opt/agentic-assistant/docs --source knowledge_base
```

This will:
- Read files (PDF, TXT, MD), chunk them into ~500-word chunks (configurable), create embeddings using the sentence-transformers model, store vectors in `hnswlib`, and metadata in SQLite.

## Messaging credentials: where to get them and where to place them

All credentials go into `.env` (copy `.env.example` → `.env`). Set file permissions to restrict access:

```bash
chmod 600 /opt/agentic-assistant/.env
```

Telegram
- What: `TELEGRAM_BOT_TOKEN` from BotFather when creating a bot.
- How to get: message `@BotFather` on Telegram → `/newbot` → follow prompts → copy the token.
- Place in `.env` as `TELEGRAM_BOT_TOKEN=123456:ABC...`.
- Optional inbound verification: set a secret token in `setWebhook` `secret_token` parameter and copy to `TELEGRAM_SECRET`.

Discord
- What: `DISCORD_BOT_TOKEN` from Discord Developer Portal.
- How to get: Create an application in https://discord.com/developers → Bot → Create Bot → copy token.
- Place in `.env` as `DISCORD_BOT_TOKEN=<token>`.
- Optional inbound verification: `DISCORD_BEARER_TOKEN` is a user-configurable token you can require in the `Authorization` header for incoming webhooks.

Where to place
- Copy `.env.example` to `.env` and fill the values. The service reads runtime settings from `.env` via `python-dotenv`.

## Cloud credentials: where to get them and where to place them

Groq
- Portal: `https://console.groq.com/keys`
- `.env`: `GROQ_API_KEY=...`
- Use for: complex reasoning route

Gemini
- Portal: Google AI Studio / Gemini API key console
- `.env`: `GEMINI_API_KEY=...`
- Use for: long-context route

Kimi (Moonshot)
- Portal: Moonshot AI developer console
- `.env`:
	- `KIMI_API_KEY=...`
	- `KIMI_BASE_URL=https://api.moonshot.ai/v1`
	- `KIMI_MODEL=moonshot-v1-8k`
- Use for: planning route

## Configuration and tuning values (what and why)

- `INFERENCE_THREADS` (default 4): number of threads for `llama.cpp` inference. Start conservative (2–4) on Pi 5 and increase if temperature and performance allow.
- `LLM_CONTEXT_TOKENS` (2048): context window used for prompt/response. Larger uses more memory and CPU.
- `MAX_RESPONSE_TOKENS` (256): max generated tokens.
- `EMBEDDING_MODEL`: sentence-transformers model; `all-MiniLM-L6-v2` is a good speed/quality balance.
- `RAG_TOP_K` (3): number of nearest neighbors to retrieve for context.

Hybrid routing variables
- `LONG_CONTEXT_THRESHOLD_CHARS` (1200): if message length exceeds this, route to Gemini.
- `GROQ_API_KEY` + `GROQ_MODEL`: used for complex reasoning requests.
- `GEMINI_API_KEY` + `GEMINI_MODEL`: used for long-context requests.
- `KIMI_API_KEY` + `KIMI_BASE_URL` + `KIMI_MODEL`: used for planning/orchestration requests.
- `CLOUD_TIMEOUT_SECONDS`: cloud request timeout.
- `MAX_INPUT_CHARS`: hard limit for inbound message size to reduce abuse and runaway costs.
- `EXPOSE_DELIVERY_ERRORS`: when `false`, webhook responses avoid exposing verbose provider error payloads.

Routing rules implemented from TDD v2
- Simple query -> Local Gemma
- RAG query -> Local RAG pipeline
- Complex reasoning -> Groq
- Long context -> Gemini
- Planning request -> Kimi

Where to get cloud API keys
- Groq: https://console.groq.com/keys
- Gemini: Google AI Studio/API key in Google AI platform
- Kimi (Moonshot): Moonshot developer console/API key; use OpenAI-compatible endpoint and model.

Tuning strategy
- If inference is slow or the Pi overheats, lower `INFERENCE_THREADS` and `LLM_CONTEXT_TOKENS` and ensure `llama.cpp` is built with optimizations.
- Keep RAG files on NVMe, and consider limiting `ef` and `M` parameters in HNSW index for lower memory usage.

## One-command start + smoke test

For Raspberry Pi deployment, run:

```bash
bash scripts/pi_start_and_check.sh
```

What it does:
- Starts `assistant.agent` in the background
- Waits until `/health` is ready
- Executes one `/query` check
- Prints responses and exits

## Security best-practices

- Do NOT commit `.env` or model files to git. `.gitignore` in this repo prevents this by default.
- Use HTTPS and a reverse proxy (Nginx) with TLS certs for external webhooks.
- Restrict inbound webhook IPs where possible.
- Keep tokens rotated and stored securely (Vault, AWS Secrets Manager) for production.

## Publishing this repository to GitHub

We provide two helper scripts:
- `scripts/publish_to_github.sh` — Bash script using `gh` (GitHub CLI) to create a repo and push.
- `scripts/publish_to_github.ps1` — PowerShell equivalent for Windows.

High-level steps:

1. Install `gh` (GitHub CLI) and authenticate: `gh auth login`.
2. Run the publish script:

```bash
bash scripts/publish_to_github.sh --repo-name agentic-assistant --private
```

The script will:
- initialize git if not already a repo
- create a new GitHub repository under your account
- push the current code and create the remote `origin`

If you prefer manual steps:

```bash
git init
git add .
git commit -m "Initial commit"
gh repo create myuser/agentic-assistant --public --source=. --push
```

## Troubleshooting & debugging

- `agent` process fails to start: check `journalctl -u agent -b` and `/var/log/nginx` for proxy errors.
- Model not found: verify `MODEL_PATH` in `.env` and file ownership/permissions.
- HNSW issues: delete `data/rag` and re-ingest if the index is corrupted.
- Cloud route not used: check `/health` to confirm `groq_enabled`, `gemini_enabled`, `kimi_enabled` are true.
- Unexpected route choice: verify your message content and `LONG_CONTEXT_THRESHOLD_CHARS` setting.

---

If you want, I can now:
- Add the `publish_to_github.sh` and PowerShell script and `.gitignore`.
- Create a small `scripts/test_webhooks.py` that sends mock payloads to the API for local verification.

Tell me which of these next steps to do and I will produce them and run validations locally.
