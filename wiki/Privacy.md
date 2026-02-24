# Privacy & Security

Swarm 2.0 is designed with a **privacy-first** posture. This page documents what data is collected, where it lives, and how to operate the system securely.

---

## Data Inventory

| Data | Storage location | Leaves device? |
|------|-----------------|----------------|
| User messages | SQLite (`.venv/`-adjacent or `RAG_DATA_DIR`) | Only when cloud API key is set |
| Conversation history | SQLite | Never |
| RAG document embeddings | HNSW index file + SQLite | Never |
| API keys | `.env` file on disk | Used only for outbound API calls |
| LLM inference input | subprocess stdin → llama-cli | Never (local); cloud API call (cloud route) |

---

## Local-Only Mode

When **no cloud API keys** are configured, the system operates entirely on-device:

- All inference is performed by `llama-cli` as a local subprocess.
- No network connections are made by the AI pipeline.
- SQLite is the only persistence layer.
- User messages never leave the machine.

To confirm local-only mode, check that your `.env` has no `GROQ_API_KEY`, `GEMINI_API_KEY`, or `KIMI_API_KEY` set.

---

## Cloud Mode Data Handling

When cloud provider keys are configured, messages routed to cloud providers are sent over HTTPS to third-party APIs:

| Provider | Data sent | Policy |
|----------|-----------|--------|
| Groq | Prompt + system message | [Groq Privacy Policy](https://groq.com/privacy-policy/) |
| Google Gemini | Prompt + system message | [Google AI Policy](https://policies.google.com/privacy) |
| Kimi/Moonshot | Prompt + system message | [Moonshot Privacy Policy](https://www.moonshot.ai/privacy) |

> **Important:** Review each provider's data retention and training policies before enabling them in production environments that handle sensitive data.

The routing cascade is transparent: every response includes a `route` and `reason` field so you always know which backend processed a message.

---

## `.env` File Security

The `.env` file contains all secrets. Follow these practices:

```bash
# Restrict permissions immediately after creation
chmod 600 .env

# Never commit it
echo ".env" >> .gitignore

# Verify it is not tracked
git status .env   # should show 'nothing to commit'
```

The repository's `.gitignore` already excludes `.env`. Do not override this.

---

## Bot Security

### Telegram Webhook Verification

Set `TELEGRAM_SECRET` in `.env` to a random string:

```env
TELEGRAM_SECRET=long-random-string-here
```

The server verifies the `X-Telegram-Bot-Api-Secret-Token` header on every incoming webhook request. Requests without the correct token are rejected with HTTP 403.

### Discord Interaction Verification

Set `DISCORD_PUBLIC_KEY` in `.env`:

```env
DISCORD_PUBLIC_KEY=your-app-public-key-from-dev-portal
```

The server verifies the Ed25519 signature (`X-Signature-Ed25519` + `X-Signature-Timestamp`) on every incoming Discord interaction using the `PyNaCl` library. Requests that fail verification are rejected with HTTP 401.

> Discord requires this verification for registered interactions endpoints. If `DISCORD_PUBLIC_KEY` is not set, signature verification is skipped (suitable for local development only).

---

## Error Exposure

```env
EXPOSE_DELIVERY_ERRORS=false   # default
```

With this set to `false` (the default), internal Python exceptions and stack traces are never forwarded to users via bot responses. The user receives a generic error message while the full trace appears only in the server log.

Set to `true` only during local debugging.

---

## SQLite Security

The SQLite database files contain conversation history. To protect them:

- Store them on an encrypted volume (e.g. LUKS on Pi).
- Restrict file permissions: `chmod 600 *.db`.
- Back up and rotate periodically if handling sensitive conversations.

Configure the storage path:

```env
RAG_DATA_DIR=/opt/agentic-assistant/data
```

---

## Network Exposure

By default the API binds to `0.0.0.0:8000`. On a Pi connected to a local network this means any device on that network can reach the API.

For production deployments:

- Bind to `127.0.0.1` only, and proxy through Nginx with TLS:
  ```env
  API_HOST=127.0.0.1
  ```
- Use `deploy/nginx-agent.conf` as a starting point for TLS termination.
- Apply firewall rules (`ufw`) to restrict inbound access.

---

## Dependency Security

Dependencies are pinned in `requirements.txt`. Before upgrading, review changelogs for breaking changes and security advisories. The project uses:

- `PyNaCl` for cryptographic signature verification (Discord).
- `httpx` / `requests` for outbound HTTP — both use system CA store for TLS validation.

---

## Summary

| Control | Default | Notes |
|---------|---------|-------|
| Local-only inference | Yes (if no cloud keys) | Zero data egress |
| `.env` permissions | User-set | Must run `chmod 600` after creation |
| Telegram webhook token | Optional | Strongly recommended for production |
| Discord Ed25519 verify | Auto when `DISCORD_PUBLIC_KEY` set | Required by Discord for registered endpoints |
| Error exposure to users | Off | Set `EXPOSE_DELIVERY_ERRORS=false` |
| API network binding | `0.0.0.0` | Change to `127.0.0.1` + Nginx in production |
