import os
import typing as t
from dataclasses import dataclass
from pathlib import Path

from .constants import COMPONENT_FOLDERS
from .utils import (
    copy_file,
    check_file_conditions,
    has_j2_version,
    get_template_dir,
    render_jinja_template,
)


@dataclass
class FileInfo:
    src_path: Path
    dst_path: Path
    should_render: bool = False


class ProjectGenerator:
    def __init__(self, config: dict, dst_dir: Path, project_name: str) -> None:
        self.config = config
        self.dst_dir = dst_dir
        self.project_name = project_name
        self.template_dir = get_template_dir()
        self.allowed_folders = self._get_allowed_folders()

    def copy_or_render(self) -> None:
        try:
            files_to_copy = self._collect_files()
            self._process_files(files_to_copy)
        except Exception as e:
            raise RuntimeError(f"Failed to generate project: {e}") from e

    def _get_allowed_folders(self) -> t.Set[str]:
        return {name for name, cond in COMPONENT_FOLDERS.items() if cond(self.config)}

    def _collect_files(self) -> t.List[FileInfo]:
        result: t.List[FileInfo] = []

        for src_path in self._walk_template():
            if not self._should_include_path(src_path):
                continue

            dst_path = self._get_destination_path(src_path)
            should_render = src_path.suffix == ".j2"

            if should_render:
                dst_path = dst_path.with_suffix("")
            elif has_j2_version(src_path):
                continue

            result.append(FileInfo(src_path, dst_path, should_render))

        return result

    def _walk_template(self) -> t.Generator[Path, None, None]:
        for root, dirs, files in os.walk(self.template_dir):
            root_path = Path(root)
            self._filter_directories(root_path, dirs)
            for file in files:
                yield root_path / file

    def _filter_directories(self, current_path: Path, dirs: t.List[str]) -> None:
        rel_path = current_path.relative_to(self.template_dir)
        dirs[:] = [d for d in dirs if self._should_include_directory(rel_path / d)]

    def _should_include_directory(self, rel_path: Path) -> bool:
        parts = rel_path.parts
        if not parts:
            return True

        top = parts[0]

        if len(parts) > 1 and top == "project":
            return self._check_nested_conditions(parts[1:])
        if top in COMPONENT_FOLDERS:
            return top in self.allowed_folders
        return True

    def _check_nested_conditions(self, parts: tuple[str, ...]) -> bool:
        match parts:
            case ["services", service, *_]:
                return service in self.allowed_folders
            case ["services", *_]:
                return "services" in self.allowed_folders
            case ["app", "admin", *_]:
                return "app" in self.allowed_folders and "admin" in self.allowed_folders
            case ["app", *_]:
                return "app" in self.allowed_folders
        return True

    def _should_include_path(self, src_path: Path) -> bool:
        rel_path = src_path.relative_to(self.template_dir)
        if not self._should_include_directory(rel_path.parent):
            return False
        return check_file_conditions(src_path, rel_path, self.config)

    def _get_destination_path(self, src_path: Path) -> Path:
        rel_path = src_path.relative_to(self.template_dir)
        parts = list(rel_path.parts)

        if "project" in parts:
            parts[parts.index("project")] = self.project_name

        return self.dst_dir.joinpath(*parts)

    def _process_files(self, files: t.List[FileInfo]) -> None:
        for file_info in files:
            file_info.dst_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                if file_info.should_render:
                    render_jinja_template(
                        file_info.src_path,
                        file_info.dst_path,
                        self._get_template_context()
                    )
                else:
                    copy_file(file_info.src_path, file_info.dst_path)
            except Exception as e:
                raise RuntimeError(f"Failed to process {file_info.src_path}: {e}") from e

    def _get_template_context(self) -> dict:
        return {**self.config, "project_name": self.project_name}
