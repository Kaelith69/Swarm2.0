# Privacy

Where your data goes, where it doesn't, and what controls you have.

---

## The Short Version

- **Local routes:** Your message never leaves your device.
- **Cloud routes:** Your message goes to a third-party API over HTTPS.
- **Conversation memory:** Stored in SQLite on your device. Not synced anywhere.
- **RAG data:** Stored in hnswlib + SQLite on your device. Your documents don't leave.

---

## Local Inference (On-Device)

When a message routes to `local_simple`, `local_rag`, or `local_fallback`:

1. The message (and any RAG context + conversation history) is passed to the `llama-cli` binary as a subprocess argument.
2. `llama-cli` runs the Gemma model entirely on your hardware.
3. The response comes back through `stdout`.
4. **Nothing leaves the device.** No network calls are made.

This is the default for short messages (≤ 150 characters) and RAG-specific queries. If you configure no cloud API keys, 100% of traffic stays local.

**Who gets your data:** Nobody. It's on your CPU.

---

## Cloud Inference

When a message routes to `groq`, `gemini`, or `kimi`, the following data is sent to the provider:

- Your message text
- Retrieved RAG context (top-3 chunks from your ingested documents)
- Conversation history (last N turns)
- The personality system prompt

This data is transmitted over HTTPS. The contents are subject to each provider's privacy policy and terms of service:

| Provider | Privacy Policy | Terms |
|---|---|---|
| Groq | [groq.com/privacy-policy](https://groq.com/privacy-policy/) | [groq.com/terms-of-use](https://groq.com/terms-of-use/) |
| Google Gemini | [ai.google.dev/gemini-api/terms](https://ai.google.dev/gemini-api/terms) | [policies.google.com/privacy](https://policies.google.com/privacy) |
| Kimi / Moonshot | [platform.moonshot.cn/docs](https://platform.moonshot.cn/docs) | Check their developer console |

**Key questions to ask each provider:**
- Do they use your inputs to train their models?
- How long do they retain request data?
- What data residency options exist?

These answers vary by provider and change over time. Check their current policies.

**How to avoid cloud routes:**
- Set `USE_LLM_ROUTING=false` to disable the LLM classifier (Tier 3 cloud routing)
- Leave all cloud API keys empty (`GROQ_API_KEY=`, `GEMINI_API_KEY=`, `KIMI_API_KEY=`)
- With no cloud keys, all cloud routes fail and fall back to `local_fallback`

---

## Conversation Memory

Conversation history is stored in `RAG_DATA_DIR/memory.sqlite3` on your device.

- **Content stored:** `user_id`, `role` (user/assistant), `content` (message text), `timestamp`
- **Location:** Your device only — not transmitted anywhere
- **Retention:** Kept until you clear it or delete the file
- **Who has access:** Anyone with filesystem access to `RAG_DATA_DIR`

**Recommendations:**
- On Linux: `chmod 700 data/rag/` to restrict access to your user
- On Windows: Set NTFS permissions on the `data\rag\` directory
- Back up regularly if you care about the conversation history
- Clear a user's history with `ConversationMemory.clear(user_id)` if needed

---

## RAG Data (Ingested Documents)

Documents you ingest are stored as:
- Embeddings in `data/rag/index.bin` (hnswlib binary format)
- Chunk text and metadata in `data/rag/metadata.sqlite3`

These files live on your device. The ingested content is sent to cloud models as part of the RAG context when cloud routes are used (see Cloud Inference above).

If your documents contain sensitive information:
- Use only local routes (remove cloud API keys)
- Restrict filesystem permissions on `data/rag/`
- Consider whether the documents should be ingested at all

---

## API Keys

API keys (Groq, Gemini, Kimi, Telegram, Discord) are stored in the `.env` file.

- `.env` is excluded from git by `.gitignore` (both root and `agentic_assistant/`)
- On Linux: the installer sets `chmod 600 .env` — only your user can read it
- On Windows: restrict file permissions via NTFS

**Never commit `.env` to git.** The `.gitignore` prevents this by default, but be vigilant when creating PRs or publishing the repository.

**Rotation:** Rotate your API keys regularly. If you believe a key has been leaked, rotate it immediately in the respective provider's console.

---

## Webhook Security

### Telegram

When `TELEGRAM_SECRET` is set, the `/webhook/telegram` endpoint verifies the `X-Telegram-Bot-Api-Secret-Token` header on every request. Requests without the correct token receive a 401 response.

### Discord

When `DISCORD_PUBLIC_KEY` is set, the `/webhook/discord` endpoint verifies the `X-Signature-Ed25519` + `X-Signature-Timestamp` headers using Ed25519 cryptographic signature verification (via PyNaCl). This is the recommended production configuration.

If `DISCORD_PUBLIC_KEY` is not set, signature verification is skipped. The optional `DISCORD_BEARER_TOKEN` provides a weaker bearer-token check. For any production deployment, **set `DISCORD_PUBLIC_KEY`**.

---

## Network Exposure

By default, the FastAPI server binds to `0.0.0.0` (all interfaces), making it accessible on your local network.

**Recommendations:**
- On a home Pi: consider setting `HOST=127.0.0.1` if you only need localhost access, or use firewall rules to restrict port 8000
- For public exposure: use an nginx reverse proxy with TLS (see `deploy/nginx-agent.conf`)
- Never expose port 8000 directly to the internet without TLS and authentication

---

## What We Don't Collect

Swarm2.0 is self-hosted software. There is no telemetry, analytics, or phone-home behavior built into the codebase. The only outbound network calls are:

1. Explicit API calls to Groq / Gemini / Kimi (when configured and triggered)
2. Telegram/Discord API calls to send bot responses
3. `llama.cpp` subprocess — no network access

That's it. No usage stats. No crash reports. No "anonymous telemetry". Nothing.

---

## GDPR / Data Subject Requests

If you're deploying this as a service and collecting data on behalf of others, you are responsible for:

- Informing users about data processing
- Handling data subject rights (access, deletion, portability)
- Appropriate data retention policies

The `ConversationMemory.clear(user_id)` method is the mechanism for user data deletion. The `RAG_DATA_DIR` can be cleared to remove all stored knowledge.

This project does not provide a built-in GDPR compliance layer. That's on you, deployer.
