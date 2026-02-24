# Troubleshooting

Something broke. Let's fix it.

---

## Diagnostic Checklist

Before diving into specific issues, run these three commands. They tell you 90% of what's wrong.

```bash
# 1. Is the server even running?
curl http://127.0.0.1:8000/health

# 2. What do the server logs say?
# Linux/Pi:
journalctl -u agent -n 50 --no-pager
# or if running manually:
cat /tmp/agentic-assistant.log

# 3. Can it actually respond?
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

---

## Server Won't Start

### `ModuleNotFoundError: No module named 'assistant'`

You forgot to set `PYTHONPATH`.

```bash
# Linux
export PYTHONPATH=/opt/agentic-assistant/src
python -m assistant.agent

# Windows
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m assistant.agent
```

### `FileNotFoundError` on `llama-cli`

The `LLAMA_MAIN_PATH` doesn't exist. Either:
- Build `llama.cpp` (see [Installation](Installation.md))
- Or go cloud-only: leave `MODEL_PATH` and `LLAMA_MAIN_PATH` empty in `.env`. Local inference will fail gracefully and fall back to cloud.

```bash
# Verify the path exists
ls -la /home/pi/llama.cpp/build/bin/llama-cli
```

### `port 8000 already in use`

Something is already on port 8000.

```bash
# Find what's using port 8000
lsof -i :8000
# or on Windows:
netstat -ano | findstr :8000

# Kill it (replace PID with the actual PID)
kill <PID>
```

Or change the port: `PORT=8001` in `.env`.

### Virtual environment not found

```bash
# Recreate the venv
python3 -m venv .venv
source .venv/bin/activate  # Linux
# .\.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

---

## Bots Not Responding

### Telegram — no messages received

**Polling mode:**
1. Verify `BOT_MODE=polling` in `.env`
2. Verify `TELEGRAM_BOT_TOKEN` is set correctly
3. Check `/health` — is it reporting the bot mode correctly?
4. Make sure the bot was actually started (look for "Telegram polling bot started" in server logs)
5. Try messaging the bot from Telegram — wait up to 30 seconds for the long-poll cycle

**Webhook mode:**
1. Verify the webhook is registered: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
2. Verify the URL is HTTPS and publicly reachable
3. Check for auth failures: `TELEGRAM_SECRET` mismatch → 401 errors

### Discord — no messages received

**Polling mode:**
1. Verify `DISCORD_BOT_TOKEN` is correct
2. In the Discord Developer Portal → **Bot** → **Privileged Gateway Intents** → enable **Message Content Intent**. Without this, the bot sees messages but not their content.
3. Verify the bot has been invited to your server with the correct permissions
4. Check server logs for "Discord gateway bot started"

**Webhook mode:**
1. Set `DISCORD_PUBLIC_KEY` in `.env` — without it, Discord's signature verification will be skipped but Discord won't send interactions either if the endpoint fails verification
2. Make sure the Interactions Endpoint URL is set in the Developer Portal to `https://your-domain.com/webhook/discord`
3. Discord sends a PING (type 1) to verify your endpoint — check that `/health` works and the endpoint returns `{"type": 1}` for the ping

---

## Cloud Routes Not Working

### `groq_enabled: false` in `/health`

