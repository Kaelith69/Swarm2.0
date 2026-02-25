<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 100" width="720" height="100" role="img" aria-label="API Reference header">
  <defs>
    <linearGradient id="apiBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B18"/>
      <stop offset="100%" stop-color="#0B1124"/>
    </linearGradient>
    <linearGradient id="apiAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
  </defs>
  <rect width="720" height="100" rx="12" fill="url(#apiBg)"/>
  <text x="360" y="42" text-anchor="middle" font-family="'Segoe UI',Arial,sans-serif" font-size="26" font-weight="700" fill="url(#apiAccent)">Swarm 2.0 — REST API Reference</text>
  <text x="360" y="66" text-anchor="middle" font-family="'Segoe UI',Arial,sans-serif" font-size="12" fill="#64748B">FastAPI · Version 2.0.0 · Base URL: http://&lt;host&gt;:8000</text>
  <line x1="80" y1="80" x2="640" y2="80" stroke="url(#apiAccent)" stroke-width="1" opacity="0.4"/>
</svg>

</div>

# REST API Reference

The Swarm 2.0 REST API is served by a single FastAPI application (`src/assistant/api.py`) on port `8000` (configurable via `PORT`). All endpoints return JSON.

**Base URL:** `http://<HOST>:<PORT>` (default `http://0.0.0.0:8000`)

---

## Endpoints at a Glance

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | None | Server liveness probe and capability report |
| `POST` | `/query` | None | Submit a message and receive an AI response |
| `POST` | `/webhook/telegram` | Optional secret | Ingest a Telegram Bot API update |
| `POST` | `/webhook/discord` | Ed25519 / Bearer | Ingest a Discord gateway event or interaction |

---

## `GET /health`

Returns the current liveness status, model configuration, and cloud provider availability.

**Authentication:** None required.

**Response `200 OK`:**

