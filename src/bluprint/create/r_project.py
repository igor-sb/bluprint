"""Create an R project for bluprint."""

from pathlib import Path

from bluprint.binary import rcmd
from bluprint.create.errors import (
    RenvInitError,
    RenvInstallError,
    RpackageMissingError,
)
from bluprint.demo import copy_rproj_file


def create_r_project(
    project_name: str,
    project_dir: str | None = None,
) -> None:
    if not project_dir:
        project_dir = '.'
    working_dir = Path(project_dir) / project_name
    rcmd('renv::init()', RenvInitError, cwd=working_dir)
    rcmd('renv::install("reticulate")', RenvInstallError, cwd=working_dir)
    copy_rproj_file(project_name, working_dir)


def check_if_r_package_is_installed(package: str) -> None:
    rcmd(f'library({package})', RpackageMissingError)
