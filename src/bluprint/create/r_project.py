"""Create an R project for bluprint."""

from pathlib import Path

from bluprint.binary import rcmd, renv_init, renv_install
from bluprint.colors import styled_print
from bluprint.create.errors import RenvSnapshotError, RpackageMissingError
from bluprint.template import copy_rproj_files


def initialize_r_project(
    project_name: str,
    parent_dir: str | None = None,
) -> None:
    r_packages = ('reticulate', 'here', 'knitr', 'rmarkdown')
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    styled_print('initalizing renv...', endline='')
    renv_init(project_dir)
    styled_print(' Ok.', print_bluprint=False)
    # Use Rstudio package manager for faster install
    styled_print('installing reticulate, here, knitr...', endline='')
    renv_install(r_packages, project_dir)
    styled_print(' Ok.', print_bluprint=False)
    styled_print('installing reticulate, here, knitr...', endline='')
    rcmd('renv::snapshot()', RenvSnapshotError, cwd=project_dir)
    copy_rproj_files(project_name, project_dir)


def check_if_r_package_is_installed(package: str) -> None:
    rcmd(f'library({package})', RpackageMissingError)
