# Hybrid Agentic Assistant for Raspberry Pi 5 (8GB)

Hybrid assistant with local + cloud inference:
- Local: `llama.cpp` + local RAG (`sentence-transformers` + `hnswlib` + SQLite)
- Cloud: Groq (fast reasoning), Gemini (long context), Kimi/Moonshot (planning)
- APIs: FastAPI + Telegram/Discord webhooks

## 1) Hardware and OS

Recommended:
- Raspberry Pi 5 (8GB)
- NVMe SSD (>= 128GB)
- Official 27W PSU
- Active cooling
- Raspberry Pi OS (64-bit)

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
- On Raspberry Pi/Linux, use Linux paths like `/home/pi/...`
- On Windows local testing, use Windows paths like `C:\Users\...`
- Do not mix Windows and Linux paths in the same runtime

Minimum local runtime values:
- `MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf`
- `LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli`

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

## 5) Routing behavior — 4-tier cascade

Every message passes through a priority cascade. **RAG context and conversation history (last `MEMORY_MAX_TURNS` turns) are injected into every prompt regardless of route.**

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

Tier 3 runs only when `USE_LLM_ROUTING=true` (default). Set `USE_LLM_ROUTING=false` for keyword-only routing (faster on very slow hardware).

`/query` returns both `route` and `reason` for full explainability.

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
- Discord: `POST /webhook/discord` (also handles Discord PING/PONG verification automatically)

## 10) Performance notes for Pi 5 (8GB, aarch64)

- Keep model quantized (`Q4_K_M`) — Gemma 2 2B Q4_K_M is ~1.6 GB RAM
- `INFERENCE_THREADS=4` — Pi 5 has 4 × Cortex-A76 cores, use all of them
- **Single-worker only**: The assistant uses SQLite for memory and RAG storage. Do NOT run with `uvicorn --workers N` (multi-worker mode) — SQLite connections are not safe across processes. The default single-worker mode is correct and sufficient for Pi 5 workloads.
- Store `RAG_DATA_DIR` on NVMe, not SD card — embedding queries are I/O-bound
- Monitor temperature: `vcgencmd measure_temp` (throttling begins at 80 °C)
- Lower `LLM_CONTEXT_TOKENS=1024` and `MEMORY_MAX_TURNS=6` if RAM is tight
- Disable LLM routing `USE_LLM_ROUTING=false` to save the classification inference call

**Approximate latency on Pi 5 8GB (active cooling, NVMe):**

| Route | Typical latency |
|-------|-----------------|
| Local Gemma (short / simple) | 2–8 s |
| Local Gemma + RAG | 3–10 s |
| Groq (cloud) | 0.3–1 s |
| Gemini (cloud) | 1–3 s |
| Kimi / Moonshot (cloud) | 1–4 s |
