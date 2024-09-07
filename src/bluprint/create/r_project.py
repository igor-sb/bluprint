"""Create an R project for bluprint."""

from pathlib import Path

from bluprint.binary import rcmd, renv_create_snapshot, renv_init, renv_install
from bluprint.colors import progress_log
from bluprint.create.errors import RpackageMissingError
from bluprint.template import Placeholder


@progress_log('creating R project', print_ok=False)
def create_r_project(
    project_name: str,
    parent_dir: str | None = None,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    initialize_r_project(project_name, project_dir)


@progress_log('initializing R project', print_ok=False)
def initialize_r_project(
    project_name: str,
    project_dir: str | Path = '.',
) -> None:
    r_packages = ('reticulate', 'here')
    renv_init(project_dir)
    renv_install(r_packages, project_dir)
    renv_create_snapshot(project_dir)
    Path.rename(
        Path(project_dir) / f'{Placeholder.project_name}.Rproj',
        Path(project_dir) / f'{project_name}.Rproj',
    )


def check_if_r_package_is_installed(package: str) -> None:
    rcmd(f'library({package})', RpackageMissingError)
