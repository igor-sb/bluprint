"""Create a bluprint project."""

import re
import subprocess
from pathlib import Path, PosixPath

import fire

from bluprint.binary import check_if_executable_is_installed
from bluprint.demo import copy_demo_files


def latest_python_version() -> str:
    pyenv_out = subprocess.run(['pyenv', 'install', '-l'], capture_output=True)
    stable_re = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+$')

    for pyenv_version in pyenv_out.stdout.decode('utf-8').split('\n'):
        stable_version = stable_re.match(pyenv_version.strip())
        if stable_version:
            latest_stable_version = stable_version.group(0)
    return latest_stable_version


def create_project_directory_skeleton(
    project_name: str,
    parent_dir: str = '.',
    directories: tuple[str, ...] = ('.venv', 'conf', 'notebooks'),
) -> None:
    for folder in (*directories, f'{project_name}'):
        folder_path = Path(parent_dir) / project_name / folder
        folder_path.mkdir(parents=True)


def initalize_poetry(
    project_name: str,
    python_version: str,
    working_dir: str | Path | PosixPath,
) -> None:
    subprocess.run(
        [  # noqa: WPS317
            'poetry', 'init',
            '--no-interaction',
            '--name', project_name,
            '--python', python_version,
        ],
        cwd=working_dir,
    )


def install_project_as_editable_package(project_dir: str | Path = '.') -> None:
    subprocess.run(
        ['poetry', 'run', 'pip', 'install', '-e', '.'],
        cwd=project_dir,
        capture_output=True,
    )


def create_project(
    project_name: str,
    python_version: str | None = None,
    parent_dir: str | None = None,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    for executable in ('pyenv', 'poetry'):
        check_if_executable_is_installed(executable)
    create_project_directory_skeleton(project_name, parent_dir)
    if not python_version:
        python_version = latest_python_version()
    initalize_poetry(project_name, python_version, project_dir)
    copy_demo_files(project_name, project_dir)
    install_project_as_editable_package(project_dir)


if __name__ == '__main__':
    fire.Fire(create_project)
