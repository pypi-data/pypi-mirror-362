import typing as t
from dataclasses import dataclass

Config = t.Dict[str, bool]
Condition = t.Callable[[Config], bool]


@dataclass(frozen=True)
class SurveyOption:
    message: str
    choices: list[str]
    is_multi: bool = False


SURVEY_FIELDS: t.Dict[str, SurveyOption] = {
    "run_type": SurveyOption("Choose how the bot should be launched:", ["Webhook", "Polling"]),
    "services": SurveyOption(
        "Select the services to include in your project:",
        ["Redis", "Database", "Scheduler"],
        is_multi=True
    ),
    "db_type": SurveyOption("Choose the type of database to use:", ["PostgreSQL", "MySQL", "SQLite"]),
    "storage_type": SurveyOption("Select storage type for the bot:", ["Redis", "Memory"]),
    "add_admin": SurveyOption("Would you like to include a Web Admin Panel?", ["Yes", "No"]),
}

COMPONENT_FOLDERS: t.Dict[str, Condition] = {
    "bot": lambda _: True,
    "app": lambda cfg: cfg.get("use_webhook", False),
    "admin": lambda cfg: cfg.get("use_admin", False),
    "services": lambda cfg: cfg.get("use_db", False) or cfg.get("use_redis", False) or cfg.get("use_scheduler", False),
    "db": lambda cfg: cfg.get("use_db", False),
    "redis": lambda cfg: cfg.get("use_redis", False),
    "scheduler": lambda cfg: cfg.get("use_scheduler", False),
    "alembic": lambda cfg: cfg.get("use_db", False),
    "data": lambda cfg: cfg.get("use_db", False) or cfg.get("use_scheduler", False),
}
