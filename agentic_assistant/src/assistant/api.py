from __future__ import annotations

import logging

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from assistant.config import settings
from assistant.llm.cloud_router import CloudConfig, CloudRouter
from assistant.llm.llama_cpp_runner import LlamaCppRunner
from assistant.memory import ConversationMemory
from assistant.messaging.parsers import parse_discord, parse_telegram
from assistant.messaging.senders import OutboundSenders
from assistant.orchestrator import AgentOrchestrator
from assistant.rag.store import RagStore

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singleton service objects
# ---------------------------------------------------------------------------

rag_store = RagStore(settings.rag_data_dir, settings.embedding_model)

llm_runner = LlamaCppRunner(
    executable_path=settings.llama_main_path,
    model_path=settings.model_path,
    threads=settings.inference_threads,
    context_tokens=settings.llm_context_tokens,
    max_tokens=settings.max_response_tokens,
    temperature=settings.llm_temperature,
    timeout_seconds=settings.llama_timeout_seconds,
)

cloud_router = CloudRouter(
    CloudConfig(
        groq_api_key=settings.groq_api_key,
        groq_model=settings.groq_model,
        gemini_api_key=settings.gemini_api_key,
        gemini_model=settings.gemini_model,
        kimi_api_key=settings.kimi_api_key,
        kimi_base_url=settings.kimi_base_url,
        kimi_model=settings.kimi_model,
        timeout_seconds=settings.cloud_timeout_seconds,
    )
)

memory = ConversationMemory(
    data_dir=settings.rag_data_dir,
    max_turns=settings.memory_max_turns,
)

orchestrator = AgentOrchestrator(
    rag=rag_store,
    llm=llm_runner,
    cloud=cloud_router,
    memory=memory,
    top_k=settings.rag_top_k,
    long_context_threshold_chars=settings.long_context_threshold_chars,
    short_message_threshold_chars=settings.local_short_threshold_chars,
    use_llm_routing=settings.use_llm_routing,
)

senders = OutboundSenders(
    telegram_bot_token=settings.telegram_bot_token,
    discord_bot_token=settings.discord_bot_token,
)

app = FastAPI(title="Pi Agentic Assistant", version="2.0.0")


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    message: str


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _validate_message_or_400(message: str) -> str:
    cleaned = message.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="message is required")
    if len(cleaned) > settings.max_input_chars:
        raise HTTPException(status_code=413, detail=f"message exceeds {settings.max_input_chars} chars")
    return cleaned


def _safe_delivery(delivery: dict) -> dict:
    if settings.expose_delivery_errors or delivery.get("sent") is True:
        return delivery
    safe: dict = {"sent": False, "reason": str(delivery.get("reason", "delivery_failed"))}
    if "status_code" in delivery:
        safe["status_code"] = delivery["status_code"]
    return safe


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "model_path": str(settings.model_path),
        "llama_main_path": str(settings.llama_main_path),
        "use_llm_routing": settings.use_llm_routing,
        "hybrid": {
            "groq_enabled": cloud_router.is_groq_available(),
            "gemini_enabled": cloud_router.is_gemini_available(),
            "kimi_enabled": cloud_router.is_kimi_available(),
        },
    }


@app.post("/query")
def query(req: QueryRequest) -> dict:
    message = _validate_message_or_400(req.message)
    result = orchestrator.respond_with_route(message, user_id="api")
    return {"route": result.route, "reason": result.reason, "response": result.response}


# ---------------------------------------------------------------------------
# Telegram webhook
# ---------------------------------------------------------------------------

@app.post("/webhook/telegram")
def telegram_webhook(
    payload: dict,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict:
    if settings.telegram_secret and x_telegram_bot_api_secret_token != settings.telegram_secret:
        raise HTTPException(status_code=401, detail="invalid telegram secret")

    parsed = parse_telegram(payload)
    if not parsed:
        return {"status": "ignored"}

    user_id, text = parsed
    text = _validate_message_or_400(text)
    result = orchestrator.respond_with_route(text, user_id=f"tg:{user_id}")

    # Extract chat_id cleanly
    msg_obj = payload.get("message") or payload.get("edited_message") or {}
    chat_id = str((msg_obj.get("chat") or {}).get("id", ""))

    outbound = (
        senders.send_telegram(chat_id=chat_id, text=result.response)
        if chat_id
        else {"sent": False, "reason": "chat_id missing"}
    )
    return {
        "status": "ok",
        "route": result.route,
        "reason": result.reason,
        "response": result.response,
        "delivery": _safe_delivery(outbound),
    }


# ---------------------------------------------------------------------------
# Discord webhook
# ---------------------------------------------------------------------------

@app.post("/webhook/discord")
def discord_webhook(
    payload: dict,
    authorization: str | None = Header(default=None),
) -> dict:
    # Discord sends a PING (type 1) when registering the webhook → must PONG.
    if payload.get("type") == 1:
        return {"type": 1}

    if settings.discord_bearer_token:
        if authorization != f"Bearer {settings.discord_bearer_token}":
            raise HTTPException(status_code=401, detail="invalid discord token")

    parsed = parse_discord(payload)
    if not parsed:
        return {"status": "ignored"}

    user_id, text = parsed
    text = _validate_message_or_400(text)
    result = orchestrator.respond_with_route(text, user_id=f"dc:{user_id}")

    channel_id = str(payload.get("channel_id", ""))
    outbound = (
        senders.send_discord(channel_id=channel_id, text=result.response)
        if channel_id
        else {"sent": False, "reason": "channel_id missing"}
    )
    return {
        "status": "ok",
        "route": result.route,
        "reason": result.reason,
        "response": result.response,
        "delivery": _safe_delivery(outbound),
    }

