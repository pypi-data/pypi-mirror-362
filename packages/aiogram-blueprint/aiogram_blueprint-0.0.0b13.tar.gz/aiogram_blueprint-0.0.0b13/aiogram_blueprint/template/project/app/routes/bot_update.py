from aiogram.types import Update
from starlette.requests import Request
from starlette.responses import Response

from ...context import Context


async def bot_update(request: Request, update: dict) -> Response:
    ctx: Context = request.app.state.ctx

    await ctx.dp.feed_update(
        bot=ctx.bot,
        update=Update(**update),
    )
    return Response()
