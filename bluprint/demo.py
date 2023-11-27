"""Placeholder file contents for new projects."""

import shutil
from importlib import resources
from importlib.abc import Traversable
from pathlib import Path, PosixPath


def copy_demo_files(
    project_name: str,
    project_dir: str | Path | PosixPath,
) -> None:
    demo_path = str(dir_in_package('demo'))
    shutil.copytree(
        src=Path(demo_path),
        dst=project_dir,
        ignore=shutil.ignore_patterns(['project', '*.Rmd', '*.R']),
        dirs_exist_ok=True,
    )
    shutil.copytree(
        src=Path(demo_path) / 'project',
        dst=Path(project_dir) / project_name,
        dirs_exist_ok=True,
    )


def dir_in_package(package_dir: str) -> PosixPath | Traversable:
    return resources.files(package_dir).joinpath('')
