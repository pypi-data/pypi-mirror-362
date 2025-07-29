from aiogram import Dispatcher, Bot
from sulguk import AiogramSulgukMiddleware

from .db import DbSessionMiddleware
from .i18n import I18nJinjaMiddleware
from .throttling import ThrottlingMiddleware


def register(dp: Dispatcher, bot: Bot) -> None:
    bot.session.middleware(AiogramSulgukMiddleware())

    dp.update.middleware(ThrottlingMiddleware())
    dp.update.middleware(DbSessionMiddleware())
    dp.update.middleware(I18nJinjaMiddleware())

    dp.error.middleware(ThrottlingMiddleware())
    dp.error.middleware(DbSessionMiddleware())
    dp.error.middleware(I18nJinjaMiddleware())


__all__ = ["register"]
