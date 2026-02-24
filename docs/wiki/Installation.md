# Installation

Complete setup instructions for Raspberry Pi 5 and Windows. Pick your platform and follow along.

---

## Prerequisites (All Platforms)

- **Python 3.10 or later**
- At least **one of**:
  - A local model + `llama.cpp` binary (for on-device inference)
  - A cloud API key (Groq, Gemini, or Kimi) (for cloud-only mode)
- At least **one of**:
  - Telegram bot token (from `@BotFather`)
  - Discord bot token (from the Developer Portal)
  - Neither — you can use the REST API directly without any bot

---

## 🥧 Raspberry Pi 5 Setup

### Hardware Recommendations

| Component | Recommendation | Why |
|---|---|---|
| Pi model | Pi 5 (8 GB) | Needs 2+ GB free for the model + Python overhead |
| Storage | NVMe SSD ≥ 128 GB via PCIe HAT | Model load and RAG queries are I/O-bound |
| Power supply | Official 27 W USB-C PSU | Under-voltage causes random crashes during inference |
| Cooling | Active fan + heatsink | Thermal throttling begins at 80 °C; inference pushes temps |

### Step 1 — Flash OS

Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash **Raspberry Pi OS Lite (64-bit)** or the full desktop version. Enable SSH in the imager settings (Ctrl+Shift+X).

### Step 2 — Copy the Repository

```bash
sudo mkdir -p /opt/agentic-assistant
sudo chown -R $USER:$USER /opt/agentic-assistant
# Copy or clone the agentic_assistant/ directory contents to /opt/agentic-assistant
# e.g. from another machine:
rsync -av ./agentic_assistant/ pi@<pi-ip>:/opt/agentic-assistant/
```

### Step 3 — Run the Installer

```bash
cd /opt/agentic-assistant
bash deploy/install_pi.sh
```

This script:
1. Installs system packages (`git`, `cmake`, `build-essential`, `python3-venv`, etc.)
2. Builds `llama.cpp` from source
3. Creates a Python virtual environment at `.venv/`
4. Installs all Python dependencies from `requirements.txt`

### Step 4 — Get a Model

Download a quantized Gemma 2 2B GGUF model from Hugging Face:

```bash
# Example — adjust URL for the actual HuggingFace model page
wget -O /home/pi/models/gemma-2-2b-it-Q4_K_M.gguf \
  "https://huggingface.co/...gemma-2-2b-it-Q4_K_M.gguf"
```

The Q4_K_M quantization is ~1.6 GB RAM at runtime. This is the recommended balance of quality vs. memory on an 8 GB Pi.

### Step 5 — Configure

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Minimum required for local + Telegram:
```env
MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli
BOT_MODE=webhook
TELEGRAM_BOT_TOKEN=your_token_here
```

Pi 5 recommended performance settings:
```env
INFERENCE_THREADS=4
LLM_CONTEXT_TOKENS=2048
MAX_RESPONSE_TOKENS=256
LLM_TEMPERATURE=0.2
RAG_DATA_DIR=/opt/agentic-assistant/data/rag
```

### Step 6 — Start

```bash
bash scripts/pi_start_and_check.sh
```

This starts the server, polls `/health` until ready (up to 30 seconds), runs a `/query` smoke test, and prints the results.

### Step 7 — Run as a Service

```bash
sudo cp deploy/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
sudo systemctl enable --now agent
sudo systemctl status agent --no-pager
```

### Step 8 — (Optional) Nginx Reverse Proxy

```bash
sudo apt install nginx
sudo cp deploy/nginx-agent.conf /etc/nginx/sites-available/agent
sudo ln -sf /etc/nginx/sites-available/agent /etc/nginx/sites-enabled/agent
sudo nginx -t && sudo systemctl restart nginx
```

---

## 🪟 Windows Setup

### Prerequisites

