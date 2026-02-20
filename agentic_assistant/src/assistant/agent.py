from __future__ import annotations

import logging
import platform

import uvicorn

from assistant.api import app
from assistant.config import settings

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Use uvicorn's default logging so output is clean (works on Windows too).
    # log_config=None means uvicorn uses its own sensible defaults (not the
    # root logger config) which avoids duplicate / garbled log lines.
    # On Windows, use "asyncio" loop policy (default); on Linux, "uvloop" is
    # auto-selected by uvicorn[standard] when available.
    loop_policy = "auto"

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info",
        access_log=True,
        loop=loop_policy,
    )
