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
    # 1. Linked Roles / Message Components (if any) might have 'content'
    if "content" in payload:
        text = str(payload.get("content", "")).strip()
        user = str((payload.get("author") or {}).get("id", "unknown"))
        return (user, text) if text else None

    # 2. Application Command (Slash Command)
    # Payload structure: { "type": 2, "data": { "options": [ { "value": "..." } ] }, "member": { "user": { "id": "..." } } }
    if payload.get("type") == 2:
        data = payload.get("data", {})
        options = data.get("options", [])
        if not options:
            return None
        
        # Assume the first option contains the message content
        # (Works for /chat message: "hello" or /ask query: "hello")
        text = str(options[0].get("value", "")).strip()
        
        # Extract user from 'member' (server) or 'user' (DM)
        member = payload.get("member", {})
        user_obj = member.get("user") or payload.get("user") or {}
        user = str(user_obj.get("id", "unknown"))
        
        return (user, text) if text else None

    return None
