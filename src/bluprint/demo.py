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
    project_dir: str | Path | PosixPath,
) -> None:
    demo_path = str(dir_in_package('demo'))
    shutil.copyfile(
        src=Path(demo_path) / 'project.Rproj',
        dst=Path(project_dir) / f'{project_name}.Rproj',
    )


def dir_in_package(package_dir: str) -> PosixPath | Traversable:
    return resources.files(package_dir).joinpath('')
