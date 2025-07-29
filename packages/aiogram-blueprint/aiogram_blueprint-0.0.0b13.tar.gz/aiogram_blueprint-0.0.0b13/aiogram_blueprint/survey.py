import typing as t

from InquirerPy import inquirer

from .constants import SURVEY_FIELDS


def ask(field: str) -> t.Any:
    option = SURVEY_FIELDS[field]
    if option.is_multi:
        return inquirer.checkbox(
            message=option.message,
            choices=option.choices,
            transformer=lambda result: ", ".join(result)
        ).execute()
    return inquirer.select(
        message=option.message,
        choices=option.choices,
    ).execute()


def run_survey() -> t.Dict[str, t.Any]:
    config: t.Dict[str, t.Any] = {"use_webhook": ask("run_type") == "Webhook"}

    services = ask("services") or []
    config.update({
        "use_redis": "Redis" in services,
        "use_db": "Database" in services,
        "use_scheduler": "Scheduler" in services,
        "use_admin": False,
    })

    config["db_type"] = ask("db_type") if config["use_db"] else None
    config["storage_type"] = ask("storage_type").lower() if config["use_redis"] else None

    if config["use_webhook"] and config["use_db"]:
        config["use_admin"] = ask("add_admin") == "Yes"

    return config
