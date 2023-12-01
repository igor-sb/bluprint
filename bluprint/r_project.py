"""Create an R project for bluprint."""

import subprocess
import sys
from pathlib import Path, PosixPath

from bluprint.demo import copy_rproj_file
from bluprint.errors import RenvInitError, RpackageMissingError


def create_r_project(
    project_name: str,
    project_dir: str | None = None,
) -> None:
    if not project_dir:
        project_dir = '.'
    run_renv_init(Path(project_dir) / project_name)
    run_renv_install('reticulate', Path(project_dir) / project_name)
    copy_rproj_file(project_name, Path(project_dir) / project_name)


def check_if_r_package_is_installed(package: str) -> None:
    r_error_msg = subprocess.run(
        ['Rscript', '-e', f'library({package})'],
        capture_output=True,
    ).stderr.decode('utf-8')
    if r_error_msg.startswith(f'Error in library({package})'):
        raise RpackageMissingError(r_error_msg)


def run_renv_init(project_dir: str | PosixPath):
    r_error_msg = subprocess.run(
        ['Rscript', '-e', 'renv::init()'],
        capture_output=True,
        cwd=project_dir,
    ).stderr.decode('utf-8')
    if r_error_msg:
        raise RenvInitError(r_error_msg)


def run_renv_install(package: str, project_dir: str | PosixPath) -> str:
    r_error_msg = subprocess.run(
        ['Rscript', '-e', f'renv::install("{package}")'],
        capture_output=True,
        cwd=project_dir,
    ).stderr.decode('utf-8')
    if r_error_msg:
        sys.stderr.write(r_error_msg)
