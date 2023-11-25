"""Create a bluprint project."""

import subprocess
import sys
from pathlib import Path

import fire

from bluprint.binary import check_if_executable_is_installed
from bluprint.demo import copy_demo_files, create_demo_readme_md


def latest_python_version() -> str:
    python_version = subprocess.run(
        '{list_versions} | {select_stable} | {get_latest}'.format(
            list_versions='pyenv install -l',
            select_stable=r'grep -E "\s[0-9]+\.[0-9]+\.[0-9]+$"',
            get_latest='tail -n 1',
        ),
        capture_output=True,
        shell=True,  # noqa: S602
    )
    return python_version.stdout.decode('utf-8').strip()


def create_project_directory_skeleton(
    project_name: str,
    parent_dir: str = '.',
    directories: tuple[str, ...] = ('.venv', 'conf', 'notebooks'),
) -> None:
    sys.stderr.write('Creating directory skeleton:')
    sys.stderr.flush()
    for folder in (*directories, f'{project_name}'):
        folder_path = Path(parent_dir) / project_name / folder
        folder_path.mkdir(parents=True)
    sys.stderr.write(' ✓\n')


def initalize_poetry(
    project_name: str,
    python_version: str,
    working_dir: str,
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


def install_project_as_editable_package(
    project_dir: str = '.',
) -> None:
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
    sys.stderr.write(f'Setting Python version: {python_version}. ✓\n')
    initalize_poetry(project_name, python_version, project_dir)
    create_demo_readme_md(project_name, project_dir)
    copy_demo_files(project_name, project_dir)
    install_project_as_editable_package(project_dir)


if __name__ == '__main__':
    fire.Fire(create_project)
