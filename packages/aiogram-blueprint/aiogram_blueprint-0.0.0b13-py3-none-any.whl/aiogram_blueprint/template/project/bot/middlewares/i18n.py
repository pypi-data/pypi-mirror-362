from __future__ import annotations

import typing as t
from collections.abc import Awaitable, Callable
from pathlib import Path

import yaml
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, User
from jinja2 import Environment

from ..utils import Localizer
from ...config import (
    LOCALES_DIR,
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
)


class I18nJinjaMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        self.locales_data = self.load_locales()
        self.jinja_env = Environment(
            autoescape=True,
            lstrip_blocks=True,
            trim_blocks=True,
            enable_async=True,
        )

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, t.Dict[str, t.Any]],
                Awaitable[t.Any]
            ],
            event: TelegramObject,
            data: t.Dict[str, t.Any],
    ) -> t.Any:
        user: t.Optional[User] = data.get("event_from_user")

        if user is not None and not user.is_bot:
            user_locale = (
                user.language_code
                if user.language_code in SUPPORTED_LOCALES
                else DEFAULT_LOCALE
            )
            translations = self.locales_data.get(user_locale)
            if translations is None:
                raise ValueError(
                    f"Translations for locale '{user_locale}' not found in i18n component."
                )

            data["localizer"] = Localizer(
                jinja_env=self.jinja_env,
                translations=translations,
            )

        return await handler(event, data)

    @staticmethod
    def load_yaml(file_path: Path) -> t.Dict[str, str]:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing locale file: '{file_path}'")
        with file_path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def load_locales(self) -> t.Dict[str, t.Dict[str, str]]:
        if not LOCALES_DIR.is_dir():
            raise FileNotFoundError(
                f"Locales path '{LOCALES_DIR}' not found or is not a directory"
            )

        locales_data = {}
        for locale in SUPPORTED_LOCALES:
            file_path = LOCALES_DIR / f"{locale}.yaml"
            locales_data[locale] = self.load_yaml(file_path)
        return locales_data
