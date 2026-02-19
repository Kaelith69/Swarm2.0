from __future__ import annotations

import uvicorn

from assistant.api import app
from assistant.config import settings


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
