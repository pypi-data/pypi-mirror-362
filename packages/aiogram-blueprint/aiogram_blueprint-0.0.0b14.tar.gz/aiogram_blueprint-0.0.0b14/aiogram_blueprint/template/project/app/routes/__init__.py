from fastapi import FastAPI

from .bot_update import bot_update
from ...config import WEBHOOK_PATH


def add(app: FastAPI) -> None:
    app.add_api_route(
        path=f"/{WEBHOOK_PATH}",
        endpoint=bot_update,
        methods=["POST"],
    )


__all__ = ["add"]
