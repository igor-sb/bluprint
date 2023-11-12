"""Command-line interface for bluprint."""

import os

import fire

from bluprint.binary import Executable, check_if_executable_is_installed


def create_project_folder_skeleton(project_name: str) -> None:
    for folder in ('.github/workflows', 'conf', 'notebooks'):
        os.makedirs(f'{project_name}/{folder}')
    os.makedirs(f'{project_name}/{project_name}')


def initalize_poetry(project_name: str, python_version: str) -> None:
    Executable([
        'poetry',
        'config',
        '--local',
        'virtualenvs.in-project',
        'true',
    ])
    Executable([
        'poetry',
        'init',
        '--no-interaction',
        f'--name={project_name}',
        f'--python={python_version}',
        f'--directory={project_name}',
    ])


def main(project_name: str) -> None:
    for executable in ('poetry', 'git', 'gh'):
        check_if_executable_is_installed(executable)
    create_project_folder_skeleton(project_name)
