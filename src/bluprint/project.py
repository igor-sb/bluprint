"""Validators for project creation / initialization."""

import os
import re
import shutil
from pathlib import Path

from importlib_resources import files

from bluprint.binary import check_if_executable_is_installed
from bluprint.colors import progress_log, styled_print
from bluprint.create.r_project import check_if_r_package_is_installed
from bluprint.errors import ProjectExistsError
from bluprint.template import example_files, r_files


@progress_log('checking if project can be created...')
def check_if_project_can_be_created(
    project_name: str,
    parent_dir: str | None = None,
    r_project: bool = False,
) -> None:
    check_if_project_dir_exists(project_name, parent_dir)
    check_if_executable_is_installed('uv')
    if r_project:
        check_if_executable_is_installed('Rscript')
        check_if_r_package_is_installed('renv')


def check_if_project_dir_exists(
    project_name: str,
    parent_dir: str | None,
) -> None:
    if not parent_dir:
        parent_dir = get_current_working_dir()
    if (Path(parent_dir) / project_name).is_dir():
        raise ProjectExistsError(f'{project_name} directory exists.')


def check_if_project_files_exist(
    project_name: str,
    project_dir: str,
    overwrite: bool = False,
) -> str:
    if (Path(project_dir) / 'pyproject.toml').exists():
        raise ProjectExistsError(
            f'pyproject.toml already exists in {project_dir}: '
            + 'cannot initialize new bluprint project',
        )
    if overwrite:
        styled_print('overwriting existing files')
        return 'overwrite'
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
    return 'ok'


def copy_template(
    src_path: str | Path,
    dst_path: str | Path,
    project_name: str = 'placeholder_name',
    omit_examples: bool = False,
    keep_r_files: bool = False,
    overwrite: bool = False,
) -> None:
    src_path_regex = re.escape(str(src_path))

    for src_root, src_dirs, src_files in os.walk(src_path):
        dst_root = re.sub(f'^{src_path_regex}', str(dst_path), src_root)
        for src_dir in src_dirs:
            if not (Path(dst_root) / src_dir).exists():
                (Path(dst_root) / src_dir).mkdir()
        for src_file in src_files:
            src_file_path = Path(src_root) / src_file
            dst_file_path = Path(dst_root) / src_file
            src_is_example = is_example_file(
                src_file_path,
                src_path,
                project_name,
            )
            src_is_rfile = is_r_file(src_file_path, src_path)
            if overwrite or not dst_file_path.exists():
                if (
                    (omit_examples and src_is_example) or
                    (not keep_r_files and src_is_rfile)
                ):
                    continue
                shutil.copyfile(src_file_path, dst_file_path)


def is_example_file(
    filename: str | Path,
    parent_dir: str | Path,
    project_name: str,
) -> bool:
    file_relative_to_parent = Path(filename).relative_to(parent_dir)
    project_example_files = example_files(project_name)
    return file_relative_to_parent in project_example_files


def is_r_file(filename: str | Path, parent_dir: str | Path) -> bool:
    file_relative_to_parent = Path(filename).relative_to(parent_dir)
    return file_relative_to_parent in r_files()


def get_current_working_dir() -> str:
    return str(Path.cwd())


def absolute_path_in_project(path_to_file: str | Path) -> Path:
    """Return an absolute path to a file in a Bluprint project

    Args:
        path_to_file (str | Path): Relative path to a file.

    Returns:
        Path: pathlib Path object specifying the absolute path to file.
    """
    dir_name = str(Path(path_to_file).parent)
    if dir_name == '.':
        return Path(files(path_to_file).joinpath('_').parent)
    dir_as_module = dir_name.strip('/').replace('/', '.')
    file_basename = Path(path_to_file).name
    return Path(files(dir_as_module).joinpath(file_basename))
