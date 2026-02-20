from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

_IS_WINDOWS = platform.system() == "Windows"

# Platform-aware default paths for llama.cpp and model files
_DEFAULT_MODEL_PATH = (
    r"C:\llama.cpp\models\gemma-2-2b-it-Q4_K_M.gguf"
    if _IS_WINDOWS
    else "/home/pi/models/gemma-2-2b-it-Q4_K_M.gguf"
)
_DEFAULT_LLAMA_PATH = (
    r"C:\llama.cpp\build\bin\llama-cli.exe"
    if _IS_WINDOWS
    else "/home/pi/llama.cpp/build/bin/llama-cli"
)


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


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = _env_int("PORT", 8000)

    model_path: Path = Path(os.getenv("MODEL_PATH", _DEFAULT_MODEL_PATH))
    llama_main_path: Path = Path(os.getenv("LLAMA_MAIN_PATH", _DEFAULT_LLAMA_PATH))

    # Thread count: conservative default; tune up once temperatures are stable.
    inference_threads: int = _env_int(
        "INFERENCE_THREADS",
        max(1, (os.cpu_count() or 4) if (os.cpu_count() or 4) <= 4 else (os.cpu_count() or 4) - 1),
    )
    llm_context_tokens: int = _env_int("LLM_CONTEXT_TOKENS", 2048)
    max_response_tokens: int = _env_int("MAX_RESPONSE_TOKENS", 256)
    llm_temperature: float = _env_float("LLM_TEMPERATURE", 0.2)

    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    rag_top_k: int = _env_int("RAG_TOP_K", 3)
    rag_data_dir: Path = Path(os.getenv("RAG_DATA_DIR", "./data/rag"))
    max_input_chars: int = _env_int("MAX_INPUT_CHARS", 8000)
    expose_delivery_errors: bool = _env_bool("EXPOSE_DELIVERY_ERRORS", False)

    long_context_threshold_chars: int = _env_int("LONG_CONTEXT_THRESHOLD_CHARS", 1200)
    cloud_timeout_seconds: int = _env_int("CLOUD_TIMEOUT_SECONDS", 25)

    # Conversation memory
    memory_max_turns: int = _env_int("MEMORY_MAX_TURNS", 10)

    # Local LLM routing classification
    use_llm_routing: bool = _env_bool("USE_LLM_ROUTING", True)
    local_short_threshold_chars: int = _env_int("LOCAL_SHORT_THRESHOLD_CHARS", 150)
    # Timeout in seconds for the llama.cpp subprocess
    llama_timeout_seconds: int = _env_int("LLAMA_TIMEOUT_SECONDS", 120)

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
    discord_public_key: str = os.getenv("DISCORD_PUBLIC_KEY", "")

    # Bot mode: "webhook" (requires public HTTPS URL) or "polling" (Windows-friendly)
    # In polling mode, Telegram and Discord bots actively pull messages — no public URL needed.
    bot_mode: str = os.getenv("BOT_MODE", "webhook")

    # ---------------------------------------------------------------------------
    # Personality configuration
    # ---------------------------------------------------------------------------
    # These fields shape the assistant's identity, tone, and response style.
    # They are injected into the system prompt for every route (local + cloud).
    agent_name: str = os.getenv("AGENT_NAME", "Assistant")
    agent_personality: str = os.getenv(
        "AGENT_PERSONALITY", "helpful, knowledgeable, and professional"
    )
    agent_response_style: str = os.getenv(
        "AGENT_RESPONSE_STYLE", "concise, clear, and accurate"
    )
    agent_humor: str = os.getenv("AGENT_HUMOR", "subtle and professional")
    agent_expertise: str = os.getenv(
        "AGENT_EXPERTISE", "general knowledge, technology, and problem-solving"
    )
    # Path to an optional YAML personality file (overrides the env vars above when present)
    personality_file: Path = Path(os.getenv("PERSONALITY_FILE", "./personality.yaml"))


settings = Settings()
