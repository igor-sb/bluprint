"""Create an R project for bluprint."""

from pathlib import Path

from bluprint.binary import rcmd, renv_init, renv_install
from bluprint.create.errors import RpackageMissingError
from bluprint.template import copy_rproj_file


def initialize_r_project(
    project_name: str,
    parent_dir: str | None = None,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    renv_init(project_dir)
    renv_install(['reticulate', 'here'], project_dir)
    copy_rproj_file(project_name, project_dir)


def check_if_r_package_is_installed(package: str) -> None:
    rcmd(f'library({package})', RpackageMissingError)
