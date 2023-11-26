"""Placeholder file contents for new projects."""

import shutil
import sys
from importlib import resources
from importlib.abc import Traversable
from pathlib import Path, PosixPath


def copy_demo_files(
    project_name: str,
    project_dir: str | Path | PosixPath,
) -> None:
    demo_path = str(dir_in_package('demo'))
    sys.stderr.write('Copying demo generic files:')
    shutil.copytree(
        src=Path(demo_path),
        dst=project_dir,
        ignore=shutil.ignore_patterns('project'),
        dirs_exist_ok=True,
    )
    sys.stderr.write(' ✓\n')
    sys.stderr.write('Copying demo project files:')
    shutil.copytree(
        src=Path(demo_path) / 'project',
        dst=Path(project_dir) / project_name,
        dirs_exist_ok=True,
    )
    sys.stderr.write(' ✓\n')


def dir_in_package(package_dir: str) -> PosixPath | Traversable:
    return resources.files(package_dir).joinpath('')
