import keyword
import re
import shutil
from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
)


def get_template_dir() -> Path:
    return Path(__file__).parent / "template"


def has_j2_version(src_path: Path) -> bool:
    return src_path.with_suffix(src_path.suffix + ".j2").exists()


def copy_file(src_path: Path, dst_path: Path) -> None:
    shutil.copy2(src_path, dst_path)


def render_jinja_template(src_path: Path, dst_path: Path, context: dict) -> None:
    template_dir = src_path.parent
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(src_path.name)
    dst_path.write_text(template.render(**context), encoding="utf-8")


def check_file_conditions(src_path: Path, rel_path: Path, config: dict) -> bool:
    if (src_path.name == "db.py"
            and "middlewares" in rel_path.parts
            and not config.get("use_db", False)):
        return False

    if (src_path.name == "alembic.ini"
            and not config.get("use_db", False)):
        return False

    return True


def is_valid_project_name(name: str) -> bool:
    try:
        is_identifier = re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name) is not None
        is_not_keyword = not keyword.iskeyword(name)
    except (Exception,):
        return False
    return is_identifier and is_not_keyword