```json
{
  "ok": true,
  "model_path": "/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf",
  "llama_main_path": "/home/pi/llama.cpp/build/bin/llama-cli",
  "use_llm_routing": true,
  "bot_mode": "polling",
  "agent_name": "Aria",
  "hybrid": {
    "groq_enabled": true,
    "gemini_enabled": false,
    "kimi_enabled": false
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `ok` | `bool` | Always `true` when the server is healthy |
| `model_path` | `string` | Resolved path to the GGUF model file |
| `llama_main_path` | `string` | Resolved path to `llama-cli` / `llama-cli.exe` |
| `use_llm_routing` | `bool` | Whether Tier-3 LLM routing is active |
| `bot_mode` | `string` | `"polling"` or `"webhook"` |
| `agent_name` | `string` | Display name loaded from personality config |
| `hybrid.groq_enabled` | `bool` | `true` if `GROQ_API_KEY` is set |
| `hybrid.gemini_enabled` | `bool` | `true` if `GEMINI_API_KEY` is set |
| `hybrid.kimi_enabled` | `bool` | `true` if `KIMI_API_KEY` is set |

**Example:**

```bash
curl http://127.0.0.1:8000/health
```

---

## `POST /query`

Submit a user message and receive the AI-generated response, including the routing decision.

**Authentication:** None required.

> ⚠️ If you expose this endpoint over a network, add a reverse-proxy auth layer. There is no built-in authentication for `/query`.

**Request body (`application/json`):**

```json
{
  "message": "Analyze the trade-offs between REST and GraphQL"
}
```

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `message` | `string` | ✅ | 1–`MAX_INPUT_CHARS` chars (default 8000) | The user's query |

**Response `200 OK`:**

```json
{
  "route": "groq",
  "reason": "kw_reasoning",
  "response": "REST and GraphQL each have distinct trade-offs..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `route` | `string` | The inference backend that handled this message (see table below) |
| `reason` | `string` | Human-readable classification reason (see table below) |
| `response` | `string` | The generated response text |

**`route` values:**

| `route` | Backend | Description |
|---------|---------|-------------|
| `local_simple` | llama.cpp | Local inference — short message or default |
| `local_rag` | llama.cpp + RAG | Local inference with retrieved knowledge context |
| `local_fallback` | llama.cpp | Cloud was configured but unavailable; fell back to local |
| `groq` | Groq API | Cloud inference via Groq (reasoning queries) |
| `gemini` | Gemini API | Cloud inference via Google Gemini (long context) |
| `kimi` | Kimi/Moonshot API | Cloud inference via Kimi (planning queries) |

**`reason` values:**

| `reason` | Routing tier | Explanation |
|----------|-------------|-------------|
| `short_message` | Tier 1 | Message length ≤ `LOCAL_SHORT_THRESHOLD_CHARS` and no complex signal |
| `kw_planning` | Tier 2 | Contains planning keywords (`plan`, `roadmap`, `strategy`, `workflow`) |
| `kw_long_context` | Tier 2 | Message length ≥ `LONG_CONTEXT_THRESHOLD_CHARS` |
| `kw_reasoning` | Tier 2 | Contains reasoning keywords (`analyze`, `compare`, `tradeoff`, etc.) |
| `kw_rag` | Tier 2 | Contains retrieval keywords (`docs`, `document`, `knowledge base`, etc.) |
| `llm_classifier` | Tier 3 | Local Gemma model classified this as a cloud-bound query |
| `llm_classifier_local` | Tier 3 | Local Gemma model classified this as a local query |
| `default` | — | No signal found; routed to local as default |
| `groq_unavailable` | Tier 4 | Groq was targeted but key missing or API failed |
| `gemini_unavailable` | Tier 4 | Gemini was targeted but key missing or API failed |
| `kimi_unavailable` | Tier 4 | Kimi was targeted but key missing or API failed |
| `cloud_unavailable` | Tier 4 | Generic cloud fallback |
| `unmatched_target` | — | Internal routing fallthrough (should not occur in practice) |

**Error responses:**

| Status | Condition | Body |
|--------|-----------|------|
| `400 Bad Request` | `message` is empty or whitespace-only | `{"detail":"message is required"}` |
| `413 Request Entity Too Large` | `message` exceeds `MAX_INPUT_CHARS` | `{"detail":"message exceeds 8000 chars"}` |

**Examples:**

```bash
# Simple local query
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'

# Reasoning → routes to Groq
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze the trade-offs between REST and GraphQL APIs"}'

# Planning → routes to Kimi
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a roadmap for migrating our monolith to microservices"}'
```

---

## `POST /webhook/telegram`

Receives an update payload from the Telegram Bot API and delivers a response back to the user's chat.

This endpoint is used in **webhook mode** (`BOT_MODE=webhook`). In polling mode, this endpoint still exists but is not normally called — the bot polls Telegram's `getUpdates` API directly.

**Authentication:** Optional `TELEGRAM_SECRET` header check.

If `TELEGRAM_SECRET` is configured, the request must include the header:
```
X-Telegram-Bot-Api-Secret-Token: <your-secret>
```
Requests with a missing or incorrect secret are rejected with `401 Unauthorized`.

**Request body:** A [Telegram Update object](https://core.telegram.org/bots/api#update) (JSON).

```json
{
  "update_id": 100000001,
  "message": {
    "message_id": 42,
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Alice"
    },
    "chat": {
      "id": 123456789,
      "type": "private"
    },
    "date": 1700000000,
    "text": "What is the weather like today?"
  }
}
```

**Response `200 OK` (message processed):**

```json
{
  "status": "ok",
  "route": "local_simple",
  "reason": "short_message",
  "response": "I don't have live weather data, but I can help with...",
  "delivery": {
    "sent": true
  }
}
```

**Response `200 OK` (update ignored — no text content):**

```json
{
  "status": "ignored"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | `"ok"` if processed, `"ignored"` if no usable text was found |
| `route` | `string` | Routing decision (same values as `/query`) |
| `reason` | `string` | Routing reason (same values as `/query`) |
| `response` | `string` | Generated response sent to the user |
| `delivery.sent` | `bool` | `true` if the Telegram `sendMessage` call succeeded |
| `delivery.reason` | `string` | Present only when `sent` is `false` — error description |
| `delivery.status_code` | `int` | HTTP status from Telegram API (only if Telegram returned an error) |

**Error responses:**

| Status | Condition |
|--------|-----------|
| `400 Bad Request` | Message text is empty after parsing |
| `401 Unauthorized` | `TELEGRAM_SECRET` is configured and the header is missing/wrong |
| `413 Request Entity Too Large` | Message text exceeds `MAX_INPUT_CHARS` |

**Register the webhook with Telegram:**

```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://your-domain.com/webhook/telegram" \
  -d "secret_token=<TELEGRAM_SECRET>"
```

---

## `POST /webhook/discord`

Receives Discord interaction events (slash commands, message components) or gateway webhook events and responds to the user.

**Authentication:** Ed25519 signature verification (recommended) or Bearer token (legacy).

### Ed25519 Verification (recommended for production)

Discord signs every interaction webhook request. When `DISCORD_PUBLIC_KEY` is configured, the server verifies the signature using `PyNaCl`. Requests that fail verification are rejected with `401 Unauthorized`.

Required headers from Discord:
```
X-Signature-Ed25519: <hex-encoded-signature>
X-Signature-Timestamp: <unix-timestamp>
```

### Bearer Token (legacy)

When `DISCORD_BEARER_TOKEN` is configured (and `DISCORD_PUBLIC_KEY` is not), the server checks:
```
Authorization: Bearer <token>
```

### PING / PONG (type 1)

Discord sends a `type: 1` PING when registering an interactions endpoint. The server responds immediately with `{"type": 1}` without routing the message.

**Request body:** A [Discord Interaction object](https://discord.com/developers/docs/interactions/receiving-and-responding) or a custom webhook payload (JSON).

```json
{
  "type": 2,
  "data": {
    "name": "chat",
    "options": [
      { "name": "message", "value": "Summarize the quarterly report" }
    ]
  },
  "member": {
    "user": { "id": "987654321", "username": "Bob" }
  },
  "channel_id": "111222333444555666"
}
```

**Response `200 OK` — Discord Interaction (type 2):**

```json
{
  "type": 4,
  "data": {
    "content": "The quarterly report highlights..."
  }
}
```

Discord requires `type: 4` (`CHANNEL_MESSAGE_WITH_SOURCE`) to display the response inline. The `content` field is truncated to 2000 characters (Discord limit).

**Response `200 OK` — Custom webhook (not a Discord Interaction):**

```json
{
  "status": "ok",
  "route": "gemini",
  "reason": "kw_long_context",
  "response": "The quarterly report highlights...",
  "delivery": {
    "sent": true
  }
}
```

**Response `200 OK` — PING:**

```json
{ "type": 1 }
```

**Error responses:**

| Status | Condition |
|--------|-----------|
| `400 Bad Request` | Invalid JSON body |
| `400 Bad Request` | Message text is empty after parsing |
| `401 Unauthorized` | Ed25519 signature verification failed |
| `401 Unauthorized` | Bearer token mismatch |
| `413 Request Entity Too Large` | Message text exceeds `MAX_INPUT_CHARS` |
| `500 Internal Server Error` | `DISCORD_PUBLIC_KEY` set but `PyNaCl` not installed |

**Register the interactions endpoint in the Discord Developer Portal:**

1. Navigate to your application → **General Information** → copy **Public Key** → set as `DISCORD_PUBLIC_KEY` in `.env`.
2. Under **Interactions Endpoint URL**, enter: `https://your-domain.com/webhook/discord`.
3. Discord will send a PING and verify the server responds with `{"type":1}`.

---

## Conversation Memory and User IDs

The `/query` endpoint uses `user_id="api"` for all requests — a single shared memory slot. If you need per-user memory via the REST API, use the `/webhook/telegram` or `/webhook/discord` endpoints, which derive `user_id` from `tg:<user_id>` and `dc:<user_id>` respectively.

---

## Rate Limiting and Input Constraints

| Setting | Default | Description |
|---------|---------|-------------|
| `MAX_INPUT_CHARS` | `8000` | Maximum characters per message; 413 returned if exceeded |
| `MAX_RESPONSE_TOKENS` | `256` | Maximum tokens the local LLM will generate |
| `CLOUD_TIMEOUT_SECONDS` | `25` | Timeout for cloud API calls |
| `LLAMA_TIMEOUT_SECONDS` | `120` | Timeout for the llama.cpp subprocess |

There is no built-in rate limiter. Add one at the reverse-proxy layer (nginx `limit_req`, Cloudflare Rate Limiting, etc.) if exposing the API publicly.

---

## OpenAPI / Swagger UI

FastAPI automatically generates interactive API documentation:

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/docs` | Swagger UI — interactive endpoint explorer |
| `http://127.0.0.1:8000/redoc` | ReDoc — clean reference documentation |
| `http://127.0.0.1:8000/openapi.json` | Raw OpenAPI 3.0 schema |

---

## Error Response Format

All error responses follow FastAPI's default format:

```json
{
  "detail": "message is required"
}
```

HTTP status codes used:

| Code | Meaning |
|------|---------|
| `200` | Success |
| `400` | Bad request (empty message, invalid JSON) |
| `401` | Authentication failure (webhook secret / signature mismatch) |
| `413` | Message too long |
| `500` | Server configuration error (e.g., missing `PyNaCl`) |
