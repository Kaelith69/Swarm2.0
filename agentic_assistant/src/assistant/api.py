from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from assistant.config import settings
from assistant.llm.cloud_router import CloudConfig, CloudRouter
from assistant.llm.llama_cpp_runner import LlamaCppRunner
from assistant.messaging.parsers import parse_discord, parse_telegram, parse_whatsapp
from assistant.messaging.senders import OutboundSenders
from assistant.orchestrator import AgentOrchestrator
from assistant.rag.store import RagStore


rag_store = RagStore(settings.rag_data_dir, settings.embedding_model)
llm_runner = LlamaCppRunner(
    executable_path=settings.llama_main_path,
    model_path=settings.model_path,
    threads=settings.inference_threads,
    context_tokens=settings.llm_context_tokens,
    max_tokens=settings.max_response_tokens,
    temperature=settings.llm_temperature,
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
orchestrator = AgentOrchestrator(
    rag_store,
    llm_runner,
    cloud_router,
    top_k=settings.rag_top_k,
    long_context_threshold_chars=settings.long_context_threshold_chars,
)
senders = OutboundSenders(
    telegram_bot_token=settings.telegram_bot_token,
    discord_bot_token=settings.discord_bot_token,
    whatsapp_access_token=settings.whatsapp_access_token,
    whatsapp_phone_number_id=settings.whatsapp_phone_number_id,
)

app = FastAPI(title="Pi Agentic Assistant", version="1.0.0")


class QueryRequest(BaseModel):
    message: str


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "model_path": str(settings.model_path),
        "llama_main_path": str(settings.llama_main_path),
        "hybrid": {
            "groq_enabled": bool(settings.groq_api_key),
            "gemini_enabled": bool(settings.gemini_api_key),
            "kimi_enabled": bool(settings.kimi_api_key),
        },
    }


@app.post("/query")
def query(req: QueryRequest) -> dict:
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required")
    result = orchestrator.respond_with_route(req.message.strip())
    return {"route": result.route, "response": result.response}


@app.post("/webhook/telegram")
def telegram_webhook(payload: dict, x_telegram_bot_api_secret_token: str | None = Header(default=None)) -> dict:
    if settings.telegram_secret and x_telegram_bot_api_secret_token != settings.telegram_secret:
        raise HTTPException(status_code=401, detail="invalid telegram secret")

    parsed = parse_telegram(payload)
    if not parsed:
        return {"status": "ignored"}

    _, text = parsed
    result = orchestrator.respond_with_route(text)
    generated = result.response
    chat_id = str(((payload.get("message") or payload.get("edited_message") or {}).get("chat") or {}).get("id", ""))
    outbound = senders.send_telegram(chat_id=chat_id, text=generated) if chat_id else {"sent": False, "reason": "chat id missing"}
    return {"status": "ok", "route": result.route, "response": generated, "delivery": outbound}


@app.post("/webhook/discord")
def discord_webhook(payload: dict, authorization: str | None = Header(default=None)) -> dict:
    if settings.discord_bearer_token:
        expected = f"Bearer {settings.discord_bearer_token}"
        if authorization != expected:
            raise HTTPException(status_code=401, detail="invalid discord token")

    parsed = parse_discord(payload)
    if not parsed:
        return {"status": "ignored"}

    _, text = parsed
    result = orchestrator.respond_with_route(text)
    generated = result.response
    channel_id = str(payload.get("channel_id", ""))
    outbound = senders.send_discord(channel_id=channel_id, text=generated) if channel_id else {"sent": False, "reason": "channel id missing"}
    return {"status": "ok", "route": result.route, "response": generated, "delivery": outbound}


@app.get("/webhook/whatsapp")
def whatsapp_verify(mode: str = "", token: str = "", challenge: str = "") -> str:
    if mode == "subscribe" and token == settings.whatsapp_verify_token:
        return challenge
    raise HTTPException(status_code=403, detail="verification failed")


@app.post("/webhook/whatsapp")
def whatsapp_webhook(payload: dict) -> dict:
    parsed = parse_whatsapp(payload)
    if not parsed:
        return {"status": "ignored"}

    user_phone, text = parsed
    result = orchestrator.respond_with_route(text)
    generated = result.response
    number_id = str(
        (
            (
                (payload.get("entry") or [{}])[0].get("changes") or [{}]
            )[0].get("value")
            or {}
        ).get("metadata", {})
        .get("phone_number_id", "")
    )
    outbound = senders.send_whatsapp(to_phone=user_phone, text=generated, phone_number_id=number_id or None)
    return {"status": "ok", "route": result.route, "response": generated, "delivery": outbound}
