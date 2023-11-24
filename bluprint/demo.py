"""Placeholder file contents for new projects."""

import shutil
from importlib import resources
from pathlib import Path, PosixPath


def create_demo_readme_md(project_name: str) -> None:
    with open(f'{project_name}/README.md', 'w') as readme:
        readme.write(f'#{project_name}\n Description.')


def copy_demo_files(
    project_name: str,
    project_path: str | Path | PosixPath,
) -> None:
    demo_path = str(resources.files('demo').joinpath(''))
    shutil.copytree(
        src=Path(demo_path),
        dst=project_path,
        ignore=shutil.ignore_patterns('project'),
    )
    shutil.copytree(
        src=Path(demo_path) / 'project',
        dst=Path(project_path) / project_name,
    )
