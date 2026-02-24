<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260" width="900" height="260">
  <defs>
    <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0F0A1E;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#1E0A3C;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0A1628;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#7C3AED;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#06B6D4;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2563EB;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="orb1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#7C3AED;stop-opacity:0.6" />
      <stop offset="100%" style="stop-color:#2563EB;stop-opacity:0.1" />
    </linearGradient>
    <linearGradient id="orb2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#06B6D4;stop-opacity:0.4" />
      <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:0.1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="900" height="260" fill="url(#heroBg)" rx="12"/>
  <circle cx="80" cy="80" r="120" fill="url(#orb1)" opacity="0.4"/>
  <circle cx="820" cy="180" r="100" fill="url(#orb2)" opacity="0.3"/>
  <g opacity="0.06" stroke="#7C3AED" stroke-width="1">
    <line x1="0" y1="52" x2="900" y2="52"/><line x1="0" y1="104" x2="900" y2="104"/>
    <line x1="0" y1="156" x2="900" y2="156"/><line x1="0" y1="208" x2="900" y2="208"/>
    <line x1="150" y1="0" x2="150" y2="260"/><line x1="300" y1="0" x2="300" y2="260"/>
    <line x1="450" y1="0" x2="450" y2="260"/><line x1="600" y1="0" x2="600" y2="260"/>
    <line x1="750" y1="0" x2="750" y2="260"/>
  </g>
  <polygon points="100,65 120,53 140,65 140,89 120,101 100,89" fill="none" stroke="#7C3AED" stroke-width="2" opacity="0.8" filter="url(#glow)"/>
  <polygon points="105,68 120,59 135,68 135,86 120,95 105,86" fill="#7C3AED" opacity="0.2"/>
  <circle cx="120" cy="77" r="4" fill="#06B6D4" filter="url(#glow)"/>
  <line x1="108" y1="69" x2="120" y2="77" stroke="#06B6D4" stroke-width="1" opacity="0.7"/>
  <line x1="132" y1="69" x2="120" y2="77" stroke="#06B6D4" stroke-width="1" opacity="0.7"/>
  <line x1="108" y1="85" x2="120" y2="77" stroke="#7C3AED" stroke-width="1" opacity="0.7"/>
  <line x1="132" y1="85" x2="120" y2="77" stroke="#7C3AED" stroke-width="1" opacity="0.7"/>
  <circle cx="108" cy="69" r="2.5" fill="#7C3AED"/>
  <circle cx="132" cy="69" r="2.5" fill="#7C3AED"/>
  <circle cx="108" cy="85" r="2.5" fill="#2563EB"/>
  <circle cx="132" cy="85" r="2.5" fill="#2563EB"/>
  <text x="165" y="82" font-family="'Segoe UI',Arial,sans-serif" font-size="42" font-weight="800" fill="url(#titleGrad)" filter="url(#glow)" letter-spacing="1">Swarm 2.0</text>
  <text x="165" y="112" font-family="'Segoe UI',Arial,sans-serif" font-size="17" fill="#94A3B8" letter-spacing="0.5">Hybrid AI Assistant &#xB7; Local + Cloud Intelligence &#xB7; Pi 5 &amp; Windows</text>
  <line x1="165" y1="126" x2="700" y2="126" stroke="url(#titleGrad)" stroke-width="1.5" opacity="0.6"/>
  <rect x="165" y="140" width="130" height="26" rx="13" fill="#7C3AED" opacity="0.2" stroke="#7C3AED" stroke-width="1"/>
  <text x="230" y="157" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#C4B5FD" text-anchor="middle">&#x26A1; Local Inference</text>
  <rect x="305" y="140" width="120" height="26" rx="13" fill="#2563EB" opacity="0.2" stroke="#2563EB" stroke-width="1"/>
  <text x="365" y="157" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#93C5FD" text-anchor="middle">&#x2601; Cloud Routing</text>
  <rect x="435" y="140" width="110" height="26" rx="13" fill="#06B6D4" opacity="0.2" stroke="#06B6D4" stroke-width="1"/>
  <text x="490" y="157" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#67E8F9" text-anchor="middle">&#x1F9E0; RAG + Memory</text>
  <rect x="555" y="140" width="120" height="26" rx="13" fill="#7C3AED" opacity="0.15" stroke="#7C3AED" stroke-width="1"/>
  <text x="615" y="157" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#C4B5FD" text-anchor="middle">&#x1F916; Multi-Platform</text>
  <text x="165" y="210" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#475569">Python 3.9+ &#xB7; FastAPI &#xB7; llama.cpp &#xB7; Groq / Gemini / Kimi &#xB7; Telegram &amp; Discord</text>
  <circle cx="790" cy="80" r="5" fill="#7C3AED" opacity="0.8" filter="url(#glow)"/>
  <circle cx="830" cy="60" r="4" fill="#2563EB" opacity="0.7"/>
  <circle cx="830" cy="100" r="4" fill="#2563EB" opacity="0.7"/>
  <circle cx="860" cy="50" r="3" fill="#06B6D4" opacity="0.6"/>
  <circle cx="860" cy="80" r="3" fill="#06B6D4" opacity="0.6"/>
  <circle cx="860" cy="110" r="3" fill="#06B6D4" opacity="0.6"/>
  <line x1="790" y1="80" x2="830" y2="60" stroke="#7C3AED" stroke-width="1" opacity="0.5"/>
  <line x1="790" y1="80" x2="830" y2="100" stroke="#7C3AED" stroke-width="1" opacity="0.5"/>
  <line x1="830" y1="60" x2="860" y2="50" stroke="#2563EB" stroke-width="1" opacity="0.4"/>
  <line x1="830" y1="60" x2="860" y2="80" stroke="#2563EB" stroke-width="1" opacity="0.4"/>
  <line x1="830" y1="100" x2="860" y2="80" stroke="#2563EB" stroke-width="1" opacity="0.4"/>
  <line x1="830" y1="100" x2="860" y2="110" stroke="#2563EB" stroke-width="1" opacity="0.4"/>
