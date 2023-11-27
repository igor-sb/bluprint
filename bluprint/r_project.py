"""Create an R project for bluprint."""

from pathlib import Path

import subprocess

from bluprint.errors import RpackageMissingError
from bluprint.project import check_if_executable_is_installed


def create_r_project(project_name: str, project_dir: str | None = None):
    if not project_dir:
        project_dir = '.'
    check_if_executable_is_installed('Rscript')
    check_if_r_package_is_installed('renv')
    check_if_r_package_is_installed('reticulate')
    run_renv_init(Path(project_dir) / project_name)


def check_if_r_package_is_installed(package: str) -> None:
    r_out = subprocess.run(
        ['Rscript', '-e', f'library({package})'],
        capture_output=True,
    )
    r_error_msg = 'Error in library(renv) : there is no package called ‘renv’'
    if r_out.stderr.decode('utf-8').startswith(r_error_msg):
        raise RpackageMissingError(f'{package} package is missing.')


def run_renv_init(project_dir):
    r_out = subprocess.run(
        ['Rscript', '-e', 'renv::init()'],
        capture_output=True,
        cwd=project_dir,
    )