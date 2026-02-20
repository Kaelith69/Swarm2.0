"""Telegram long-polling bot.

Polls the Telegram Bot API ``getUpdates`` endpoint in a background asyncio
task.  No public URL or webhook registration is required — ideal for Windows
development and production machines behind NAT/firewalls.

Usage
-----
Set ``BOT_MODE=polling`` in ``.env``.  This module is started automatically
by ``api.py`` during FastAPI startup when a ``TELEGRAM_BOT_TOKEN`` is
present.

Security note
-------------
Long-polling is a perfectly valid and officially supported Telegram Bot API
mode.  The ``timeout`` parameter (default 30s) keeps connections efficient;
the server holds each request open until a new update arrives or the timeout
elapses.
"""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

import httpx

if TYPE_CHECKING:
    from assistant.orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)

_BASE = "https://api.telegram.org/bot{token}/{method}"
_POLL_TIMEOUT = 30   # seconds — server-side long-poll window
_RETRY_DELAY = 5     # seconds to wait before retrying on error
_MAX_CHARS = 3900    # Telegram message limit with some headroom


class TelegramPoller:
    """Async Telegram long-polling loop that feeds messages to the orchestrator."""

    def __init__(
        self,
        token: str,
        orchestrator: "AgentOrchestrator",
        poll_timeout: int = _POLL_TIMEOUT,
    ) -> None:
        self.token = token
        self.orchestrator = orchestrator
        self.poll_timeout = poll_timeout
        self._offset: int = 0

    def _url(self, method: str) -> str:
        return _BASE.format(token=self.token, method=method)

    async def run(self) -> None:
        """Run the polling loop forever (until cancelled)."""
        logger.info("Telegram polling bot started (long-poll timeout=%ds)", self.poll_timeout)
        async with httpx.AsyncClient(timeout=self.poll_timeout + 10) as client:
            while True:
                try:
                    await self._poll_once(client)
                except asyncio.CancelledError:
                    logger.info("Telegram polling bot stopping")
                    return
                except Exception as exc:  # noqa: BLE001
                    logger.warning("Telegram polling error: %s — retrying in %ds", exc, _RETRY_DELAY)
                    await asyncio.sleep(_RETRY_DELAY)

    async def _poll_once(self, client: httpx.AsyncClient) -> None:
        params: dict[str, Any] = {
            "timeout": self.poll_timeout,
            "offset": self._offset,
            "allowed_updates": ["message"],
        }
        resp = await client.get(self._url("getUpdates"), params=params)
        resp.raise_for_status()
        data = resp.json()

        updates: list[dict] = data.get("result", [])
        for update in updates:
            self._offset = update["update_id"] + 1
            await self._handle_update(client, update)

    async def _handle_update(self, client: httpx.AsyncClient, update: dict) -> None:
        message = update.get("message") or update.get("edited_message")
        if not message:
            return

        text = (message.get("text") or "").strip()
        if not text:
            return

        chat_id = str((message.get("chat") or {}).get("id", ""))
        user_id = str((message.get("from") or {}).get("id", "unknown"))

        if not chat_id:
            return

        logger.debug("Telegram message from %s: %r", user_id, text[:80])

        try:
            # Run orchestrator in a thread so we don't block the event loop
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                self.orchestrator.respond_with_route,
                text,
                f"tg:{user_id}",
            )
            reply = result.response
        except Exception as exc:  # noqa: BLE001
            logger.error("Orchestrator error for Telegram message: %s", exc)
            reply = "Sorry, I encountered an error processing your message."

        await self._send_message(client, chat_id, reply)

    async def _send_message(self, client: httpx.AsyncClient, chat_id: str, text: str) -> None:
        truncated = text[:_MAX_CHARS] if len(text) > _MAX_CHARS else text
        payload = {"chat_id": chat_id, "text": truncated}
        try:
            resp = await client.post(self._url("sendMessage"), json=payload)
            if resp.status_code >= 400:
                logger.warning("Telegram sendMessage failed: HTTP %d", resp.status_code)
        except httpx.RequestError as exc:
            logger.warning("Telegram send error: %s", exc)
