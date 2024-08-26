"""Validators for project creation / initialization."""

import os
import re
import shutil
from pathlib import Path

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
    keep_examples: bool = True,
    keep_r_files: bool = False,
    overwrite: str ='never',
) -> None:
    src_path_regex = re.escape(str(src_path))
    project_example_files = example_files(project_name)
    project_r_files = r_files()
    print(example_files(project_name))
    for src_root, src_dirs, src_files in os.walk(src_path):
        dst_root = re.sub(f'^{src_path_regex}', str(dst_path), src_root)
        for src_dir in src_dirs:
            if not (Path(dst_root) / src_dir).exists():
                (Path(dst_root) / src_dir).mkdir()
        for src_file in src_files:
            src_file_path = Path(src_root) / src_file
            dst_file_path = Path(dst_root) / src_file
            src_file_relative_to_project = src_file_path.relative_to(src_path)
            if (
                (dst_file_path.exists() and overwrite == 'always') or
                (not dst_file_path.exists())
            ):
                print(src_file_relative_to_project)
                print(src_file_relative_to_project in project_example_files)
                # Check if file is an example if keep_examples is off
                # Check if file is an r file if keep_r_files is off
                if (
                    keep_examples or
                    (src_file_relative_to_project not in project_example_files)
                ):
                    shutil.copyfile(src_file_path, dst_file_path)


def get_current_working_dir() -> str:
    return os.getcwd()
