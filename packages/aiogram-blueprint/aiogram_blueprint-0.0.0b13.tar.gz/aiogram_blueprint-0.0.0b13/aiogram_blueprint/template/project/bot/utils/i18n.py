import typing as t
from typing import Any, Optional

from jinja2 import Environment
from sulguk import RenderResult


class Localizer:

    def __init__(
            self,
            jinja_env: Environment,
            translations: t.Dict[str, t.Any],
    ) -> None:
        self.jinja_env = jinja_env
        self.translations = translations

    async def __call__(
            self,
            key: Optional[str] = None,
            *,
            default: Optional[str] = None,
            **kwargs: t.Any
    ) -> t.Union[str, RenderResult]:
        if key is not None:
            template_str = self._get_translation(key)
            if template_str is None:
                raise KeyError(f"Translation key '{key}' not found.")
        elif default is not None:
            template_str = default
        else:
            raise ValueError("Either 'key' or 'default' must be provided.")

        try:
            template = self.jinja_env.from_string(template_str)
            text = await template.render_async(**kwargs)
        except (Exception,):
            return template_str
        return text

    def _get_translation(
            self,
            key: str,
            default: Optional[str] = None
    ) -> Optional[str]:
        if "." in key:
            return self._get_nested(self.translations, key, default)
        return self.translations.get(key, default)

    @classmethod
    def _get_nested(
            cls,
            data: t.Dict[str, t.Any],
            dotted_key: str,
            default: Optional[Any] = None
    ) -> Any:
        keys = dotted_key.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
