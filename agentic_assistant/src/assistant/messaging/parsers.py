from __future__ import annotations

from typing import Any


def parse_telegram(payload: dict[str, Any]) -> tuple[str, str] | None:
    message = payload.get("message") or payload.get("edited_message")
    if not message:
        return None
    text = (message.get("text") or "").strip()
    user = str((message.get("from") or {}).get("id", "unknown"))
    if not text:
        return None
    return user, text


def parse_discord(payload: dict[str, Any]) -> tuple[str, str] | None:
    text = str(payload.get("content", "")).strip()
    user = str((payload.get("author") or {}).get("id", "unknown"))
    if not text:
        return None
    return user, text
