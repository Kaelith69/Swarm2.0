<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 220" width="900" height="220" role="img" aria-label="Swarm 2.0 banner">
  <defs>
    <linearGradient id="swarmBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B1020"/>
      <stop offset="100%" stop-color="#111B36"/>
    </linearGradient>
    <linearGradient id="swarmAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="900" height="220" rx="18" fill="url(#swarmBg)"/>
  <circle cx="130" cy="65" r="7" fill="#7C3AED"/>
  <circle cx="175" cy="105" r="7" fill="#06B6D4"/>
  <circle cx="85" cy="105" r="7" fill="#8B5CF6"/>
  <line x1="130" y1="65" x2="175" y2="105" stroke="url(#swarmAccent)" stroke-width="2"/>
  <line x1="130" y1="65" x2="85" y2="105" stroke="url(#swarmAccent)" stroke-width="2"/>
  <line x1="85" y1="105" x2="175" y2="105" stroke="url(#swarmAccent)" stroke-width="2"/>
  <text x="450" y="92" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="48" font-weight="800" fill="url(#swarmAccent)">Swarm 2.0</text>
  <text x="450" y="132" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="18" fill="#A5B4FC">Hybrid Agentic Assistant • Local + Cloud Inference • Discord + Telegram</text>
  <line x1="260" y1="158" x2="640" y2="158" stroke="url(#swarmAccent)" stroke-width="2" opacity="0.45"/>
</svg>

</div>

# Swarm 2.0

Swarm 2.0 is a production-focused hybrid AI assistant designed for Raspberry Pi 5 and Windows environments.  
It combines local `llama.cpp` inference, cloud model routing (Groq / Gemini / Kimi), local RAG, and multi-platform bot delivery.

## Documentation Suite

This repository includes a complete documentation system:

- **Project Docs**
  - [Contributing Guide](CONTRIBUTING.md)
  - [Security Policy](SECURITY.md)
  - [Changelog](CHANGELOG.md)
  - [License](LICENSE)
- **Wiki**
  - [Wiki Home](wiki/Home.md)
  - [Architecture](wiki/Architecture.md)
  - [Installation](wiki/Installation.md)
  - [Usage](wiki/Usage.md)
  - [Troubleshooting](wiki/Troubleshooting.md)
  - [Privacy](wiki/Privacy.md)
  - [Roadmap](wiki/Roadmap.md)
- **Assistant Subproject**
  - [Agentic Assistant README](agentic_assistant/README.md)
  - [Windows Setup Guide](agentic_assistant/GUIDE.md)
  - [Raspberry Pi Setup](agentic_assistant/docs/pi_setup.md)

## Quick Start

```bash
cd agentic_assistant
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/test_agent_end_to_end.py
```

For complete setup, see [agentic_assistant/README.md](agentic_assistant/README.md).
