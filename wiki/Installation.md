# Installation

This page covers full installation on both **Raspberry Pi 5** and **Windows**. For a quick-start summary see the [README](https://github.com/Kaelith69/Swarm2.0/blob/main/README.md).

---

## Prerequisites

### Hardware (Raspberry Pi 5 — recommended)

| Component | Recommendation |
|-----------|---------------|
| Board | Raspberry Pi 5 — 8 GB |
| Storage | NVMe SSD ≥ 128 GB (via PCIe HAT) |
| Power | Official 27 W USB-C PSU |
| Cooling | Active cooler (fan + heatsink) |
| OS | Raspberry Pi OS Lite 64-bit (Bookworm) |

> **Why NVMe?** Embedding queries and SQLite writes are I/O-bound. An NVMe drive provides 5–10× the throughput of a class-10 SD card.

> **Why active cooling?** Sustained inference at Q4 uses all 4 Cortex-A76 cores. Throttling begins at 80 °C. Monitor with `vcgencmd measure_temp`.

### Hardware (Windows)

Any PC with Python 3.9+ and at least 4 GB free RAM.

### Software Requirements

| Requirement | Notes |
|-------------|-------|
| Python 3.9+ | `python3 --version` |
| llama.cpp `llama-cli` binary | See [build instructions](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#build) |
| GGUF model file | Gemma 2 2B Q4_K_M recommended (~1.6 GB) |
| Git | For cloning the repo |

---

## Raspberry Pi 5 — Full Setup

### Step 1 — Flash OS

Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to write **Raspberry Pi OS Lite 64-bit** (Bookworm) to your NVMe/SD. Enable SSH in the imager settings.

### Step 2 — System dependencies

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-venv git cmake build-essential
```

### Step 3 — Build llama.cpp

```bash
cd ~
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DLLAMA_NATIVE=ON
cmake --build build --config Release -j4
# Binary is at: ~/llama.cpp/build/bin/llama-cli
```

### Step 4 — Download model

```bash
mkdir -p ~/models
# Download Gemma 2 2B Q4_K_M from Hugging Face
# https://huggingface.co/bartowski/gemma-2-2b-it-GGUF
wget -P ~/models https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf
```

### Step 5 — Clone and install Swarm 2.0

```bash
sudo mkdir -p /opt/agentic-assistant
sudo chown -R $USER:$USER /opt/agentic-assistant
cd /opt/agentic-assistant
git clone https://github.com/Kaelith69/Swarm2.0.git .
cd agentic_assistant
bash deploy/install_pi.sh
```

The install script creates a Python virtual environment at `.venv` and installs all dependencies from `requirements.txt`.

### Step 6 — Configure `.env`

```bash
cp .env.example .env
chmod 600 .env
nano .env   # or use any editor
```

Minimum required values:

```env
MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli

# Pi-safe inference settings
INFERENCE_THREADS=4
LLM_CONTEXT_TOKENS=2048
MAX_RESPONSE_TOKENS=256
LLM_TEMPERATURE=0.2
```

### Step 7 — (Optional) API keys

Add any cloud provider keys you want to enable:

```env
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...
KIMI_API_KEY=sk-...
KIMI_BASE_URL=https://api.moonshot.ai/v1

TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_SECRET=my-secret-token

DISCORD_BOT_TOKEN=MTI...
DISCORD_PUBLIC_KEY=abcdef...
```

If no cloud keys are set the system runs in fully local mode and falls back to `local_simple` / `local_rag` for all messages.

### Step 8 — Start and verify

```bash
bash scripts/pi_start_and_check.sh
```

This script:
1. Activates the virtual environment.
2. Starts the API in the background.
3. Polls `/health` until ready.
4. Sends a test `/query`.
5. Prints the result and stops the process.

---

## Windows — Full Setup

### Step 1 — Install Python 3.9+

Download from [python.org](https://www.python.org/downloads/). Ensure "Add Python to PATH" is checked.

### Step 2 — Build llama.cpp (Windows)

```powershell
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
# Binary: build\bin\Release\llama-cli.exe
```

Or download a pre-built Windows binary from the [llama.cpp releases](https://github.com/ggerganov/llama.cpp/releases).

### Step 3 — Download model

Download `gemma-2-2b-it-Q4_K_M.gguf` from [Hugging Face](https://huggingface.co/bartowski/gemma-2-2b-it-GGUF) and place it in a known directory (e.g. `C:\models\`).

### Step 4 — Clone and install

```powershell
git clone https://github.com/Kaelith69/Swarm2.0.git
cd Swarm2.0\agentic_assistant
powershell -ExecutionPolicy Bypass -File deploy\install_windows.ps1
```

### Step 5 — Configure `.env`

```powershell
Copy-Item .env.example .env
notepad .env
```

Windows paths example:

```env
MODEL_PATH=C:\models\gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=C:\llama.cpp\build\bin\Release\llama-cli.exe
```

### Step 6 — Start

```powershell
.\scripts\start_windows.ps1
```

---

## Run as a System Service (Pi only)

```bash
sudo cp deploy/agent.service /etc/systemd/system/agent.service
# Edit the service file to match your install path if different from /opt/agentic-assistant
sudo systemctl daemon-reload
sudo systemctl enable --now agent
sudo systemctl status agent --no-pager
```

---

## Nginx Reverse Proxy (webhook mode)

Required for Telegram/Discord webhook mode (HTTPS endpoint needed):

```bash
sudo apt-get install -y nginx
sudo cp deploy/nginx-agent.conf /etc/nginx/sites-available/agent
sudo ln -sf /etc/nginx/sites-available/agent /etc/nginx/sites-enabled/agent
sudo nginx -t
sudo systemctl restart nginx
```

Edit `nginx-agent.conf` to set your domain name and SSL certificate paths. Use [Certbot](https://certbot.eff.org/) for free Let's Encrypt certificates.

---

## Ingest Documents into RAG

Place your documents (`.txt`, `.md`, `.pdf`) in `data/knowledge/` or any directory, then:

```bash
source .venv/bin/activate
export PYTHONPATH=src
python scripts/ingest_documents.py data/knowledge --source knowledge_base
```

Re-run whenever you add new documents.

---

## API Keys Reference

| Service | Where to create | Env var |
|---------|----------------|---------|
| Groq | https://console.groq.com/keys | `GROQ_API_KEY` |
| Gemini | https://aistudio.google.com/ | `GEMINI_API_KEY` |
| Kimi | https://platform.moonshot.ai/ | `KIMI_API_KEY` |
| Telegram | `@BotFather` → `/newbot` | `TELEGRAM_BOT_TOKEN` |
| Discord | https://discord.com/developers/applications | `DISCORD_BOT_TOKEN` + `DISCORD_PUBLIC_KEY` |

---

## Troubleshooting

See the [Troubleshooting](Troubleshooting) wiki page for common issues and solutions.
