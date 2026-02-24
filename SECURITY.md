# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 2.x (current) | ✅ Yes |
| 1.x | ❌ No — upgrade to 2.x |

---

## Reporting a Vulnerability

Found something sketchy? We appreciate responsible disclosure.

**Please do NOT open a public GitHub issue for security vulnerabilities.** If the bug is exploitable, making it public before there's a fix creates a window where users are exposed. That's bad.

Instead:

1. **Email** the maintainer directly. Check the GitHub profile for contact info, or use the repository's private security advisory feature.
2. **GitHub Private Advisory** — on the repository page, go to **Security → Advisories → Report a vulnerability**. This creates a private discussion only visible to you and the maintainers.

### What to include in your report

- Description of the vulnerability and what it allows an attacker to do
- Steps to reproduce (the more specific, the faster we can fix it)
- Affected version(s)
- Any suggested mitigations or patches you've already thought of

### Response timeline

- **Acknowledgement**: within 48 hours (usually faster)
- **Initial assessment**: within 5 business days
- **Fix timeline**: depends on severity — critical issues get priority

We'll keep you updated throughout the process and credit you in the changelog (unless you prefer to stay anonymous).

---

## Known Security Design Decisions

These are intentional behaviors, not vulnerabilities. But if you think the reasoning is wrong, tell us anyway.

### API keys in `.env`

API keys (Groq, Gemini, Kimi, Telegram, Discord) are stored in a `.env` file that is excluded from git via `.gitignore`. On Linux, the installer sets `chmod 600 .env`. On Windows, restrict file permissions via NTFS.

**Risk**: If an attacker has local filesystem access, they can read `.env`. This is a fundamental risk for any secret stored on disk. Mitigation: use an OS-level secret manager or vault if you need stronger guarantees.

### SQLite for memory and RAG

The application uses SQLite (single-file databases) for conversation memory and RAG metadata. These files live in `RAG_DATA_DIR` and contain conversation history and ingested document content.

**Risk**: If `RAG_DATA_DIR` is world-readable, conversation data is accessible. Set appropriate filesystem permissions.

### Single-worker constraint

The application is explicitly single-worker (no `uvicorn --workers N`). This is a design choice for SQLite safety, not a bug. Running multiple workers sharing the same SQLite files would lead to data corruption or race conditions.

### Discord signature verification

When `DISCORD_PUBLIC_KEY` is set, the `/webhook/discord` endpoint verifies the Ed25519 signature on every request using PyNaCl. This is strongly recommended for production.

When `DISCORD_PUBLIC_KEY` is **not** set, signature verification is skipped. The optional `DISCORD_BEARER_TOKEN` provides a weaker bearer-token check. For production deployments, always set `DISCORD_PUBLIC_KEY`.

### `EXPOSE_DELIVERY_ERRORS`

Defaults to `false`. When false, raw error messages from downstream delivery failures (e.g. Telegram API errors) are sanitized before being returned in the response. This prevents internal error details from leaking to end users.

---

## Out of Scope

The following are **not** considered vulnerabilities for this project:

- Issues in upstream dependencies (`fastapi`, `llama.cpp`, `groq`, etc.) — report those to the relevant project
- Issues requiring physical access to the device where the server runs
- Denial of service via extremely large inputs (mitigated by `MAX_INPUT_CHARS`)
- The existential risk of running an AI assistant on a Raspberry Pi

---

*Thank you for helping keep Swarm2.0 and its users safe.* 🔒
