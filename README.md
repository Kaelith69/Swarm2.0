<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 240" width="960" height="240" role="img" aria-label="Swarm 2.0 banner">
  <defs>
    <linearGradient id="swarmBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B18"/>
      <stop offset="50%" stop-color="#0B1124"/>
      <stop offset="100%" stop-color="#0F1930"/>
    </linearGradient>
    <linearGradient id="swarmAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <linearGradient id="nodeGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#6D28D9"/>
    </linearGradient>
    <linearGradient id="nodeGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#06B6D4"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect x="0" y="0" width="960" height="240" rx="20" fill="url(#swarmBg)"/>
  <!-- Decorative grid lines -->
  <line x1="0" y1="80" x2="960" y2="80" stroke="#1E293B" stroke-width="0.5" opacity="0.5"/>
  <line x1="0" y1="160" x2="960" y2="160" stroke="#1E293B" stroke-width="0.5" opacity="0.5"/>
  <line x1="240" y1="0" x2="240" y2="240" stroke="#1E293B" stroke-width="0.5" opacity="0.3"/>
  <line x1="720" y1="0" x2="720" y2="240" stroke="#1E293B" stroke-width="0.5" opacity="0.3"/>
  <!-- Network nodes — left cluster -->
  <circle cx="95" cy="70" r="9" fill="url(#nodeGrad1)" filter="url(#glow)" opacity="0.9"/>
  <circle cx="55" cy="120" r="7" fill="url(#nodeGrad2)" filter="url(#glow)" opacity="0.8"/>
  <circle cx="140" cy="120" r="7" fill="url(#nodeGrad1)" filter="url(#glow)" opacity="0.8"/>
  <circle cx="75" cy="170" r="6" fill="url(#nodeGrad2)" opacity="0.7"/>
  <circle cx="125" cy="170" r="6" fill="url(#nodeGrad1)" opacity="0.7"/>
  <line x1="95" y1="70" x2="55" y2="120" stroke="url(#swarmAccent)" stroke-width="1.5" opacity="0.5"/>
  <line x1="95" y1="70" x2="140" y2="120" stroke="url(#swarmAccent)" stroke-width="1.5" opacity="0.5"/>
  <line x1="55" y1="120" x2="75" y2="170" stroke="#7C3AED" stroke-width="1" opacity="0.4"/>
  <line x1="140" y1="120" x2="125" y2="170" stroke="#06B6D4" stroke-width="1" opacity="0.4"/>
  <line x1="55" y1="120" x2="140" y2="120" stroke="url(#swarmAccent)" stroke-width="1.5" opacity="0.4"/>
  <!-- Network nodes — right cluster -->
  <circle cx="865" cy="70" r="9" fill="url(#nodeGrad2)" filter="url(#glow)" opacity="0.9"/>
  <circle cx="820" cy="120" r="7" fill="url(#nodeGrad1)" filter="url(#glow)" opacity="0.8"/>
  <circle cx="905" cy="120" r="7" fill="url(#nodeGrad2)" filter="url(#glow)" opacity="0.8"/>
  <circle cx="835" cy="170" r="6" fill="url(#nodeGrad1)" opacity="0.7"/>
  <circle cx="885" cy="170" r="6" fill="url(#nodeGrad2)" opacity="0.7"/>
  <line x1="865" y1="70" x2="820" y2="120" stroke="url(#swarmAccent)" stroke-width="1.5" opacity="0.5"/>
  <line x1="865" y1="70" x2="905" y2="120" stroke="url(#swarmAccent)" stroke-width="1.5" opacity="0.5"/>
  <line x1="820" y1="120" x2="835" y2="170" stroke="#7C3AED" stroke-width="1" opacity="0.4"/>
  <line x1="905" y1="120" x2="885" y2="170" stroke="#06B6D4" stroke-width="1" opacity="0.4"/>
  <line x1="820" y1="120" x2="905" y2="120" stroke="url(#swarmAccent)" stroke-width="1.5" opacity="0.4"/>
  <!-- Main title -->
  <text x="480" y="104" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="56" font-weight="800" fill="url(#swarmAccent)" filter="url(#glow)">Swarm 2.0</text>
  <text x="480" y="142" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="17" fill="#94A3B8" letter-spacing="1">Hybrid Agentic Assistant</text>
  <text x="480" y="164" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="13" fill="#64748B">Local llama.cpp · Groq · Gemini · Kimi · Discord · Telegram · RAG · SQLite Memory</text>
  <!-- Accent line -->
  <line x1="280" y1="186" x2="680" y2="186" stroke="url(#swarmAccent)" stroke-width="1.5" opacity="0.5"/>
  <!-- Platform badges (text) -->
  <rect x="298" y="196" width="84" height="20" rx="10" fill="#1E1B4B" stroke="#7C3AED" stroke-width="1" opacity="0.9"/>
  <text x="340" y="210" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="9" fill="#A78BFA">Raspberry Pi 5</text>
  <rect x="392" y="196" width="64" height="20" rx="10" fill="#0C1A2E" stroke="#06B6D4" stroke-width="1" opacity="0.9"/>
  <text x="424" y="210" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="9" fill="#67E8F9">Windows</text>
  <rect x="466" y="196" width="56" height="20" rx="10" fill="#0C1A2E" stroke="#0EA5E9" stroke-width="1" opacity="0.9"/>
  <text x="494" y="210" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="9" fill="#38BDF8">Python 3.9+</text>
  <rect x="532" y="196" width="52" height="20" rx="10" fill="#1A1A1A" stroke="#334155" stroke-width="1" opacity="0.9"/>
  <text x="558" y="210" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="9" fill="#94A3B8">MIT License</text>
  <rect x="594" y="196" width="70" height="20" rx="10" fill="#0F1F1A" stroke="#10B981" stroke-width="1" opacity="0.9"/>
  <text x="629" y="210" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="9" fill="#34D399">Production Ready</text>
