from __future__ import annotations

import logging

import uvicorn

from assistant.api import app
from assistant.config import settings

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Use uvicorn's default logging so output is clean (works on Windows too).
    # log_config=None means uvicorn uses its own sensible defaults (not the
    # root logger config) which avoids duplicate / garbled log lines.
    # uvicorn auto-selects asyncio on Windows and uvloop on Linux/macOS
    # when uvloop is installed (included via uvicorn[standard]).
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info",
        access_log=True,
    )
