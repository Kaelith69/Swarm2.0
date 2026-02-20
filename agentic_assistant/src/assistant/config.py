from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = _env_int("PORT", 8000)

    model_path: Path = Path(os.getenv("MODEL_PATH", str(Path.home() / "models" / "gemma-2-2b-it-Q4_K_M.gguf")))
    llama_main_path: Path = Path(
        os.getenv("LLAMA_MAIN_PATH", str(Path.home() / "llama.cpp" / "build" / "bin" / "llama-cli"))
    )
    inference_threads: int = _env_int("INFERENCE_THREADS", max(1, os.cpu_count() or 4))
    llm_context_tokens: int = _env_int("LLM_CONTEXT_TOKENS", 2048)
    max_response_tokens: int = _env_int("MAX_RESPONSE_TOKENS", 256)
    llm_temperature: float = _env_float("LLM_TEMPERATURE", 0.2)

    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    rag_top_k: int = _env_int("RAG_TOP_K", 3)
    rag_data_dir: Path = Path(os.getenv("RAG_DATA_DIR", "./data/rag"))
    max_input_chars: int = _env_int("MAX_INPUT_CHARS", 8000)
    expose_delivery_errors: bool = os.getenv("EXPOSE_DELIVERY_ERRORS", "false").lower() == "true"

    long_context_threshold_chars: int = _env_int("LONG_CONTEXT_THRESHOLD_CHARS", 1200)
    cloud_timeout_seconds: int = _env_int("CLOUD_TIMEOUT_SECONDS", 25)

    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    kimi_api_key: str = os.getenv("KIMI_API_KEY", "")
    kimi_base_url: str = os.getenv("KIMI_BASE_URL", "https://api.moonshot.ai/v1")
    kimi_model: str = os.getenv("KIMI_MODEL", "moonshot-v1-8k")

    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_secret: str = os.getenv("TELEGRAM_SECRET", "")
    discord_bot_token: str = os.getenv("DISCORD_BOT_TOKEN", "")
    discord_bearer_token: str = os.getenv("DISCORD_BEARER_TOKEN", "")
    whatsapp_access_token: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    whatsapp_phone_number_id: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    whatsapp_verify_token: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "")


settings = Settings()