- Windows 10 or 11 (64-bit)
- Python 3.10+ from [python.org](https://python.org) — check "Add to PATH" during install
- (Optional) Visual Studio Build Tools (C++ workload) + CMake if building `llama.cpp`

### Step 1 — Get the Code

```powershell
# Option A: Clone
git clone https://github.com/Kaelith69/Swarm2.0 C:\agentic-assistant
cd C:\agentic-assistant\agentic_assistant

# Option B: Download ZIP and extract to C:\agentic-assistant
```

### Step 2 — Run the Installer

```powershell
cd C:\agentic-assistant
powershell -ExecutionPolicy Bypass -File deploy\install_windows.ps1
```

This creates `.venv\`, installs dependencies, copies `.env.example` → `.env`, and copies `personality.yaml.example` → `personality.yaml`.

### Step 3 — (Optional) Build llama.cpp on Windows

Requirements: Visual Studio Build Tools (C++ workload) and CMake.

```powershell
git clone https://github.com/ggerganov/llama.cpp C:\llama.cpp
cd C:\llama.cpp
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j4
# Binary will be at: C:\llama.cpp\build\bin\Release\llama-cli.exe
```

Download a model (e.g. `gemma-2-2b-it-Q4_K_M.gguf`) from Hugging Face and place it anywhere, then set `MODEL_PATH` in `.env`.

### Step 4 — Configure

```powershell
notepad .env
```

Minimum for cloud-only + polling bots:
```env
BOT_MODE=polling
GROQ_API_KEY=your_groq_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token
DISCORD_BOT_TOKEN=your_discord_token
```

With local model on Windows:
```env
MODEL_PATH=C:\llama.cpp\models\gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=C:\llama.cpp\build\bin\Release\llama-cli.exe
```

> **Path tip:** Use Windows paths (`C:\...`) on Windows. The app auto-detects the OS. Don't mix path formats.

### Step 5 — (Optional) Customise Personality

```powershell
notepad personality.yaml
```

### Step 6 — Start

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1
# or:
scripts\start_windows.bat
```

### Step 7 — Run at Startup (Task Scheduler)

Run once from an Administrator PowerShell:

```powershell
$action  = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File C:\agentic-assistant\scripts\start_windows.ps1"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask `
    -TaskName "AgenticAssistant" `
    -Action $action `
    -Trigger $trigger `
    -RunLevel Highest `
    -Force
```

---

## Getting API Keys

### Groq

1. Create an account at [console.groq.com](https://console.groq.com)
2. Go to **API Keys** → **Create API Key**
3. Set in `.env`: `GROQ_API_KEY=your_key`
4. Default model: `llama-3.1-8b-instant` (override with `GROQ_MODEL`)

### Gemini (Google)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Set in `.env`: `GEMINI_API_KEY=your_key`
4. Default model: `gemini-1.5-flash` (override with `GEMINI_MODEL`)

### Kimi / Moonshot

1. Register at the [Moonshot developer console](https://platform.moonshot.cn)
2. Create an API key
3. Set in `.env`:
   ```env
   KIMI_API_KEY=your_key
   KIMI_BASE_URL=https://api.moonshot.ai/v1
   ```
4. Default model: `moonshot-v1-8k` (override with `KIMI_MODEL`)

### Telegram

1. Message `@BotFather` on Telegram
2. Send `/newbot` → follow prompts → copy the token
3. Set in `.env`: `TELEGRAM_BOT_TOKEN=your_token`
4. For webhook mode: optionally set `TELEGRAM_SECRET` for request verification

### Discord

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. **New Application** → **Bot** → **Create a Bot** → **Reset Token** → copy
3. Set in `.env`: `DISCORD_BOT_TOKEN=your_token`
4. Under **Bot → Privileged Gateway Intents**, enable **Message Content Intent** (required for polling mode)
5. Under **OAuth2 → URL Generator**, select `bot` scope with `Send Messages`, `Read Message History`, `View Channels`
6. Use the generated URL to invite the bot to your server
7. For webhook mode: copy the **Public Key** from "General Information" → `DISCORD_PUBLIC_KEY=your_key`

---

## Verify Installation

```bash
# Health check
curl http://127.0.0.1:8000/health

# Test query
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you do?"}'
```

A successful response looks like:
```json
{
  "route": "local_simple",
  "reason": "short_message",
  "response": "Hi! I'm [name]. I can answer questions, ..."
}
```

The `route` and `reason` fields tell you exactly which backend was used and why.