`GROQ_API_KEY` is empty or not set in `.env`. Check for:
- Trailing spaces
- Quotes around the value (don't quote values in `.env`)
- File not saved after editing

```bash
# Verify
grep GROQ_API_KEY .env
```

### Cloud API returning errors

Check the server logs for the actual error message from the provider. Common issues:
- **401 Unauthorized**: Invalid API key
- **429 Too Many Requests**: Rate limited — wait and retry
- **503 / timeout**: Provider is having issues — the system falls back to local automatically

### All cloud routes falling back to local

This is expected behavior when:
- The API key is missing
- The API call times out (after `CLOUD_TIMEOUT_SECONDS=25`)
- The provider returns an error

The `reason` field in the `/query` response tells you what happened: `groq_unavailable`, `gemini_unavailable`, or `kimi_unavailable`.

---

## Routing Issues

### Message is going to the wrong backend

The `/query` response includes `route` and `reason`. Use these to diagnose.

**Examples:**
- `reason: short_message` — message was ≤ 150 chars. If you want it to go elsewhere, make it longer or add keywords.
- `reason: kw_reasoning` — "analyze", "compare" or similar keyword was found. This is intentional.
- `reason: llm_classifier` — the local Gemma model made the call. It may be wrong sometimes. Disable with `USE_LLM_ROUTING=false` for purely deterministic routing.

**To debug routing:**
```bash
# Watch what keywords are triggering
echo '{"message": "plan a project roadmap"}' | curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" -d @-
# → reason: kw_planning → route: kimi
```

### LLM classifier making bad routing decisions

Set `USE_LLM_ROUTING=false` in `.env` to fall back to keyword-only routing. Restart the server. This skips Tier 3 entirely and only uses the keyword fast-path (Tier 2) with local fallback (Tier 4).

---

## Performance Issues (Raspberry Pi)

### Slow responses (local)

Local inference on Pi 5 typically takes 2–10 seconds. If it's consistently slower:

1. **Check temperature:** `vcgencmd measure_temp` — throttling begins at 80 °C. If you're over 80 °C, add cooling.
2. **Check model is on NVMe:** `RAG_DATA_DIR` should point to your NVMe mount, not the SD card.
3. **Reduce context:** Lower `LLM_CONTEXT_TOKENS=1024` and `MEMORY_MAX_TURNS=6` to reduce prompt size.
4. **Reduce tokens:** Lower `MAX_RESPONSE_TOKENS=128` for shorter responses.
5. **Disable LLM routing:** `USE_LLM_ROUTING=false` saves one classification inference call per ambiguous query.

### High RAM usage

Gemma 2B Q4_K_M uses ~1.6 GB RAM. Python + FastAPI + RAG embeddings add another 1–1.5 GB. Total: ~3 GB on a clean Pi 5.

If you're running close to the 8 GB limit:
- Lower `LLM_CONTEXT_TOKENS=1024`
- Lower `MEMORY_MAX_TURNS=5`
- Close other processes

### `llama-cli` subprocess timeout

If inference times out (default: `LLAMA_TIMEOUT_SECONDS=120`), the server returns a local fallback response. If timeouts are frequent:
- Reduce `MAX_RESPONSE_TOKENS`
- Reduce `LLM_CONTEXT_TOKENS`
- Add more aggressive cooling

---

## RAG Issues

### No RAG results / RAG context empty

Documents haven't been ingested yet. Run the ingestion script:

```bash
python scripts/ingest_documents.py data/knowledge --source knowledge_base
```

Check that documents are actually in `data/knowledge/`. The script only reads `.txt`, `.md`, and `.pdf` files.

### HNSW index corrupted or missing

Delete and rebuild:

```bash
# Linux / Pi
rm -rf data/rag
python scripts/ingest_documents.py data/knowledge --source knowledge_base

# Windows
Remove-Item -Recurse -Force data\rag
.\.venv\Scripts\python.exe scripts\ingest_documents.py data\knowledge --source knowledge_base
```

### RAG returning irrelevant results

The default model (`all-MiniLM-L6-v2`) is a general-purpose embedding model. For domain-specific content, consider changing `EMBEDDING_MODEL` to a domain-appropriate model. Note: changing the model requires re-ingesting all documents (the vectors are incompatible between models).

---

## Memory Issues

### Assistant not remembering previous messages

1. Check `MEMORY_MAX_TURNS` — if set to 0, memory is disabled
2. Verify the `user_id` is consistent — Telegram and Discord use platform-specific IDs; direct API calls always use `api` (all direct API calls share the same memory)
3. Check that `RAG_DATA_DIR` is writable

### Memory bleeding between users

Each user has their own memory keyed by `user_id`. This should not happen unless something is reusing the same `user_id`. Check your bot configuration.

---

## Windows-Specific Issues

### PowerShell execution policy error

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or run scripts with the explicit bypass:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1
```

### `llama-cli.exe` not found

Build `llama.cpp` on Windows (see [Installation](Installation.md)), or use cloud-only mode by leaving `MODEL_PATH` and `LLAMA_MAIN_PATH` empty.

### Unicode / encoding errors in logs

Set environment variable `PYTHONIOENCODING=utf-8` before running the server.

---

## Still Stuck?

Open a [GitHub Issue](https://github.com/Kaelith69/Swarm2.0/issues) with:
1. Your OS and Python version
2. The error message (full stack trace if available)
3. The relevant lines from your `.env` (with secrets redacted)
4. What you've already tried

The more context you provide, the faster we can help.
