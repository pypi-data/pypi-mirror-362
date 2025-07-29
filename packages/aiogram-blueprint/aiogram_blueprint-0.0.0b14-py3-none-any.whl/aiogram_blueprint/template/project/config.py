from __future__ import annotations

import typing as t
from pathlib import Path
from zoneinfo import ZoneInfo

from environs import Env

ENV = Env()
ENV.read_env()

BASE_DIR = Path(__file__).resolve().parent
TIMEZONE = ZoneInfo(ENV.str("TIMEZONE", "UTC"))

LOCALES_DIR: Path = BASE_DIR.parent / "locales"
DEFAULT_LOCALE: str = ENV.str("DEFAULT_LOCALE", "en")
SUPPORTED_LOCALES: t.List[str] = ENV.list("SUPPORTED_LOCALES", default=[DEFAULT_LOCALE])

DEV_ID: int = ENV.int("DEV_ID")
ADMIN_IDS: list = ENV.list("ADMIN_IDS", subcast=int, default=[])

DB_URL = ENV.str("DB_URL")
REDIS_URL = ENV.str("REDIS_URL")
SCHEDULER_URL = ENV.str("SCHEDULER_URL")

APP_URL: str = ENV.str("APP_URL")
APP_PORT: int = ENV.int("APP_PORT")
APP_HOST: str = ENV.str("APP_HOST")

BOT_TOKEN: str = ENV.str("BOT_TOKEN")
BOT_USERNAME: str = ENV.str("BOT_USERNAME")

WEBHOOK_PATH: str = f"{BOT_USERNAME}/{BOT_TOKEN}"
WEBHOOK_URL: str = f"{APP_URL.rstrip('/')}/{WEBHOOK_PATH}"

THROTTLING_DEFAULT_KEY: str = "default"
THROTTLING_DEFAULT_TTL: float = 0.7
