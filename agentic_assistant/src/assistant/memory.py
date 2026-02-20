"""Per-user conversation memory backed by SQLite.

Stores the last N turns (user + assistant) per user_id so the
orchestrator can include recent context in every prompt.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path


class ConversationMemory:
    def __init__(self, data_dir: Path, max_turns: int = 10) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "memory.sqlite3"
        self.max_turns = max_turns
        self._ensure_schema()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        # Fresh connection per operation — thread-safe by default.
        # Do NOT use check_same_thread=False: SQLite connections cannot be
        # safely shared across threads without external locking.
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS history (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id   TEXT    NOT NULL,
                    role      TEXT    NOT NULL,
                    content   TEXT    NOT NULL,
                    ts        TEXT    DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_hist_user ON history (user_id, id)")
            conn.commit()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_turn(self, user_id: str, role: str, content: str) -> None:
        """Append a message turn for *user_id*.  role is 'user' or 'assistant'."""
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO history (user_id, role, content) VALUES (?, ?, ?)",
                (user_id, role, content),
            )
            conn.commit()
        self._trim(user_id)

    def get_history(self, user_id: str) -> list[dict]:
        """Return the last *max_turns* turns (oldest first)."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT role, content FROM history
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, self.max_turns * 2),
            ).fetchall()
        return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

    def format_for_prompt(self, user_id: str) -> str:
        """Return a compact conversation history block for inclusion in prompts."""
        history = self.get_history(user_id)
        if not history:
            return ""
        lines = [
            f"{'User' if turn['role'] == 'user' else 'Assistant'}: {turn['content']}"
            for turn in history
        ]
        return "--- Previous conversation ---\n" + "\n".join(lines) + "\n--- End ---"

    def clear(self, user_id: str) -> None:
        """Remove all stored history for *user_id*."""
        with self._connect() as conn:
            conn.execute("DELETE FROM history WHERE user_id = ?", (user_id,))
            conn.commit()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _trim(self, user_id: str) -> None:
        """Keep only the most recent max_turns*2 rows for this user."""
        keep = self.max_turns * 2
        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM history WHERE user_id = ? AND id NOT IN (
                    SELECT id FROM history WHERE user_id = ? ORDER BY id DESC LIMIT ?
                )
                """,
                (user_id, user_id, keep),
            )
            conn.commit()
