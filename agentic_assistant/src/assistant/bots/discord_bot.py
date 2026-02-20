"""Discord gateway bot (polling mode).

Connects to Discord's WebSocket gateway via ``discord.py`` and listens for
messages in channels the bot has been invited to.  Responses are routed
through the same ``AgentOrchestrator`` used by the webhook endpoints.

Prerequisites
-------------
1. Add the bot to a server with ``Send Messages`` + ``Read Message History``
   permissions.
2. Enable the ``MESSAGE CONTENT INTENT`` in the Discord Developer Portal
   (Bot → Privileged Gateway Intents).
3. Set ``BOT_MODE=polling`` in ``.env``.

This module is started automatically by ``api.py`` during FastAPI startup
when both ``DISCORD_BOT_TOKEN`` and ``BOT_MODE=polling`` are configured.

Dependency
----------
``discord.py >= 2.3`` — install via ``pip install discord.py>=2.3``.
The package is listed in ``requirements.txt`` alongside the other deps.

Security note
-------------
The bot only responds to messages from non-bot users.  It ignores its own
messages to prevent feedback loops.  The ``bot_user_id`` is captured once
the ``on_ready`` event fires and used to filter outgoing echoes.
"""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assistant.orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)

_MAX_CHARS = 1900   # Discord message limit with some headroom


class DiscordBot:
    """Wraps a ``discord.Client`` to route messages through the orchestrator."""

    def __init__(self, token: str, orchestrator: "AgentOrchestrator") -> None:
        self.token = token
        self.orchestrator = orchestrator

    async def run(self) -> None:
        """Start the Discord gateway connection (runs until cancelled)."""
        try:
            import discord  # type: ignore[import]
        except ImportError as exc:
            raise RuntimeError(
                "discord.py is not installed. "
                "Run: pip install 'discord.py>=2.3'"
            ) from exc

        intents = discord.Intents.default()
        intents.message_content = True   # requires the privileged intent to be enabled
        client = discord.Client(intents=intents)
        orchestrator = self.orchestrator

        @client.event
        async def on_ready() -> None:
            logger.info("Discord bot logged in as %s (id=%s)", client.user, client.user.id)

        @client.event
        async def on_message(message: discord.Message) -> None:
            # Ignore messages sent by the bot itself
            if client.user and message.author.id == client.user.id:
                return
            # Ignore messages from other bots
            if message.author.bot:
                return

            text = (message.content or "").strip()
            if not text:
                return

            user_id = str(message.author.id)
            channel_id = str(message.channel.id)
            logger.debug("Discord message from %s in channel %s: %r", user_id, channel_id, text[:80])

            async with message.channel.typing():
                try:
                    result = await asyncio.get_event_loop().run_in_executor(
                        None,
                        orchestrator.respond_with_route,
                        text,
                        f"dc:{user_id}",
                    )
                    reply = result.response
                except Exception as exc:  # noqa: BLE001
                    logger.error("Orchestrator error for Discord message: %s", exc)
                    reply = "Sorry, I encountered an error processing your message."

            truncated = reply[:_MAX_CHARS] if len(reply) > _MAX_CHARS else reply
            try:
                await message.reply(truncated)
            except discord.HTTPException as exc:
                logger.warning("Discord reply failed: %s", exc)

        try:
            await client.start(self.token)
        except asyncio.CancelledError:
            logger.info("Discord bot stopping")
            await client.close()
            raise
        except Exception as exc:  # noqa: BLE001
            logger.error("Discord bot error: %s", exc)
            await client.close()
            raise
