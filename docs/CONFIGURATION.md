<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 100" width="720" height="100" role="img" aria-label="Configuration Reference header">
  <defs>
    <linearGradient id="cfgBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B18"/>
      <stop offset="100%" stop-color="#0B1124"/>
    </linearGradient>
    <linearGradient id="cfgAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
  </defs>
  <rect width="720" height="100" rx="12" fill="url(#cfgBg)"/>
  <text x="360" y="42" text-anchor="middle" font-family="'Segoe UI',Arial,sans-serif" font-size="26" font-weight="700" fill="url(#cfgAccent)">Swarm 2.0 — Configuration Reference</text>
  <text x="360" y="66" text-anchor="middle" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#64748B">All settings loaded from .env via python-dotenv · src/assistant/config.py</text>
  <line x1="80" y1="80" x2="640" y2="80" stroke="url(#cfgAccent)" stroke-width="1" opacity="0.4"/>
</svg>

</div>

# Configuration Reference

All Swarm 2.0 settings are loaded from a `.env` file at the `agentic_assistant/` root, using `python-dotenv`. The full `Settings` dataclass is defined in `src/assistant/config.py`.

**Setup:**

```bash
cd agentic_assistant
cp .env.example .env
chmod 600 .env   # Linux/macOS only
```

---

## Quick-Start Minimal `.env`

### Cloud-only (no local model required)

```env
BOT_MODE=polling
GROQ_API_KEY=your_groq_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token
DISCORD_BOT_TOKEN=your_discord_token
```

### Full local + cloud

```env
MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli
BOT_MODE=polling
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
KIMI_API_KEY=your_kimi_key
TELEGRAM_BOT_TOKEN=your_telegram_token
DISCORD_BOT_TOKEN=your_discord_token
AGENT_NAME=Aria
```

---

## Server Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Bind address for the FastAPI/Uvicorn server. Use `127.0.0.1` to restrict to localhost. |
| `PORT` | `8000` | TCP port the server listens on. |

```env
HOST=0.0.0.0
PORT=8000
```

---

## Local Inference (llama.cpp)

| Variable | Default (Linux) | Default (Windows) | Description |
|----------|-----------------|-------------------|-------------|
| `MODEL_PATH` | `/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf` | `C:\llama.cpp\models\gemma-2-2b-it-Q4_K_M.gguf` | Absolute path to the GGUF model file. Leave blank to disable local inference (cloud-only mode). |
| `LLAMA_MAIN_PATH` | `/home/pi/llama.cpp/build/bin/llama-cli` | `C:\llama.cpp\build\bin\llama-cli.exe` | Absolute path to the `llama-cli` binary. Leave blank to disable local inference. |
| `INFERENCE_THREADS` | `cpu_count - 1` | same | Number of CPU threads for llama.cpp. Defaults to one fewer than the available core count. Pi 5: set `4`. |
| `LLM_CONTEXT_TOKENS` | `2048` | same | Context window size in tokens. Reduce to `1024` to save RAM on constrained hardware. |
| `MAX_RESPONSE_TOKENS` | `256` | same | Maximum tokens the model may generate per response. |
| `LLM_TEMPERATURE` | `0.2` | same | Sampling temperature. `0.0` = deterministic; higher values = more creative/random. |
| `LLAMA_TIMEOUT_SECONDS` | `120` | same | Subprocess timeout (seconds). Raise to `180` on slow hardware or large context. |

```env
MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli
INFERENCE_THREADS=4
LLM_CONTEXT_TOKENS=2048
MAX_RESPONSE_TOKENS=256
LLM_TEMPERATURE=0.2
LLAMA_TIMEOUT_SECONDS=120
```

> **Platform paths**: On Windows, use Windows-style paths (`C:\...`). On Linux/Pi, use Unix paths (`/home/pi/...`). The application auto-detects the OS and sets defaults accordingly, but explicit values in `.env` must match the OS you are running on.

---

## RAG (Retrieval-Augmented Generation)

| Variable | Default | Description |
|----------|---------|-------------|
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Model name for `sentence-transformers`. Must be a valid Hugging Face model identifier or a local directory path. |
| `RAG_TOP_K` | `3` | Number of document chunks to retrieve and inject into each prompt. |
| `RAG_DATA_DIR` | `./data/rag` | Directory where the HNSW vector index (`vectors.bin`) and SQLite metadata (`chunks.sqlite3`) are stored. |

```env
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RAG_TOP_K=3
RAG_DATA_DIR=./data/rag
```

> **Windows example**: `RAG_DATA_DIR=C:\agentic-assistant\data\rag`

