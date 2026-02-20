from __future__ import annotations

import logging

import uvicorn

from assistant.api import app
from assistant.config import settings

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Use uvicorn's default logging so journal output is clean under systemd.
    # log_config=None means uvicorn uses its own sensible defaults (not the
    # root logger config) which avoids duplicate / garbled log lines.
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info",
        access_log=True,
    )
