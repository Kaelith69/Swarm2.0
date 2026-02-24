# Troubleshooting

This page covers the most common issues encountered when running Swarm 2.0 on Raspberry Pi 5 and Windows.

---

## Quick Diagnosis

```bash
# 1. Check the server is running
curl http://127.0.0.1:8000/health

# 2. Send a test message
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "ping"}'

# 3. View service logs (Pi / systemd)
sudo journalctl -u agent -n 50 --no-pager

# 4. Check Pi temperature
vcgencmd measure_temp

# 5. Check available RAM
free -h
```

---

## Startup Issues

### `ModuleNotFoundError: No module named 'assistant'`

**Cause:** `PYTHONPATH` is not set.

**Fix:**
```bash
export PYTHONPATH=/opt/agentic-assistant/agentic_assistant/src
# Or use the start script which sets this automatically
bash scripts/pi_start_and_check.sh
```

---

### `FileNotFoundError: [Errno 2] No such file or directory: '/home/pi/llama.cpp/build/bin/llama-cli'`

**Cause:** `LLAMA_MAIN_PATH` in `.env` points to a path that does not exist.

**Fix:**
```bash
# Find the actual binary
find ~ -name "llama-cli" 2>/dev/null

# Update .env
LLAMA_MAIN_PATH=/actual/path/to/llama-cli
```

---

### `FileNotFoundError: model file not found`

**Cause:** `MODEL_PATH` in `.env` is incorrect.

**Fix:**
```bash
ls ~/models/        # verify model filename
# Update MODEL_PATH in .env to match the exact filename
```

---

### Server starts but `/health` returns connection refused

**Cause:** The server may still be loading (model loading can take 10–30 seconds on Pi).

**Fix:** Wait 30 seconds and retry. Check logs for errors:
```bash
sudo journalctl -u agent -f
```

---

## Inference Issues

### Local inference returns empty or truncated responses

**Cause:** `MAX_RESPONSE_TOKENS` may be too low, or `LLM_CONTEXT_TOKENS` is exhausted.

**Fix:**
```env
MAX_RESPONSE_TOKENS=512
LLM_CONTEXT_TOKENS=2048
```

---

### Inference is very slow (> 30s on Pi)

**Causes:**
- Thermal throttling (CPU frequency reduced at 80 °C)
- SD card used instead of NVMe
- `INFERENCE_THREADS` not set to 4

**Fix:**
```bash
# Check temperature
vcgencmd measure_temp

# Check CPU frequency
vcgencmd get_throttled   # 0x0 = healthy; non-zero = throttling

# Ensure active cooling is working
# Update .env:
INFERENCE_THREADS=4
```

---

### Cloud route returns `local_fallback`

**Cause:** Cloud API key is missing or invalid, or the provider API returned an error.

**Fix:**
```bash
# Test your Groq key directly
curl -H "Authorization: Bearer $GROQ_API_KEY" \
  https://api.groq.com/openai/v1/models

# Check .env has the correct key name
GROQ_API_KEY=gsk_...
```

---

## Bot Issues

### Telegram bot not responding

**Check 1 — Polling mode:** Is `BOT_MODE=polling` set in `.env`?

**Check 2 — Token:** Is `TELEGRAM_BOT_TOKEN` correct? Test with:
```bash
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
```

**Check 3 — Webhook conflicts:** If you previously set a webhook and now want polling:
```bash
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/deleteWebhook"
```

---

### Telegram webhook returns 403

**Cause:** The `X-Telegram-Bot-Api-Secret-Token` header does not match `TELEGRAM_SECRET` in `.env`.

**Fix:** Ensure the secret you set when registering the webhook matches `TELEGRAM_SECRET` exactly.

---

### Discord bot ignores messages

**Check 1:** Is `DISCORD_BOT_TOKEN` correct?

**Check 2 — Gateway mode:** Does the bot have the `MESSAGE CONTENT` privileged intent enabled in the Discord Developer Portal?

**Check 3 — Webhook mode:** Is `DISCORD_PUBLIC_KEY` set? Is the Interactions Endpoint URL registered and verified?

```bash
# Test endpoint verification manually
curl -X POST https://yourdomain.com/webhook/discord \
  -H "Content-Type: application/json" \
  -d '{"type": 1}'
# Should return {"type": 1}
```

---

### Discord webhook returns 401

**Cause:** Ed25519 signature verification is failing.

**Fix:** Ensure `DISCORD_PUBLIC_KEY` in `.env` matches the **Public Key** shown in the Discord Developer Portal → General Information tab (not the application ID).

---

## Memory / SQLite Issues

### `sqlite3.OperationalError: database is locked`

**Cause:** Multiple processes are accessing the SQLite database simultaneously.

**Fix:** Swarm 2.0 **must** run with a single Uvicorn worker. Never start with `--workers N` where N > 1. The `agent.service` and start scripts enforce single-worker mode.

---

### Conversation history not persisting across restarts

**Check:** Is `RAG_DATA_DIR` set to a persistent path (not `/tmp`)?

```env
RAG_DATA_DIR=/opt/agentic-assistant/agentic_assistant/data
```

---

## RAG Issues

### RAG returns no results / `rag_used: false` for all queries

**Cause 1:** No documents have been ingested.

**Fix:**
```bash
python scripts/ingest_documents.py data/knowledge --source knowledge_base
```

**Cause 2:** The query does not contain RAG-triggering keywords.

**Fix:** Include `retrieve`, `docs`, `document`, `knowledge base` in the query, or set `USE_LLM_ROUTING=true` to allow the classifier to determine RAG intent.

---

## Windows-Specific Issues

### PowerShell script blocked by execution policy

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1
```

---

### `llama-cli.exe` not found

Ensure you built llama.cpp with the Release configuration and the binary is at the path set in `LLAMA_MAIN_PATH`. Use forward slashes or escaped backslashes in `.env`:

```env
LLAMA_MAIN_PATH=C:/llama.cpp/build/bin/Release/llama-cli.exe
```

---

## Getting More Help

1. Check the [GitHub Issues](https://github.com/Kaelith69/Swarm2.0/issues) for known issues.
2. Review the [Architecture](Architecture) page to understand the component that is failing.
3. Enable debug logging:
   ```bash
   uvicorn assistant.api:app --host 0.0.0.0 --port 8000 --log-level debug
   ```
4. Open a new issue with: platform, Python version, sanitised `.env`, and full log output.