> **RAG is active immediately** once documents are ingested. Use `scripts/ingest_documents.py` to populate the knowledge base. See [agentic_assistant/README.md](../agentic_assistant/README.md#8-ingest-knowledge-for-rag) for the command.

---

## Routing Behaviour

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_LLM_ROUTING` | `true` | When `true`, Tier-3 uses the local Gemma model to classify ambiguous queries. Set to `false` for deterministic keyword-only routing (faster on low-end hardware). |
| `LOCAL_SHORT_THRESHOLD_CHARS` | `150` | Messages shorter than this value (and without complex signals) are routed directly to local inference without any routing overhead (Tier 1). |
| `LONG_CONTEXT_THRESHOLD_CHARS` | `1200` | Messages longer than this value are routed to Gemini Flash (long-context specialist). Tier 2 check. |

```env
USE_LLM_ROUTING=true
LOCAL_SHORT_THRESHOLD_CHARS=150
LONG_CONTEXT_THRESHOLD_CHARS=1200
```

---

## Safety and Input Limits

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_INPUT_CHARS` | `8000` | Hard limit on incoming message length (characters). Requests exceeding this limit receive `HTTP 413`. Prevents runaway cloud costs and prompt injection attempts. |
| `EXPOSE_DELIVERY_ERRORS` | `false` | When `false` (default), internal bot delivery errors are redacted from webhook responses. Set to `true` only during development. **Never enable in production.** |
| `CLOUD_TIMEOUT_SECONDS` | `25` | Timeout (seconds) for all cloud API calls (Groq, Gemini, Kimi). Cloud routes that exceed this timeout fall back to local inference. |

```env
MAX_INPUT_CHARS=8000
EXPOSE_DELIVERY_ERRORS=false
CLOUD_TIMEOUT_SECONDS=25
```

---

## Conversation Memory

| Variable | Default | Description |
|----------|---------|-------------|
| `MEMORY_MAX_TURNS` | `10` | Number of conversation turns (user + assistant pairs) kept per user in SQLite. Older turns are pruned automatically. Reduce to `6` on memory-constrained hardware. |

```env
MEMORY_MAX_TURNS=10
```

> Memory is stored in `<RAG_DATA_DIR>/memory.sqlite3`. It is keyed by `user_id` (e.g., `tg:123456789` for Telegram, `dc:987654321` for Discord, `api` for REST queries). Memory persists across server restarts.

---

## Bot Mode

| Variable | Default | Values | Description |
|----------|---------|--------|-------------|
| `BOT_MODE` | `webhook` | `polling` or `webhook` | Controls how Telegram and Discord bots receive messages. |

```env
BOT_MODE=polling
```

### `polling` (recommended for Windows and behind-NAT deployments)

Both bots run as async background tasks within the FastAPI process:

- **Telegram**: Calls `getUpdates` with long-polling (30-second timeout). No public URL required.
- **Discord**: Connects to Discord's WebSocket gateway via `discord.py`. No public URL required.

### `webhook`

Telegram and Discord POST events to your server's webhook endpoints:

- Telegram: `POST /webhook/telegram`
- Discord: `POST /webhook/discord`

Requires a publicly reachable HTTPS URL. On Windows without a public URL, use [ngrok](https://ngrok.com/) or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/).

---

## Cloud Inference Providers

All cloud keys are optional. Leaving a key blank disables that route; the orchestrator falls back to local inference.

### Groq (fast reasoning)

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | `""` | API key from [console.groq.com/keys](https://console.groq.com/keys). Enables `groq` route. |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq model identifier. |

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.1-8b-instant
```

Triggered by: `analyze`, `analyse`, `compare`, `tradeoff`, `reason`, `justify`, `deep dive`, `pros and cons`, `step by step`, `root cause`, `explain in detail` keywords, or Tier-3 LLM classifier routing to GROQ.

### Google Gemini (long context)

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | `""` | API key from [Google AI Studio](https://aistudio.google.com/app/apikey). Enables `gemini` route. |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model identifier. |

```env
GEMINI_API_KEY=AIzaSy_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-1.5-flash
```

Triggered by: messages exceeding `LONG_CONTEXT_THRESHOLD_CHARS` characters, or Tier-3 LLM classifier routing to GEMINI.

### Kimi / Moonshot (planning)

| Variable | Default | Description |
|----------|---------|-------------|
| `KIMI_API_KEY` | `""` | API key from the [Moonshot developer console](https://platform.moonshot.ai/). Enables `kimi` route. |
| `KIMI_BASE_URL` | `https://api.moonshot.ai/v1` | Kimi API base URL. |
| `KIMI_MODEL` | `moonshot-v1-8k` | Kimi model identifier. |

```env
KIMI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
KIMI_BASE_URL=https://api.moonshot.ai/v1
KIMI_MODEL=moonshot-v1-8k
```

Triggered by: `plan`, `roadmap`, `strategy`, `orchestrate`, `workflow`, `project steps` keywords, or Tier-3 LLM classifier routing to KIMI.

---

## Bot Tokens and Secrets

### Telegram

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | `""` | Bot token from `@BotFather` → `/newbot`. Required for both polling and webhook modes. |
| `TELEGRAM_SECRET` | `""` | Optional secret token for webhook authentication. When set, Telegram must include this value in the `X-Telegram-Bot-Api-Secret-Token` header. Only used in webhook mode. |

```env
TELEGRAM_BOT_TOKEN=1234567890:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_SECRET=my-random-secret-string
```

### Discord

| Variable | Default | Description |
|----------|---------|-------------|
| `DISCORD_BOT_TOKEN` | `""` | Bot token from the Discord Developer Portal (Bot → Token). Required for both polling (gateway) and webhook modes. |
| `DISCORD_PUBLIC_KEY` | `""` | Application public key from the Developer Portal (General Information). **Required for webhook mode** — used for Ed25519 signature verification. |
| `DISCORD_BEARER_TOKEN` | `""` | Legacy bearer token for custom webhook auth. Use `DISCORD_PUBLIC_KEY` for standard Discord interactions instead. |

```env
DISCORD_BOT_TOKEN=MTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DISCORD_PUBLIC_KEY=abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
```

> **Discord polling mode**: Enable **Message Content Intent** in the Developer Portal (Bot → Privileged Gateway Intents). Without it, the bot will connect but cannot read message content.

---

## Personality Configuration

The assistant's identity, tone, and response style are configured here. The YAML file takes precedence over env vars when it exists.

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_NAME` | `Assistant` | Display name injected into the system prompt. |
| `AGENT_PERSONALITY` | `helpful, knowledgeable, and professional` | Character adjectives describing the agent's personality. |
| `AGENT_RESPONSE_STYLE` | `concise, clear, and accurate` | Tone and style guidance for responses. |
| `AGENT_HUMOR` | `subtle and professional` | Humor style used when appropriate. |
| `AGENT_EXPERTISE` | `general knowledge, technology, and problem-solving` | Knowledge domains the agent should emphasize. |
| `PERSONALITY_FILE` | `./personality.yaml` | Path to an optional YAML file. Values in this file override the corresponding env vars above. |

```env
AGENT_NAME=Aria
AGENT_PERSONALITY=friendly, witty, and deeply knowledgeable
AGENT_RESPONSE_STYLE=warm and conversational, concise without being curt
AGENT_HUMOR=clever puns and light tech humour when appropriate
AGENT_EXPERTISE=software engineering, artificial intelligence, creative writing
PERSONALITY_FILE=./personality.yaml
```

### Personality YAML (recommended)

Copy `personality.yaml.example` to `personality.yaml` and edit:

```yaml
name: Aria
personality: friendly, witty, and deeply knowledgeable
response_style: warm and conversational, concise without being curt
humor: clever puns and light tech humour when appropriate
expertise: software engineering, artificial intelligence, creative writing
```

The YAML file is loaded at startup. Restart the server after editing it.

---

## Platform-Specific Notes

### Raspberry Pi 5

```env
# Recommended Pi 5 settings
INFERENCE_THREADS=4          # All 4 Cortex-A76 cores
LLM_CONTEXT_TOKENS=2048      # Safe for 8 GB RAM; reduce to 1024 if RAM is tight
MEMORY_MAX_TURNS=10          # Reduce to 6 on memory-constrained setups
LLAMA_TIMEOUT_SECONDS=120    # Raise to 180 for heavy queries
USE_LLM_ROUTING=true         # Tier-3 LLM routing (disable to save inference time)
BOT_MODE=webhook             # Pi is typically reachable from the internet
```

Monitor temperature to prevent throttling:

```bash
vcgencmd measure_temp        # Throttling begins at 80 °C
```

### Windows

```env
# Recommended Windows settings
INFERENCE_THREADS=8          # Adjust to your CPU core count
LLM_CONTEXT_TOKENS=2048
LLAMA_TIMEOUT_SECONDS=60     # Faster CPU — shorter timeout is fine
BOT_MODE=polling             # Polling avoids needing a public URL
MODEL_PATH=C:\llama.cpp\models\gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=C:\llama.cpp\build\bin\llama-cli.exe
RAG_DATA_DIR=C:\agentic-assistant\data\rag
PERSONALITY_FILE=C:\agentic-assistant\personality.yaml
```

---

## Full `.env.example` Reference

The repository ships with `agentic_assistant/.env.example` containing all variables with comments. Copy it as your starting point:

```bash
cp .env.example .env
```

---

## Environment Variable Validation

The `Settings` dataclass in `src/assistant/config.py` applies the following parsing rules:

| Type | Parsing | Fallback on invalid |
|------|---------|---------------------|
| `int` | `int(value)` | Uses the default |
| `float` | `float(value)` | Uses the default |
| `bool` | `"1"`, `"true"`, `"yes"`, `"on"` → `True` (case-insensitive) | Uses the default |
| `Path` | `Path(value)` | — |
| `str` | Raw string | — |

There is no startup validation that aborts the server on missing values — paths are checked lazily when local inference is first attempted. This allows the server to start in cloud-only mode without `MODEL_PATH` or `LLAMA_MAIN_PATH`.
