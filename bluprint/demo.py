"""Placeholder file contents for new projects."""

import importlib
from pathlib import PosixPath
import shutil


def create_demo_readme_md(project_name: str) -> None:
    with open(f'{project_name}/README.md', 'w') as readme:
        readme.write(f'#{project_name}\n Description.')


def copy_demo_files(
    project_name: str | PosixPath,
    project_path: PosixPath,
) -> None:
    demo_path = importlib.resources.files('demo').joinpath('')
    shutil.copytree(
        src=demo_path,
        dst=project_path,
        ignore=shutil.ignore_patterns('project'),
    )
    shutil.copytree(
        src=demo_path / 'project',
        dst=project_path / project_name,
    )
