"""Polling-mode bots for Telegram and Discord.

These bots run as async background tasks when ``BOT_MODE=polling`` is set.
They are ideal for Windows environments and any machine that does not have a
publicly reachable HTTPS URL for webhooks.

Modules
-------
telegram_polling  – Telegram Bot API long-polling (no extra deps; uses httpx)
discord_bot       – Discord gateway bot (requires discord.py >= 2.3)
"""
