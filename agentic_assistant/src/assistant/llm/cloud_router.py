from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CloudConfig:
    groq_api_key: str
    groq_model: str
    gemini_api_key: str
    gemini_model: str
    kimi_api_key: str
    kimi_base_url: str
    kimi_model: str
    timeout_seconds: int = 25


class CloudRouter:
    def __init__(self, config: CloudConfig) -> None:
        self.config = config
        self._groq_client = None
        self._kimi_client = None
        self._gemini_ready = False

    def _get_groq_client(self):
        if self._groq_client is not None:
            return self._groq_client

        try:
            from groq import Groq
        except ImportError as exc:
            raise RuntimeError("groq package is not installed") from exc

        self._groq_client = Groq(api_key=self.config.groq_api_key, timeout=self.config.timeout_seconds)
        return self._groq_client

    def _get_kimi_client(self):
        if self._kimi_client is not None:
            return self._kimi_client

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package is not installed") from exc

        self._kimi_client = OpenAI(
            api_key=self.config.kimi_api_key,
            base_url=self.config.kimi_base_url,
            timeout=self.config.timeout_seconds,
        )
        return self._kimi_client

    def _configure_gemini(self):
        if self._gemini_ready:
            return

        try:
            import google.generativeai as genai
        except ImportError as exc:
            raise RuntimeError("google-generativeai package is not installed") from exc

        genai.configure(api_key=self.config.gemini_api_key)
        self._gemini_ready = True

    def groq_generate(self, prompt: str) -> str:
        if not self.config.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")

        client = self._get_groq_client()
        response = client.chat.completions.create(
            model=self.config.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        return (content or "").strip()

    def gemini_generate(self, prompt: str) -> str:
        if not self.config.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        self._configure_gemini()
        import google.generativeai as genai

        model = genai.GenerativeModel(self.config.gemini_model)
        response = model.generate_content(prompt)
        text = getattr(response, "text", None)
        return (text or "").strip()

    def kimi_generate(self, prompt: str) -> str:
        if not self.config.kimi_api_key:
            raise RuntimeError("KIMI_API_KEY is not configured")

        client = self._get_kimi_client()
        response = client.chat.completions.create(
            model=self.config.kimi_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        return (content or "").strip()
