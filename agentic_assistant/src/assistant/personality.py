"""Personality management for the agentic assistant.

The assistant's identity, tone, and response style are loaded once at startup
from either a YAML file (``PERSONALITY_FILE``) or from individual environment
variables.  The YAML file takes precedence over env vars when it exists.

Supported YAML keys (all optional — each falls back to the env var / default):

  name:           str   # assistant's display name
  personality:    str   # adjectives describing character (comma-separated)
  response_style: str   # how answers should sound
  humor:          str   # humor style
  expertise:      str   # knowledge domains (comma-separated)

Example personality.yaml
------------------------
name: Aria
personality: friendly, witty, and deeply knowledgeable
response_style: warm and concise, never verbose
humor: clever puns and light tech humour
expertise: software engineering, AI/ML, creative writing
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assistant.config import Settings

logger = logging.getLogger(__name__)


def _load_yaml(path: Path) -> dict:
    """Return a dict from *path* if it exists and is valid YAML, else empty dict."""
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore[import]
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to load personality file %s: %s", path, exc)
        return {}


class Personality:
    """Holds all personality fields and exposes a formatted system-prompt block."""

    def __init__(
        self,
        name: str,
        personality: str,
        response_style: str,
        humor: str,
        expertise: str,
    ) -> None:
        self.name = name
        self.personality = personality
        self.response_style = response_style
        self.humor = humor
        self.expertise = expertise

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_settings(cls, settings: "Settings") -> "Personality":
        """Build a Personality by merging the YAML file with Settings env vars."""
        yaml_data = _load_yaml(settings.personality_file)
        if yaml_data:
            logger.info("Loaded personality from %s", settings.personality_file)

        def _pick(yaml_key: str, setting_val: str) -> str:
            return str(yaml_data.get(yaml_key, setting_val)).strip() or setting_val

        return cls(
            name=_pick("name", settings.agent_name),
            personality=_pick("personality", settings.agent_personality),
            response_style=_pick("response_style", settings.agent_response_style),
            humor=_pick("humor", settings.agent_humor),
            expertise=_pick("expertise", settings.agent_expertise),
        )

    # ------------------------------------------------------------------
    # Prompt helpers
    # ------------------------------------------------------------------

    def system_prompt(self, is_local: bool = False) -> str:
        """Return a system instruction block that embeds this personality.

        Args:
            is_local: When True the prompt is shortened to save context tokens
                      on resource-constrained hardware (Raspberry Pi / llama.cpp).
        """
        if is_local:
            return (
                f"You are {self.name}. "
                f"Personality: {self.personality}. "
                f"Style: {self.response_style}. "
                "Use the provided context when relevant. Be concise."
            )
        return (
            f"You are {self.name}, an AI assistant.\n"
            f"Personality: {self.personality}.\n"
            f"Response style: {self.response_style}.\n"
            f"Humor: {self.humor}.\n"
            f"Areas of expertise: {self.expertise}.\n"
            "Use the provided context and conversation history when relevant."
        )
