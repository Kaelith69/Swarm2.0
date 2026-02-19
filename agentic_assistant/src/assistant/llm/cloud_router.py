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

    def groq_generate(self, prompt: str) -> str:
        if not self.config.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")

        try:
            from groq import Groq
        except ImportError as exc:
            raise RuntimeError("groq package is not installed") from exc

        client = Groq(api_key=self.config.groq_api_key)
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

        try:
            import google.generativeai as genai
        except ImportError as exc:
            raise RuntimeError("google-generativeai package is not installed") from exc

        genai.configure(api_key=self.config.gemini_api_key)
        model = genai.GenerativeModel(self.config.gemini_model)
        response = model.generate_content(prompt)
        text = getattr(response, "text", None)
        return (text or "").strip()

    def kimi_generate(self, prompt: str) -> str:
        if not self.config.kimi_api_key:
            raise RuntimeError("KIMI_API_KEY is not configured")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package is not installed") from exc

        client = OpenAI(api_key=self.config.kimi_api_key, base_url=self.config.kimi_base_url)
        response = client.chat.completions.create(
            model=self.config.kimi_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        return (content or "").strip()
