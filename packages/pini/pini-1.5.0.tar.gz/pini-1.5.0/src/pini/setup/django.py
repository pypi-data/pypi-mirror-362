import subprocess
from pathlib import Path

import typer

from pini.setup.python_base import install_python_base


def install_django(
    project_name: str,
    author: str,
    email: str,
    init_git: bool,
    init_commitizen: bool,
    init_linters: bool,
    init_pre_commit_hooks: bool,
):
    install_python_base(
        project_name,
        author,
        email,
        init_git,
        init_commitizen,
        init_linters,
        init_pre_commit_hooks,
    )

    typer.echo(f"🚀 Bootstrapping Django project: {project_name}")

    project_path = Path(project_name)

    subprocess.run(
        ["uv", "add", "django"],
        cwd=project_path,
        check=True,
    )
    typer.echo("✅ Django installed.")

    subprocess.run(
        ["uv", "run", "django-admin", "startproject", "core", "."],
        cwd=project_path,
        check=True,
    )

    typer.echo("🎉 Django project setup complete!")
