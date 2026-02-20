from __future__ import annotations

from typing import Any

import httpx


class OutboundSenders:
    def __init__(
        self,
        telegram_bot_token: str = "",
        discord_bot_token: str = "",
        timeout_seconds: float = 10.0,
    ) -> None:
        self.telegram_bot_token = telegram_bot_token
        self.discord_bot_token = discord_bot_token
        self.timeout_seconds = timeout_seconds

    @staticmethod
    def _truncate_text(text: str, max_chars: int) -> str:
        clean = text.strip()
        if len(clean) <= max_chars:
            return clean
        return clean[: max_chars - 1] + "…"

    @staticmethod
    def _safe_error(reason: str, status_code: int | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"sent": False, "reason": reason}
        if status_code is not None:
            payload["status_code"] = status_code
        return payload

    def send_telegram(self, chat_id: str, text: str) -> dict[str, Any]:
        if not self.telegram_bot_token:
            return {"sent": False, "reason": "TELEGRAM_BOT_TOKEN not set"}

        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": self._truncate_text(text, 3900)}

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(url, json=payload)
        except httpx.RequestError:
            return self._safe_error("telegram transport error")

        if response.status_code >= 400:
            return self._safe_error("telegram api error", status_code=response.status_code)

        return {"sent": True}

    def send_discord(self, channel_id: str, text: str) -> dict[str, Any]:
        if not self.discord_bot_token:
            return {"sent": False, "reason": "DISCORD_BOT_TOKEN not set"}

        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {self.discord_bot_token}",
            "Content-Type": "application/json",
        }
        payload = {"content": self._truncate_text(text, 1900)}

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(url, headers=headers, json=payload)
        except httpx.RequestError:
            return self._safe_error("discord transport error")

        if response.status_code >= 400:
            return self._safe_error("discord api error", status_code=response.status_code)

        return {"sent": True}
