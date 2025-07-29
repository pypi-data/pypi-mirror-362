from __future__ import annotations

import typing as t

from aiogram import Bot, Dispatcher

from .services.abstract import AbstractService


class Context:
    services: t.List[AbstractService]
    dp: Dispatcher
    bot: Bot

    def __init__(self, *services: AbstractService) -> None:
        self.services: list[AbstractService] = list(services)

        for service in self.services:
            for attr in getattr(service, "__slots__", []):
                if hasattr(service, attr):
                    value = getattr(service, attr)
                    setattr(self, attr, value)

    def __getattr__(self, item: str) -> t.Any:
        for service in self.services:
            if hasattr(service, item):
                return getattr(service, item)
        raise AttributeError(f"'Context' has no attribute '{item}'")

    def __setattr__(self, key: str, value: t.Any) -> None:
        super().__setattr__(key, value)

    def __dir__(self) -> list[str]:
        attrs = set(super().__dir__()) | set(vars(self).keys())
        for service in self.services:
            attrs.update(getattr(service, "__slots__", []))
        return sorted(attrs)
