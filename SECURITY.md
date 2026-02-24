# Security Policy

## Supported Versions

The following versions of Swarm 2.0 currently receive security updates:

| Version | Supported |
|---------|-----------|
| 2.x (latest) | ✅ Yes |
| 1.x | ❌ No — please upgrade |

---

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

A public issue exposes the vulnerability to everyone before a fix is available, which is exactly the outcome we're trying to avoid.

### How to Report

1. **Email**: Send a detailed report to the repository owner via GitHub's private vulnerability reporting feature, or open a [GitHub Security Advisory](https://github.com/Kaelith69/Swarm2.0/security/advisories/new) directly.

2. **What to include** in your report:
   - A clear description of the vulnerability
   - The component or file affected (e.g., `src/assistant/api.py`, Discord webhook handler)
   - Steps to reproduce or a proof-of-concept (redact any sensitive data)
   - Your assessment of the impact (data exposure, authentication bypass, RCE, etc.)
   - Any suggested mitigations if you have them

3. **Response timeline**:
   - You will receive an acknowledgement within **48 hours**.
   - We aim to triage and confirm the vulnerability within **7 days**.
   - Patches for confirmed critical issues will be prioritised and released as soon as practicable.

4. **Coordinated disclosure**: We ask that you allow us reasonable time to release a fix before publishing details publicly. We will credit you in the changelog and release notes unless you prefer to remain anonymous.

---

## Security Model Overview

Understanding how Swarm 2.0 handles data will help you assess what to look for:

### What stays local (always)
- Conversation memory — stored in SQLite on the host device only.
- Ingested RAG documents — stored in HNSW index and SQLite metadata on the host device.
- Model weights — local GGUF files, never transmitted.
- API keys — stored in `.env` (mode `600`), never logged, never included in responses.

### What may leave the device
- When cloud API keys are configured, message text and constructed prompts are sent to the configured provider (Groq, Google Gemini, Kimi/Moonshot) over HTTPS. No other data is included.
- In local-only mode (no cloud keys set), **nothing leaves the device**.

### Authentication
- **Discord**: Interaction webhook requests are verified using Ed25519 signatures via `PyNaCl`. Requests that fail signature verification are rejected with HTTP 401.
- **Telegram**: Webhook endpoint supports a configurable secret token (`TELEGRAM_SECRET`). Polling mode does not require inbound auth.
- **REST API**: No authentication is included by default. If you expose the FastAPI server to a network, you are responsible for adding appropriate auth (reverse proxy, network firewall, API key middleware).

### Known Scope Boundaries
- The REST API (`/query`, `/ingest`) has **no built-in authentication**. Deployers must secure this endpoint if it is network-accessible. This is a deployment concern, not a vulnerability.
- SQLite is accessed from a **single Uvicorn worker**. Multi-process deployments are not supported and would introduce data integrity issues.

---

## Dependency Vulnerabilities

If you discover a vulnerability in one of Swarm 2.0's dependencies (e.g., `fastapi`, `python-telegram-bot`, `discord.py`), please report it to the upstream project and also notify us so we can prioritise a dependency update.

---

## Credits

We appreciate responsible disclosure. Reporters who follow this policy will be credited in the [CHANGELOG](CHANGELOG.md) under the relevant release's Security section, unless they request anonymity.