</svg>

# Swarm 2.0 &mdash; Hybrid Agentic Assistant

**Edge-native AI that thinks locally, scales globally.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-7C3AED?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-06B6D4?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![llama.cpp](https://img.shields.io/badge/llama.cpp-local%20inference-7C3AED?style=flat-square)](https://github.com/ggerganov/llama.cpp)
[![License: MIT](https://img.shields.io/badge/License-MIT-2563EB?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205%20%7C%20Windows-06B6D4?style=flat-square)](wiki/Installation.md)
[![Telegram](https://img.shields.io/badge/Bot-Telegram-2563EB?style=flat-square&logo=telegram)](https://core.telegram.org/bots)
[![Discord](https://img.shields.io/badge/Bot-Discord-7C3AED?style=flat-square&logo=discord)](https://discord.com/developers)

</div>

---

> **Swarm 2.0** is the AI assistant that answers your questions before you finish typing them — and does it from a Raspberry Pi sitting on your desk, not a data center that may or may not be composting your prompts into ad revenue.
>
> It runs locally by default, escalates to the cloud only when it needs to flex, and falls back gracefully when the internet ghosts you at 2 AM. One box. Four routing tiers. Zero surveillance capitalism.
>
> No cloud. No spying. No Skynet. Relax. 🧘
>
> Powered by `llama.cpp`, a personality YAML, per-user SQLite memory, and the irrational optimism of someone who thought "I'll just run this on a Pi" was a reasonable idea.

<div align="center">

![Processing at the speed of your confusion](https://media.giphy.com/media/3oFzmMBnTyping2c8GQ/giphy.gif)

</div>

---

## Overview

**Swarm 2.0** is a production-ready hybrid AI assistant that combines on-device inference with cloud reasoning to deliver intelligent, context-aware responses across Telegram and Discord. It runs comfortably on a **Raspberry Pi 5 (8GB)** or any Windows PC, automatically routing each message to the best available inference backend.

A **4-tier routing cascade** decides per message whether to answer locally (fast, private, offline-capable) or escalate to Groq, Gemini, or Kimi for complex reasoning, long context, or planning tasks. A local **Retrieval-Augmented Generation (RAG)** pipeline and per-user **SQLite memory** are injected into every prompt regardless of route.

---

## Core Capability Graph

<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 320" width="760" height="320">
  <defs>
    <linearGradient id="capBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0F0A1E"/>
      <stop offset="100%" style="stop-color:#0D1B2A"/>
    </linearGradient>
    <linearGradient id="barLocal" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#7C3AED"/>
      <stop offset="100%" style="stop-color:#9F67FF"/>
    </linearGradient>
    <linearGradient id="barCloud" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2563EB"/>
      <stop offset="100%" style="stop-color:#60A5FA"/>
    </linearGradient>
    <linearGradient id="barRag" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#06B6D4"/>
      <stop offset="100%" style="stop-color:#67E8F9"/>
    </linearGradient>
  </defs>
  <rect width="760" height="320" fill="url(#capBg)" rx="10"/>
  <text x="380" y="36" font-family="'Segoe UI',Arial,sans-serif" font-size="16" font-weight="700" fill="#E2E8F0" text-anchor="middle">System Capability Overview</text>
  <text x="20" y="84" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#94A3B8">Local Inference Speed</text>
  <text x="20" y="124" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#94A3B8">Cloud Reasoning Power</text>
  <text x="20" y="164" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#94A3B8">RAG Knowledge Depth</text>
  <text x="20" y="204" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#94A3B8">Conversation Memory</text>
  <text x="20" y="244" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#94A3B8">Privacy (Local Mode)</text>
  <text x="20" y="284" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#94A3B8">Multi-Platform Bots</text>
  <rect x="210" y="68" width="400" height="20" rx="4" fill="#1E293B"/>
  <rect x="210" y="68" width="288" height="20" rx="4" fill="url(#barLocal)"/>
  <text x="506" y="83" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#C4B5FD">72%</text>
  <rect x="210" y="108" width="400" height="20" rx="4" fill="#1E293B"/>
  <rect x="210" y="108" width="380" height="20" rx="4" fill="url(#barCloud)"/>
  <text x="596" y="123" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#93C5FD">95%</text>
  <rect x="210" y="148" width="400" height="20" rx="4" fill="#1E293B"/>
  <rect x="210" y="148" width="320" height="20" rx="4" fill="url(#barRag)"/>
  <text x="536" y="163" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#67E8F9">80%</text>
  <rect x="210" y="188" width="400" height="20" rx="4" fill="#1E293B"/>
  <rect x="210" y="188" width="340" height="20" rx="4" fill="url(#barLocal)"/>
  <text x="556" y="203" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#C4B5FD">85%</text>
  <rect x="210" y="228" width="400" height="20" rx="4" fill="#1E293B"/>
  <rect x="210" y="228" width="400" height="20" rx="4" fill="url(#barRag)"/>
  <text x="616" y="243" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#67E8F9">100%</text>
  <rect x="210" y="268" width="400" height="20" rx="4" fill="#1E293B"/>
  <rect x="210" y="268" width="360" height="20" rx="4" fill="url(#barCloud)"/>
  <text x="576" y="283" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#93C5FD">90%</text>
</svg>

</div>

---

## Architecture

<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 480" width="820" height="480">
  <defs>
    <linearGradient id="archBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0F0A1E"/>
      <stop offset="100%" style="stop-color:#0D1B2A"/>
    </linearGradient>
    <linearGradient id="boxPurple" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#4C1D95"/>
      <stop offset="100%" style="stop-color:#2D1B69"/>
    </linearGradient>
    <linearGradient id="boxBlue" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#1E3A8A"/>
      <stop offset="100%" style="stop-color:#1E2A5A"/>
    </linearGradient>
    <linearGradient id="boxCyan" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#0E4A5C"/>
      <stop offset="100%" style="stop-color:#083344"/>
    </linearGradient>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7C3AED"/>
    </marker>
    <marker id="arrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563EB"/>
    </marker>
    <marker id="arrC" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#06B6D4"/>
    </marker>
  </defs>
  <rect width="820" height="480" fill="url(#archBg)" rx="10"/>
  <text x="410" y="30" font-family="'Segoe UI',Arial,sans-serif" font-size="15" font-weight="700" fill="#E2E8F0" text-anchor="middle">Swarm 2.0 System Architecture</text>
  <rect x="90" y="50" width="130" height="52" rx="8" fill="url(#boxBlue)" stroke="#2563EB" stroke-width="1.5"/>
  <text x="155" y="72" font-family="'Segoe UI',Arial,sans-serif" font-size="13" font-weight="600" fill="#93C5FD" text-anchor="middle">Telegram</text>
  <text x="155" y="90" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#60A5FA" text-anchor="middle">Polling / Webhook</text>
  <rect x="260" y="50" width="130" height="52" rx="8" fill="url(#boxPurple)" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="325" y="72" font-family="'Segoe UI',Arial,sans-serif" font-size="13" font-weight="600" fill="#C4B5FD" text-anchor="middle">Discord</text>
  <text x="325" y="90" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#A78BFA" text-anchor="middle">Gateway / Webhook</text>
  <rect x="430" y="50" width="130" height="52" rx="8" fill="url(#boxCyan)" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="495" y="72" font-family="'Segoe UI',Arial,sans-serif" font-size="13" font-weight="600" fill="#67E8F9" text-anchor="middle">HTTP Client</text>
  <text x="495" y="90" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#22D3EE" text-anchor="middle">REST / curl</text>
  <line x1="155" y1="102" x2="155" y2="138" stroke="#2563EB" stroke-width="1.5" marker-end="url(#arrB)"/>
  <line x1="325" y1="102" x2="325" y2="138" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="495" y1="102" x2="495" y2="138" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#arrC)"/>
  <rect x="90" y="138" width="600" height="82" rx="8" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>
  <text x="390" y="162" font-family="'Segoe UI',Arial,sans-serif" font-size="13" font-weight="700" fill="#E2E8F0" text-anchor="middle">FastAPI Application (api.py)</text>
  <rect x="110" y="172" width="120" height="30" rx="5" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <text x="170" y="191" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#94A3B8" text-anchor="middle">POST /query</text>
  <rect x="250" y="172" width="120" height="30" rx="5" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <text x="310" y="191" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#94A3B8" text-anchor="middle">GET /health</text>
  <rect x="390" y="172" width="150" height="30" rx="5" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <text x="465" y="191" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#94A3B8" text-anchor="middle">POST /webhook/telegram</text>
  <rect x="555" y="172" width="120" height="30" rx="5" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <text x="615" y="191" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#94A3B8" text-anchor="middle">POST /webhook/discord</text>
  <line x1="390" y1="220" x2="390" y2="248" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="90" y="248" width="600" height="102" rx="8" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>
  <text x="390" y="270" font-family="'Segoe UI',Arial,sans-serif" font-size="13" font-weight="700" fill="#E2E8F0" text-anchor="middle">Orchestrator (orchestrator.py)</text>
  <text x="390" y="286" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#64748B" text-anchor="middle">4-Tier Routing Cascade &#xB7; RAG Injection &#xB7; Memory Injection &#xB7; Personality Prompt</text>
  <rect x="110" y="295" width="100" height="40" rx="5" fill="url(#boxPurple)" stroke="#7C3AED" stroke-width="1"/>
  <text x="160" y="313" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#C4B5FD" text-anchor="middle">Personality</text>
  <text x="160" y="326" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A78BFA" text-anchor="middle">personality.py</text>
  <rect x="225" y="295" width="100" height="40" rx="5" fill="url(#boxCyan)" stroke="#06B6D4" stroke-width="1"/>
  <text x="275" y="313" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#67E8F9" text-anchor="middle">Memory</text>
  <text x="275" y="326" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#22D3EE" text-anchor="middle">memory.py</text>
  <rect x="340" y="295" width="100" height="40" rx="5" fill="url(#boxCyan)" stroke="#06B6D4" stroke-width="1"/>
  <text x="390" y="313" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#67E8F9" text-anchor="middle">RAG Store</text>
  <text x="390" y="326" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#22D3EE" text-anchor="middle">rag/store.py</text>
  <rect x="455" y="295" width="100" height="40" rx="5" fill="url(#boxBlue)" stroke="#2563EB" stroke-width="1"/>
  <text x="505" y="313" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#93C5FD" text-anchor="middle">Config</text>
  <text x="505" y="326" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#60A5FA" text-anchor="middle">config.py</text>
  <rect x="570" y="295" width="100" height="40" rx="5" fill="url(#boxPurple)" stroke="#7C3AED" stroke-width="1"/>
  <text x="620" y="313" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#C4B5FD" text-anchor="middle">Parsers/Senders</text>
  <text x="620" y="326" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A78BFA" text-anchor="middle">messaging/</text>
  <line x1="280" y1="350" x2="200" y2="382" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="390" y1="350" x2="390" y2="382" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#arrC)"/>
  <line x1="500" y1="350" x2="580" y2="382" stroke="#2563EB" stroke-width="1.5" marker-end="url(#arrB)"/>
  <rect x="90" y="382" width="180" height="70" rx="8" fill="url(#boxPurple)" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="180" y="407" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="600" fill="#C4B5FD" text-anchor="middle">Local LLM</text>
  <text x="180" y="423" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#A78BFA" text-anchor="middle">llama.cpp (Gemma 2 2B)</text>
  <text x="180" y="438" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#7C3AED" text-anchor="middle">Q4_K_M &#xB7; aarch64 / x86</text>
  <rect x="300" y="382" width="180" height="70" rx="8" fill="url(#boxCyan)" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="390" y="407" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="600" fill="#67E8F9" text-anchor="middle">RAG + Memory</text>
  <text x="390" y="423" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#22D3EE" text-anchor="middle">HNSW + sentence-transformers</text>
  <text x="390" y="438" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#06B6D4" text-anchor="middle">SQLite (memory &amp; metadata)</text>
  <rect x="510" y="382" width="220" height="70" rx="8" fill="url(#boxBlue)" stroke="#2563EB" stroke-width="1.5"/>
  <text x="620" y="407" font-family="'Segoe UI',Arial,sans-serif" font-size="12" font-weight="600" fill="#93C5FD" text-anchor="middle">Cloud Providers</text>
  <text x="620" y="423" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#60A5FA" text-anchor="middle">Groq &#xB7; Gemini Flash &#xB7; Kimi</text>
  <text x="620" y="438" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#2563EB" text-anchor="middle">cloud_router.py &#xB7; fallback-aware</text>
</svg>

</div>

---

## Data Flow

<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 200" width="780" height="200">
  <defs>
    <linearGradient id="dfBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0F0A1E"/>
      <stop offset="100%" style="stop-color:#0D1B2A"/>
    </linearGradient>
    <marker id="dfArr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7C3AED"/>
    </marker>
  </defs>
  <rect width="780" height="200" fill="url(#dfBg)" rx="10"/>
  <text x="390" y="24" font-family="'Segoe UI',Arial,sans-serif" font-size="14" font-weight="700" fill="#E2E8F0" text-anchor="middle">Message Data Flow</text>
  <rect x="20" y="50" width="100" height="50" rx="6" fill="#1E0A3C" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="70" y="72" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#C4B5FD" text-anchor="middle">User Message</text>
  <text x="70" y="88" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A78BFA" text-anchor="middle">Telegram/Discord</text>
  <line x1="120" y1="75" x2="148" y2="75" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#dfArr)"/>
  <rect x="150" y="50" width="100" height="50" rx="6" fill="#0A1628" stroke="#2563EB" stroke-width="1.5"/>
  <text x="200" y="72" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#93C5FD" text-anchor="middle">Parse &amp; Route</text>
  <text x="200" y="88" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#60A5FA" text-anchor="middle">4-Tier Cascade</text>
  <line x1="250" y1="75" x2="278" y2="75" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#dfArr)"/>
  <rect x="280" y="50" width="110" height="50" rx="6" fill="#083344" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="335" y="68" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#67E8F9" text-anchor="middle">RAG Retrieval</text>
  <text x="335" y="82" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#22D3EE" text-anchor="middle">Vector search</text>
  <text x="335" y="94" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#22D3EE" text-anchor="middle">+ Memory load</text>
  <line x1="390" y1="75" x2="418" y2="75" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#dfArr)"/>
  <rect x="420" y="50" width="110" height="50" rx="6" fill="#1E0A3C" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="475" y="68" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#C4B5FD" text-anchor="middle">Prompt Build</text>
  <text x="475" y="82" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A78BFA" text-anchor="middle">Personality +</text>
  <text x="475" y="94" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#A78BFA" text-anchor="middle">Context + Query</text>
  <line x1="530" y1="75" x2="558" y2="75" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#dfArr)"/>
  <rect x="560" y="50" width="100" height="50" rx="6" fill="#0A1628" stroke="#2563EB" stroke-width="1.5"/>
  <text x="610" y="72" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#93C5FD" text-anchor="middle">LLM Inference</text>
  <text x="610" y="88" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#60A5FA" text-anchor="middle">Local or Cloud</text>
  <line x1="660" y1="75" x2="688" y2="75" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#dfArr)"/>
  <rect x="690" y="50" width="80" height="50" rx="6" fill="#083344" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="730" y="72" font-family="'Segoe UI',Arial,sans-serif" font-size="11" font-weight="600" fill="#67E8F9" text-anchor="middle">Response</text>
  <text x="730" y="88" font-family="'Segoe UI',Arial,sans-serif" font-size="9" fill="#22D3EE" text-anchor="middle">+ route/reason</text>
  <text x="390" y="145" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#475569" text-anchor="middle">Each response includes: answer &#xB7; route &#xB7; reason &#xB7; rag_used &#xB7; memory_turns metadata</text>
  <text x="390" y="162" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#334155" text-anchor="middle">Memory is saved back to SQLite after every successful inference</text>
</svg>

</div>

---

## Technology Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Runtime** | Python | 3.9+ | Core application language |
| **API Server** | FastAPI + Uvicorn | 0.115 / 0.34 | REST API, webhooks, ASGI server |
| **Local Inference** | llama.cpp | latest | Quantized on-device LLM inference |
| **Local Model** | Gemma 2 2B Q4_K_M | &mdash; | Default local model (~1.6 GB RAM) |
| **Embeddings** | sentence-transformers | 3.4.1 | Document & query embeddings for RAG |
| **Vector Search** | hnswlib | 0.8.0 | Approximate nearest-neighbour retrieval |
| **Memory Store** | SQLite + sqlite-utils | 3.36 | Per-user conversation history |
| **Cloud &mdash; Fast** | Groq API | 0.13.1 | Fast reasoning (LLaMA-family models) |
| **Cloud &mdash; Long** | Google Gemini Flash | 0.8.4 | Long-context understanding |
| **Cloud &mdash; Plan** | Kimi / Moonshot | openai 1.61.1 | Planning and multi-step reasoning |
| **Bot &mdash; Telegram** | python-telegram-bot | &mdash; | Telegram polling & webhook bot |
| **Bot &mdash; Discord** | discord.py | 2.3.2 | Discord gateway & webhook bot |
| **Config** | python-dotenv + PyYAML | 1.0.1 / 6.0.2 | Environment management & personality |
| **Docs parsing** | pypdf + Markdown | 5.3.1 / 3.6 | RAG document ingestion |
| **Security** | PyNaCl | 1.5.0 | Discord Ed25519 signature verification |

---

## Features

| Feature | Description |
|---------|-------------|
| &#x1F500; **4-Tier Routing Cascade** | Per-message routing: local-simple &rarr; keyword cloud &rarr; LLM classifier &rarr; fallback |
| &#x1F9E0; **Hybrid Inference** | Combines llama.cpp local inference with Groq, Gemini, and Kimi |
| &#x1F4DA; **Local RAG** | HNSW vector search over ingested documents; injected into every prompt |
| &#x1F4AC; **Conversation Memory** | SQLite per-user turn history; configurable depth |
| &#x1F916; **Telegram Bot** | Full polling and webhook support via BotFather |
| &#x1F3AE; **Discord Bot** | Gateway (polling) and interactions webhook support |
| &#x1F3AD; **Personality Engine** | YAML-configurable agent identity, character, and expertise |
| &#x26A1; **Edge Optimised** | Q4_K_M quantization; tuned defaults for Raspberry Pi 5 |
| &#x1F512; **Privacy-First** | Fully offline capable in local mode; no telemetry |
| &#x1F4D6; **Explainable Routes** | Every response returns `route` and `reason` fields |
| &#x1F504; **Auto-Fallback** | Transparently falls back to local when cloud is unavailable |
| &#x1F4C4; **Document Ingestion** | CLI script for `.txt`, `.md`, `.pdf` ingestion |

---

## Installation

### Prerequisites

- Python 3.9 or higher
- A compiled `llama-cli` binary (from [llama.cpp](https://github.com/ggerganov/llama.cpp))
- A GGUF model file (e.g. `gemma-2-2b-it-Q4_K_M.gguf`)

### Raspberry Pi 5

```bash
sudo mkdir -p /opt/agentic-assistant
sudo chown -R $USER:$USER /opt/agentic-assistant
cd /opt/agentic-assistant
git clone https://github.com/Kaelith69/Swarm2.0.git .
bash deploy/install_pi.sh
cp .env.example .env && chmod 600 .env
# Edit .env with your paths and API keys
```

### Windows

```powershell
git clone https://github.com/Kaelith69/Swarm2.0.git
cd agentic_assistant
powershell -ExecutionPolicy Bypass -File deploy\install_windows.ps1
Copy-Item .env.example .env
# Edit .env with your paths and API keys
```

### Manual (any platform)

```bash
cd agentic_assistant
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env
export PYTHONPATH=$(pwd)/src
python -m assistant.agent
```

For the full setup guide see [`agentic_assistant/GUIDE.md`](agentic_assistant/GUIDE.md) or the [Installation wiki page](wiki/Installation.md).

---

## Usage

### Start the server

```bash
# Raspberry Pi
bash scripts/pi_start_and_check.sh

# Windows
.\scripts\start_windows.ps1

# Manual
source .venv/bin/activate
export PYTHONPATH=src
python -m assistant.agent
```

### Query via REST API

```bash
# Health check
curl http://127.0.0.1:8000/health

# Send a message
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?", "user_id": "user1"}'
```

**Example response:**

```json
{
  "response": "The capital of France is Paris.",
  "route": "local_simple",
  "reason": "short_message",
  "rag_used": false,
  "memory_turns": 2
}
```

### Ingest documents into RAG

```bash
source .venv/bin/activate
export PYTHONPATH=src
python scripts/ingest_documents.py /path/to/docs --source knowledge_base
```

### Run end-to-end tests

```bash
python scripts/test_agent_end_to_end.py
```

---

## Routing Reference &mdash; 4-Tier Cascade

> RAG context and conversation history are injected into every prompt regardless of route.

| Tier | Trigger | Route | Provider | `reason` |
|------|---------|-------|----------|---------|
| 1 | len &le; 150 chars, no complex signal | `local_simple` | Local Gemma | `short_message` |
| 2 | `plan / roadmap / strategy / workflow` | `kimi` | Kimi / Moonshot | `kw_planning` |
| 2 | len &ge; 1200 chars | `gemini` | Gemini Flash | `kw_long_context` |
| 2 | `analyze / compare / tradeoff / root cause` | `groq` | Groq LLaMA | `kw_reasoning` |
| 2 | `docs / document / knowledge base / retrieve` | `local_rag` | Local Gemma + RAG | `kw_rag` |
| 3 | Ambiguous &rarr; LLM classifies &rarr; cloud | varies | Groq / Gemini / Kimi | `llm_classifier` |
| 3 | Ambiguous &rarr; LLM classifies &rarr; local | `local_simple` | Local Gemma | `llm_classifier_local` |
| 4 | Cloud key missing or API error | `local_fallback` | Local Gemma | `*_unavailable` |

Set `USE_LLM_ROUTING=false` to skip Tier 3 (faster on constrained hardware).

---

## Project Structure

```
Swarm2.0/
├── README.md                        <- this file
├── LICENSE
├── wiki/                            <- GitHub Wiki pages
└── agentic_assistant/
    ├── .env.example                 <- environment configuration template
    ├── personality.yaml.example     <- personality configuration template
    ├── requirements.txt
    ├── pyproject.toml
    ├── GUIDE.md                     <- comprehensive setup guide
    ├── LANGCHAIN_DOCS_MCP_GUIDE.md
    ├── data/
    │   └── knowledge/               <- RAG document store
    ├── deploy/
    │   ├── install_pi.sh
    │   ├── install_windows.ps1
    │   ├── agent.service            <- systemd unit
    │   └── nginx-agent.conf         <- nginx reverse proxy
    ├── docs/
    │   └── pi_setup.md
    ├── scripts/
    │   ├── ingest_documents.py      <- RAG ingestion CLI
    │   ├── test_agent_end_to_end.py
    │   ├── pi_start_and_check.sh
    │   ├── start_windows.ps1
    │   └── start_windows.bat
    └── src/assistant/
        ├── agent.py                 <- entry point (uvicorn)
        ├── api.py                   <- FastAPI app + endpoints
        ├── config.py                <- settings dataclass
        ├── memory.py                <- SQLite conversation memory
        ├── orchestrator.py          <- 4-tier routing engine
        ├── personality.py           <- agent identity
        ├── llm/
        │   ├── llama_cpp_runner.py  <- local inference wrapper
        │   └── cloud_router.py      <- Groq / Gemini / Kimi client
        ├── rag/
        │   └── store.py             <- HNSW vector store
        ├── messaging/
        │   ├── parsers.py           <- inbound message parsing
        │   └── senders.py           <- outbound message delivery
        └── bots/
            ├── telegram_polling.py  <- Telegram polling loop
            └── discord_bot.py       <- Discord gateway + webhook
```

---

## Performance

<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 230" width="760" height="230">
  <defs>
    <linearGradient id="perfBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0F0A1E"/>
      <stop offset="100%" style="stop-color:#0D1B2A"/>
    </linearGradient>
  </defs>
  <rect width="760" height="230" fill="url(#perfBg)" rx="10"/>
  <text x="380" y="30" font-family="'Segoe UI',Arial,sans-serif" font-size="15" font-weight="700" fill="#E2E8F0" text-anchor="middle">Latency on Raspberry Pi 5 &#xB7; 8GB &#xB7; Active Cooling &#xB7; NVMe</text>
  <rect x="30" y="50" width="160" height="80" rx="8" fill="#1E0A3C" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="110" y="78" font-family="'Segoe UI',Arial,sans-serif" font-size="22" font-weight="800" fill="#C4B5FD" text-anchor="middle">2&#x2013;8s</text>
  <text x="110" y="98" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#A78BFA" text-anchor="middle">Local Gemma</text>
  <text x="110" y="114" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#6D28D9" text-anchor="middle">short / simple</text>
  <rect x="207" y="50" width="160" height="80" rx="8" fill="#1E0A3C" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="287" y="78" font-family="'Segoe UI',Arial,sans-serif" font-size="22" font-weight="800" fill="#C4B5FD" text-anchor="middle">3&#x2013;10s</text>
  <text x="287" y="98" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#A78BFA" text-anchor="middle">Local + RAG</text>
  <text x="287" y="114" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#6D28D9" text-anchor="middle">embedding + retrieval</text>
  <rect x="384" y="50" width="160" height="80" rx="8" fill="#0A1628" stroke="#2563EB" stroke-width="1.5"/>
  <text x="464" y="78" font-family="'Segoe UI',Arial,sans-serif" font-size="22" font-weight="800" fill="#93C5FD" text-anchor="middle">0.3&#x2013;1s</text>
  <text x="464" y="98" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#60A5FA" text-anchor="middle">Groq Cloud</text>
  <text x="464" y="114" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#1D4ED8" text-anchor="middle">fast reasoning</text>
  <rect x="561" y="50" width="160" height="80" rx="8" fill="#083344" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="641" y="78" font-family="'Segoe UI',Arial,sans-serif" font-size="22" font-weight="800" fill="#67E8F9" text-anchor="middle">1&#x2013;4s</text>
  <text x="641" y="98" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#22D3EE" text-anchor="middle">Gemini / Kimi</text>
  <text x="641" y="114" font-family="'Segoe UI',Arial,sans-serif" font-size="10" fill="#0891B2" text-anchor="middle">long context / plan</text>
  <text x="30" y="165" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#475569">&#x2022; Model: Gemma 2 2B Q4_K_M &#xB7; ~1.6 GB RAM &#xB7; INFERENCE_THREADS=4</text>
  <text x="30" y="183" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#475569">&#x2022; Single-worker Uvicorn only (SQLite not safe across multiple processes)</text>
  <text x="30" y="201" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#475569">&#x2022; Thermal throttling begins at 80&#xB0;C &#x2014; monitor with vcgencmd measure_temp</text>
  <text x="30" y="219" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="#475569">&#x2022; Lower LLM_CONTEXT_TOKENS + MEMORY_MAX_TURNS if RAM is constrained</text>
</svg>

</div>

---

## Privacy & Security

- **Local mode is fully offline.** No data leaves the device when cloud API keys are absent.
- **API keys** are stored in `.env` (mode `600`, never committed).
- **Conversation memory** lives entirely in a local SQLite database.
- **Discord webhook verification** uses Ed25519 signatures via PyNaCl.
- **Telegram webhook** supports a configurable secret token (`TELEGRAM_SECRET`).
- `EXPOSE_DELIVERY_ERRORS=false` (default) prevents internal error details from reaching end users.

See the [Privacy wiki page](wiki/Privacy.md) for the full security model.

---

## Design Principles

1. **Edge-first** &mdash; designed for Raspberry Pi 5; cloud is optional, not required.
2. **Fail-safe fallback** &mdash; any cloud failure transparently falls back to local inference.
3. **Explainable routing** &mdash; every response documents which backend was used and why.
4. **Privacy by default** &mdash; data never leaves the device unless a cloud key is configured.
5. **Single-worker discipline** &mdash; SQLite safety enforced; no multi-process footguns.
6. **Modular architecture** &mdash; each subsystem (LLM, RAG, memory, bots) is independently replaceable.

---

## Roadmap

| Milestone | Status |
|-----------|--------|
| 4-tier routing cascade | &#x2705; Complete |
| Telegram & Discord bots | &#x2705; Complete |
| Local RAG (HNSW + SQLite) | &#x2705; Complete |
| Personality YAML system | &#x2705; Complete |
| Pi 5 & Windows support | &#x2705; Complete |
| Streaming responses | &#x1F51C; Planned |
| Web UI dashboard | &#x1F51C; Planned |
| Additional cloud providers | &#x1F51C; Planned |
| Voice / TTS integration | &#x1F51C; Planned |
| Multi-agent swarm coordination | &#x1F51C; Planned |

See the full [Roadmap](wiki/Roadmap.md) in the wiki.

---

## License

This project is licensed under the **MIT License** &mdash; see [LICENSE](LICENSE) for details.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING](wiki/Contributing.md) before submitting a pull request.

---

<div align="center">

Made with &#x2764;&#xFE0F; for edge AI &mdash; built to run anywhere, privately.

</div>
