from contextlib import asynccontextmanager

import uvicorn
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI
from sulguk import SULGUK_PARSE_MODE

from .app import routes
from .bot import middlewares, handlers, commands
from .config import APP_HOST, APP_PORT, BOT_TOKEN, WEBHOOK_URL
from .context import Context
from .services.db import DBService
from .services.redis import RedisService
from .services.scheduler import SchedulerService


async def on_startup(ctx: Context) -> None:
    for service in ctx.services:
        await service.start()

    middlewares.register(ctx.dp, ctx.bot)
    handlers.register(ctx.dp)
    routes.add(ctx.app)

    await commands.setup(ctx.bot)
    await ctx.bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(ctx: Context) -> None:
    await commands.delete(ctx.bot)
    await ctx.bot.delete_webhook()
    await ctx.bot.session.close()

    for service in reversed(ctx.services):
        await service.shutdown()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    ctx = Context(
        RedisService(),
        DBService(),
        SchedulerService()
    )

    properties = DefaultBotProperties(parse_mode=SULGUK_PARSE_MODE)
    storage = RedisStorage(redis=ctx.redis, key_builder=DefaultKeyBuilder())

    ctx.bot = Bot(BOT_TOKEN, default=properties)
    ctx.dp = Dispatcher(storage=storage, ctx=ctx)

    ctx.app = _app
    _app.state.ctx = ctx  # type: ignore[attr-defined]

    await on_startup(ctx)
    try:
        yield
    finally:
        await on_shutdown(ctx)


if __name__ == "__main__":
    app = FastAPI(lifespan=lifespan)
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
