"""Placeholder file contents for new projects."""

import shutil
from pathlib import Path

from importlib_resources import files


def copy_demo_files(
    project_name: str,
    project_dir: str | Path,
) -> None:
    demo_path = files('bluprint').joinpath('demo')
    shutil.copytree(
        src=Path(demo_path),
        dst=project_dir,
        ignore=shutil.ignore_patterns('project', '*.html', '*.Rproj'),
        dirs_exist_ok=True,
    )
    shutil.copytree(
        src=Path(demo_path) / 'project',
        dst=Path(project_dir) / project_name,
        dirs_exist_ok=True,
    )


def copy_rproj_file(
    project_name: str,
    project_dir: str | Path,
) -> None:
    demo_path = files('bluprint').joinpath('demo')
    shutil.copyfile(
        src=Path(demo_path) / 'project.Rproj',
        dst=Path(project_dir) / f'{project_name}.Rproj',
    )
