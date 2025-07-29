import typing as t
from pathlib import Path

import click

from .generator import ProjectGenerator
from .survey import run_survey
from .utils import is_valid_project_name


@click.group(
    invoke_without_command=True,
    add_help_option=False,
    context_settings={"ignore_unknown_options": True}
)
@click.pass_context
def cli(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        click.echo(
            "aiogram-blueprint: generate a new aiogram project from a blueprint.\n\n"
            "Usage:\n"
            "  aiogram-blueprint create <project_name>\n\n"
            "Example:\n"
            "  aiogram-blueprint create app\n"
        )


@cli.command(add_help_option=False)
@click.argument("project_name", required=True, metavar="project_name")
def create(project_name: str) -> None:
    try:
        project_name = resolve_project_name(project_name)

        click.clear()
        click.secho("> Welcome to the aiogram-blueprint project generator!\n", fg="blue", bold=True)

        config = run_survey()
        dst_dir = Path.cwd()
        project_path = dst_dir / project_name

        generator = ProjectGenerator(config, dst_dir, project_name)
        generator.copy_or_render()

        click.secho(f"\n[+] Project '{project_name}' created successfully at:", fg="green", bold=True, nl=False)
        click.secho(f"\n    {project_path}", fg="cyan", bold=True)

        print_final_instructions(project_name, config)

    except KeyboardInterrupt:
        click.secho("\nOperation cancelled by user.", fg="red", bold=True)


def resolve_project_name(project_name: t.Optional[str]) -> str:
    if not is_valid_project_name(project_name):
        click.secho(
            "Invalid project name! Use only letters, numbers, underscores, "
            "do not start with a digit, and avoid Python keywords.",
            fg="red", bold=True
        )
        raise click.BadParameter("Invalid project name")

    dst_dir = Path.cwd()
    project_path = dst_dir / project_name

    if project_path.exists():
        click.secho(
            f"File or directory '{project_name}' already exists! Please choose another name.",
            fg="red", bold=True
        )
        raise click.BadParameter("Project path already exists")

    return project_name


def print_final_instructions(project_name: str, config: t.Dict[str, t.Any]) -> None:
    click.secho("\n[>] Next steps:", fg="yellow", bold=True)
    click.secho("    1. Install dependencies: pip install -r requirements.txt", fg="blue")
    click.secho("    2. Fill in your .env file with real values", fg="blue")

    if config.get("use_db", False):
        click.secho("    3. Initialize database: alembic revision --autogenerate -m 'Initial migration'", fg="blue")
        click.secho("    4. Apply migrations: alembic upgrade head", fg="blue")
        click.secho(f"    5. Run your bot: python -m {project_name}", fg="blue")
    else:
        click.secho(f"    3. Run your bot: python -m {project_name}", fg="blue")

    click.secho("\n[+] Start building your bot!", fg="green")


if __name__ == "__main__":
    cli()
