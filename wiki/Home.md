<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 120" width="700" height="120">
  <defs>
    <linearGradient id="homeBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0F0A1E"/>
      <stop offset="100%" style="stop-color:#0A1628"/>
    </linearGradient>
    <linearGradient id="homeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#7C3AED"/>
      <stop offset="100%" style="stop-color:#06B6D4"/>
    </linearGradient>
  </defs>
  <rect width="700" height="120" fill="url(#homeBg)" rx="10"/>
  <text x="350" y="52" font-family="'Segoe UI',Arial,sans-serif" font-size="30" font-weight="800" fill="url(#homeGrad)" text-anchor="middle">Swarm 2.0 Wiki</text>
  <text x="350" y="82" font-family="'Segoe UI',Arial,sans-serif" font-size="14" fill="#94A3B8" text-anchor="middle">Hybrid AI Assistant · Complete Documentation</text>
  <line x1="100" y1="96" x2="600" y2="96" stroke="url(#homeGrad)" stroke-width="1.5" opacity="0.5"/>
</svg>

</div>

# Welcome to the Swarm 2.0 Wiki

This wiki is the complete technical reference for **Swarm 2.0** — a hybrid agentic AI assistant that runs on Raspberry Pi 5 or Windows, combining local `llama.cpp` inference with cloud providers (Groq, Gemini, Kimi) for optimal cost, speed, and privacy.

---

## Quick Navigation

| Page | Description |
|------|-------------|
| **[Home](Home)** | This page — project overview and navigation |
| **[Architecture](Architecture)** | System design, module map, data flow |
| **[Installation](Installation)** | Full setup guide (Pi 5 and Windows) |
| **[Usage](Usage)** | Running, querying, bot configuration |
| **[Privacy](Privacy)** | Data handling, security model |
| **[Contributing](Contributing)** | Developer onboarding, PR workflow |
| **[Troubleshooting](Troubleshooting)** | Common issues and solutions |
| **[Roadmap](Roadmap)** | Planned features and milestones |

---

## What is Swarm 2.0?

Swarm 2.0 is a **production-ready hybrid AI assistant** with the following key properties:

- **Edge-native**: Designed to run on a Raspberry Pi 5 (8 GB) with no internet connection required.
- **Hybrid routing**: A 4-tier cascade automatically selects the best inference backend per message.
- **Multi-bot**: Serves responses simultaneously over Telegram and Discord.
- **RAG-augmented**: All responses are enriched by a local vector knowledge base.
- **Privacy-first**: No data leaves the device in pure local mode.

---

## Architecture at a Glance

```
User (Telegram / Discord / REST)
        │
        ▼
  FastAPI (api.py)
        │
        ▼
  Orchestrator (orchestrator.py)
    ├── Tier 1: local_simple  ──► llama.cpp
    ├── Tier 2: keyword route ──► Groq / Gemini / Kimi
    ├── Tier 3: LLM classifier──► best route
    └── Tier 4: fallback      ──► llama.cpp
        │
        ├── RAG Store (hnswlib + SQLite)
        ├── Memory (SQLite per user)
        └── Personality (YAML / env vars)
```

See the [Architecture page](Architecture) for the full diagram and module breakdown.

---

## Getting Started in 3 Steps

1. **Install** — follow [Installation](Installation) for your platform.
2. **Configure** — copy `.env.example` to `.env` and fill in your paths and API keys.
3. **Run** — start with `bash scripts/pi_start_and_check.sh` (Pi) or `.\scripts\start_windows.ps1` (Windows).

---

## Technology Summary

| Layer | Technology |
|-------|-----------|
| API | FastAPI 0.115 + Uvicorn 0.34 |
| Local LLM | llama.cpp + Gemma 2 2B Q4_K_M |
| Cloud LLM | Groq, Google Gemini Flash, Kimi/Moonshot |
| Embeddings | sentence-transformers 3.4.1 |
| Vector DB | hnswlib 0.8.0 |
| Memory | SQLite + sqlite-utils |
| Bots | python-telegram-bot, discord.py 2.3.2 |
| Language | Python 3.9+ |

---

## License

Swarm 2.0 is released under the [MIT License](https://github.com/Kaelith69/Swarm2.0/blob/main/LICENSE).
