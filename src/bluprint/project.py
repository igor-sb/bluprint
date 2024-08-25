"""Validators for project creation / initialization."""

from pathlib import Path

from bluprint.binary import check_if_executable_is_installed
from bluprint.colors import progress_log, styled_print
from bluprint.create.py_project import get_current_working_dir
from bluprint.create.r_project import check_if_r_package_is_installed
from bluprint.errors import ProjectExistsError


@progress_log('checking if project can be created...')
def check_if_project_can_be_created(
    project_name: str,
    parent_dir: str | None = None,
    r_project: bool = False,
) -> None:
    check_if_project_exists(project_name, parent_dir)
    check_if_executable_is_installed('uv')
    if r_project:
        check_if_executable_is_installed('Rscript')
        check_if_r_package_is_installed('renv')


def check_if_project_exists(project_name: str, parent_dir: str | None) -> None:
    if not parent_dir:
        parent_dir = get_current_working_dir()
    if (Path(parent_dir) / project_name).is_dir():
        raise ProjectExistsError(f'{project_name} directory exists.')


def check_if_project_files_exist(
    project_name: str,
    project_dir: str,
    overwrite: bool = False,
) -> None:
    if (Path(project_dir) / 'pyproject.toml').exists():
        raise ProjectExistsError(
            f'pyproject.toml already exists in {project_dir}: '
            + 'cannot initialize new bluprint project',
        )
    if overwrite:
        styled_print('overwriting existing files')
        return
    project_files = ('.gitignore', 'README.md', 'uv.lock')
    project_dirs = ('.venv', 'conf', 'data', 'notebooks', project_name)
    for file_in_project in project_files:
        if (Path(project_dir) / file_in_project).exists():
            raise ProjectExistsError(
                f'Error: {file_in_project} file already exists.',
            )
    for dir_in_project in project_dirs:
        if (Path(project_dir) / dir_in_project).exists():
            raise ProjectExistsError(
                f'Error: {dir_in_project} directory already exists.',
            )