</svg>

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Pi%205%20%7C%20Windows-blue?style=flat-square&logo=raspberry-pi&logoColor=white)](wiki/Installation.md)
[![llama.cpp](https://img.shields.io/badge/Local%20LLM-llama.cpp-orange?style=flat-square)](https://github.com/ggerganov/llama.cpp)
[![Groq](https://img.shields.io/badge/Cloud-Groq%20%7C%20Gemini%20%7C%20Kimi-6D28D9?style=flat-square)](agentic_assistant/README.md)

</div>

---

## What is Swarm 2.0?

**Swarm 2.0** is a production-ready, privacy-first hybrid AI assistant that runs on a **Raspberry Pi 5** or **Windows** PC. It routes each user message through a **4-tier cascade** — choosing the optimal backend (local or cloud) based on message length, keyword signals, and an on-device LLM classifier — while enriching every response with **local RAG** (retrieval-augmented generation) and **per-user conversation memory**.

```
User message
    │
    ├── Tier 1: Short & simple?      ──► llama.cpp (local, instant)
    ├── Tier 2: Keyword signal?      ──► Groq / Gemini / Kimi (cloud)
    ├── Tier 3: LLM classifier       ──► local Gemma decides
    └── Tier 4: Cloud unavailable?   ──► llama.cpp fallback (always works)
              │
              └── Every route: RAG context + conversation memory injected
```

---

## Feature Highlights

<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 310" width="920" height="310" role="img" aria-label="Feature grid">
  <defs>
    <linearGradient id="fBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B18"/>
      <stop offset="100%" stop-color="#0B1124"/>
    </linearGradient>
    <linearGradient id="fCard1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E1B4B"/><stop offset="100%" stop-color="#13113A"/>
    </linearGradient>
    <linearGradient id="fCard2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0C2340"/><stop offset="100%" stop-color="#071A30"/>
    </linearGradient>
    <linearGradient id="fCard3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A2020"/><stop offset="100%" stop-color="#061818"/>
    </linearGradient>
    <linearGradient id="fCard4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1A0A30"/><stop offset="100%" stop-color="#120820"/>
    </linearGradient>
  </defs>
  <rect width="920" height="310" rx="14" fill="url(#fBg)"/>
  <!-- Row 1 -->
  <!-- Card 1: 4-Tier Routing -->
  <rect x="16" y="16" width="208" height="130" rx="10" fill="url(#fCard1)" stroke="#7C3AED" stroke-width="1.2"/>
  <text x="32" y="42" font-family="'Segoe UI',Arial,sans-serif" font-size="20">🧠</text>
  <text x="58" y="42" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="700" fill="#C4B5FD">4-Tier Routing</text>
  <text x="32" y="64" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#8B7CC8">Length · Keyword · LLM</text>
  <text x="32" y="78" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#8B7CC8">classifier · Cloud fallback</text>
  <text x="32" y="96" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6B5FA0">Groq for reasoning</text>
  <text x="32" y="110" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6B5FA0">Gemini for long context</text>
  <text x="32" y="124" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6B5FA0">Kimi for planning</text>
  <!-- Card 2: Local RAG -->
  <rect x="238" y="16" width="208" height="130" rx="10" fill="url(#fCard2)" stroke="#0EA5E9" stroke-width="1.2"/>
  <text x="254" y="42" font-family="'Segoe UI',Arial,sans-serif" font-size="20">📚</text>
  <text x="280" y="42" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="700" fill="#7DD3FC">Local RAG</text>
  <text x="254" y="64" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#4A90B8">sentence-transformers</text>
  <text x="254" y="78" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#4A90B8">hnswlib · SQLite</text>
  <text x="254" y="96" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#3A708A">Ingest .txt / .md / .pdf</text>
  <text x="254" y="110" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#3A708A">Context injected every turn</text>
  <text x="254" y="124" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#3A708A">Zero external dependencies</text>
  <!-- Card 3: Memory -->
  <rect x="460" y="16" width="208" height="130" rx="10" fill="url(#fCard3)" stroke="#10B981" stroke-width="1.2"/>
  <text x="476" y="42" font-family="'Segoe UI',Arial,sans-serif" font-size="20">💬</text>
  <text x="502" y="42" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="700" fill="#6EE7B7">Conversation Memory</text>
  <text x="476" y="64" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#3A8A68">Per-user SQLite store</text>
  <text x="476" y="78" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#3A8A68">Configurable turn depth</text>
  <text x="476" y="96" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2E6E52">Persists across sessions</text>
  <text x="476" y="110" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2E6E52">Isolated by user_id</text>
  <text x="476" y="124" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2E6E52">Thread-safe single-writer</text>
  <!-- Card 4: Personality -->
  <rect x="682" y="16" width="222" height="130" rx="10" fill="url(#fCard4)" stroke="#A855F7" stroke-width="1.2"/>
  <text x="698" y="42" font-family="'Segoe UI',Arial,sans-serif" font-size="20">🎭</text>
  <text x="724" y="42" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="700" fill="#D8B4FE">Custom Personality</text>
  <text x="698" y="64" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#8B60C0">YAML or env vars</text>
  <text x="698" y="78" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#8B60C0">Name · style · humor</text>
  <text x="698" y="96" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6A4A94">Injected into every prompt</text>
  <text x="698" y="110" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6A4A94">Local and cloud routes</text>
  <text x="698" y="124" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6A4A94">No code changes needed</text>
  <!-- Row 2 -->
  <!-- Card 5: Bots -->
  <rect x="16" y="162" width="208" height="130" rx="10" fill="url(#fCard2)" stroke="#2563EB" stroke-width="1.2"/>
  <text x="32" y="188" font-family="'Segoe UI',Arial,sans-serif" font-size="20">🤖</text>
  <text x="58" y="188" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="700" fill="#93C5FD">Telegram + Discord</text>
  <text x="32" y="210" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#3A70B8">Polling (no public URL)</text>
  <text x="32" y="224" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#3A70B8">Webhook (server mode)</text>
  <text x="32" y="242" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2A5A94">Ed25519 Discord verify</text>
  <text x="32" y="256" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2A5A94">Telegram secret token</text>
  <text x="32" y="270" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2A5A94">Works behind NAT</text>
  <!-- Card 6: Privacy -->
  <rect x="238" y="162" width="208" height="130" rx="10" fill="url(#fCard3)" stroke="#059669" stroke-width="1.2"/>
  <text x="254" y="188" font-family="'Segoe UI',Arial,sans-serif" font-size="20">🔒</text>
  <text x="280" y="188" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="700" fill="#6EE7B7">Privacy First</text>
  <text x="254" y="210" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#3A8A68">Full offline mode available</text>
  <text x="254" y="224" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#3A8A68">No cloud when keys absent</text>
  <text x="254" y="242" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2E6E52">Memory stays on device</text>
  <text x="254" y="256" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2E6E52">Keys never logged</text>
  <text x="254" y="270" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2E6E52">EXPOSE_DELIVERY_ERRORS=false</text>
  <!-- Card 7: API -->
  <rect x="460" y="162" width="208" height="130" rx="10" fill="url(#fCard1)" stroke="#7C3AED" stroke-width="1.2"/>
  <text x="476" y="188" font-family="'Segoe UI',Arial,sans-serif" font-size="20">⚡</text>
  <text x="502" y="188" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="700" fill="#C4B5FD">FastAPI REST</text>
  <text x="476" y="210" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#8B7CC8">POST /query</text>
  <text x="476" y="224" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#8B7CC8">GET /health</text>
  <text x="476" y="242" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6B5FA0">Webhook: Telegram + Discord</text>
  <text x="476" y="256" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6B5FA0">curl-friendly JSON API</text>
  <text x="476" y="270" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#6B5FA0">route + reason in response</text>
  <!-- Card 8: Platforms -->
  <rect x="682" y="162" width="222" height="130" rx="10" fill="url(#fCard4)" stroke="#EC4899" stroke-width="1.2"/>
  <text x="698" y="188" font-family="'Segoe UI',Arial,sans-serif" font-size="20">🖥️</text>
  <text x="726" y="188" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="700" fill="#F9A8D4">Multi-Platform</text>
  <text x="698" y="210" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#C06090">Raspberry Pi 5 (8GB)</text>
  <text x="698" y="224" font-family="'Segoe UI',Arial,sans-serif" font-size="9.5" fill="#C06090">Windows 10/11 (64-bit)</text>
  <text x="698" y="242" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A04878">Linux / Ubuntu / Debian</text>
  <text x="698" y="256" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A04878">systemd + nginx ready</text>
  <text x="698" y="270" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A04878">Task Scheduler (Windows)</text>
</svg>

</div>

---

## Quick Start

### Raspberry Pi 5 / Linux

```bash
git clone https://github.com/Kaelith69/Swarm2.0.git
cd Swarm2.0/agentic_assistant
bash deploy/install_pi.sh
cp .env.example .env && chmod 600 .env
# Edit .env with your model path and API keys
bash scripts/pi_start_and_check.sh
```

### Windows (PowerShell)

```powershell
git clone https://github.com/Kaelith69/Swarm2.0.git
cd Swarm2.0\agentic_assistant
powershell -ExecutionPolicy Bypass -File deploy\install_windows.ps1
notepad .env   # fill in MODEL_PATH, bot tokens, cloud keys
powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1
```

### Verify it's running

```bash
curl http://127.0.0.1:8000/health
# → {"ok":true,"agent_name":"Assistant","bot_mode":"polling","hybrid":{...}}

curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you do?"}'
# → {"route":"local_simple","reason":"short_message","response":"..."}
```

---

## 4-Tier Routing Cascade

Every message is evaluated through a priority cascade. RAG context and conversation memory are injected into **every** backend prompt regardless of tier.

| Tier | Condition | Route | Provider | `reason` |
|------|-----------|-------|----------|----------|
| **1** | `len ≤ 150` and no complex signal | `local_simple` | llama.cpp local | `short_message` |
| **2** | `plan / roadmap / strategy / workflow` keyword | `kimi` | Moonshot Kimi | `kw_planning` |
| **2** | `len ≥ 1200` characters | `gemini` | Gemini Flash | `kw_long_context` |
| **2** | `analyze / compare / tradeoff / root cause` keyword | `groq` | Groq LLaMA | `kw_reasoning` |
| **2** | `docs / document / knowledge base / retrieve` keyword | `local_rag` | llama.cpp + RAG | `kw_rag` |
| **3** | Ambiguous → local Gemma classifies → cloud | varies | Groq / Gemini / Kimi | `llm_classifier` |
| **3** | Ambiguous → local Gemma classifies → local | `local_simple` | llama.cpp | `llm_classifier_local` |
| **4** | Cloud key missing or API error | `local_fallback` | llama.cpp | `*_unavailable` |

> Set `USE_LLM_ROUTING=false` for deterministic keyword-only routing (useful on constrained hardware).

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| API server | FastAPI + Uvicorn | 0.115 / 0.34 |
| Local LLM | llama.cpp + Gemma 2 2B Q4_K_M | latest |
| Cloud: reasoning | Groq (`llama-3.1-8b-instant`) | — |
| Cloud: long context | Google Gemini Flash | `gemini-1.5-flash` |
| Cloud: planning | Kimi / Moonshot | `moonshot-v1-8k` |
| Embeddings | sentence-transformers | 3.4.1 |
| Vector index | hnswlib (cosine HNSW) | 0.8.0 |
| Conversation store | SQLite 3 | built-in |
| Document parsing | pypdf | 5.3.1 |
| Bot: Telegram | httpx async poller | — |
| Bot: Discord | discord.py | 2.3.2 |
| Language | Python | 3.9+ |

---

## Platform Support

| Feature | Raspberry Pi 5 | Windows 10/11 | Linux (x86) |
|---------|:--------------:|:-------------:|:-----------:|
| Local inference (llama.cpp) | ✅ | ✅ | ✅ |
| Cloud routing (Groq/Gemini/Kimi) | ✅ | ✅ | ✅ |
| Telegram bot (polling) | ✅ | ✅ | ✅ |
| Discord bot (polling) | ✅ | ✅ | ✅ |
| Webhook mode | ✅ | ⚠️ (needs ngrok) | ✅ |
| systemd auto-start | ✅ | ❌ | ✅ |
| Task Scheduler auto-start | ❌ | ✅ | ❌ |
| Nginx reverse proxy | ✅ | ❌ | ✅ |

---

## Configuration Overview

All settings are loaded from `.env`. The most important ones:

```env
# Local model (required for local inference)
MODEL_PATH=/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf
LLAMA_MAIN_PATH=/home/pi/llama.cpp/build/bin/llama-cli

# Bot mode — "polling" for Windows/NAT, "webhook" for public servers
BOT_MODE=polling

# Cloud API keys (optional — leave blank to disable that route)
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
KIMI_API_KEY=your_key_here

# Bot tokens
TELEGRAM_BOT_TOKEN=your_token
DISCORD_BOT_TOKEN=your_token

# Personality (or use personality.yaml)
AGENT_NAME=Aria
AGENT_PERSONALITY=friendly, witty, and deeply knowledgeable
```

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for the full annotated reference.

---

## RAG Knowledge Ingestion

Place documents (`.txt`, `.md`, `.pdf`) in `data/knowledge/`, then run:

```bash
# Linux / Pi
export PYTHONPATH=src
python scripts/ingest_documents.py data/knowledge --source knowledge_base

# Windows (PowerShell)
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts\ingest_documents.py data\knowledge --source knowledge_base
```

RAG context is fetched for every message and injected into every prompt — local and cloud routes alike.

---

## Documentation Suite

| Document | Description |
|----------|-------------|
| **[agentic_assistant/README.md](agentic_assistant/README.md)** | Complete setup and operation guide |
| **[agentic_assistant/GUIDE.md](agentic_assistant/GUIDE.md)** | Detailed Windows & Pi walkthrough |
| **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** | REST API endpoint reference |
| **[docs/CONFIGURATION.md](docs/CONFIGURATION.md)** | Full `.env` configuration reference |
| **[wiki/Architecture.md](wiki/Architecture.md)** | System design and module map |
| **[wiki/Installation.md](wiki/Installation.md)** | Step-by-step installation |
| **[wiki/Usage.md](wiki/Usage.md)** | Running, querying, bot configuration |
| **[wiki/Troubleshooting.md](wiki/Troubleshooting.md)** | Common issues and fixes |
| **[wiki/Privacy.md](wiki/Privacy.md)** | Data handling and security model |
| **[wiki/Roadmap.md](wiki/Roadmap.md)** | Planned features and milestones |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Developer workflow and PR guide |
| **[SECURITY.md](SECURITY.md)** | Vulnerability reporting policy |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history |
| **[agentic_assistant/docs/pi_setup.md](agentic_assistant/docs/pi_setup.md)** | Raspberry Pi 5 production setup |

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

Key rules:
- **Single Uvicorn worker only** — SQLite is not process-safe; do not use `--workers N`.
- **Cloud is optional** — every code path must fall back gracefully to local inference.
- **Routing logic in `orchestrator.py`** — no routing decisions in `api.py` or bot adapters.
- **`pyright src/`** must exit cleanly before opening a PR.
- **`python scripts/test_agent_end_to_end.py`** must pass.

---

## License

Released under the [MIT License](LICENSE). © 2025 Kaelith69.
