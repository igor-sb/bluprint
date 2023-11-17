"""Command-line interface for bluprint."""

import os
import subprocess

import fire

from bluprint.binary import Executable, check_if_executable_is_installed
from bluprint.demo import create_demo_py_module, create_demo_readme_md


def latest_python_version() -> str:
    check_if_executable_is_installed('pyenv')
    python_version = subprocess.run(
        '{list_versions} | {select_stable} | {get_last}'.format(
            list_versions='pyenv install -l',
            select_stable=r'grep -E "\s[0-9]+\.[0-9]+\.[0-9]+$"',
            get_last='tail -n 1',
        ),
        capture_output=True,
        shell=True,  # noqa: S602
    )
    return python_version.stdout.decode('UTF-8').strip()


def create_project_folder_skeleton(project_name: str) -> None:
    for folder in ('.venv', 'conf', 'notebooks', f'{project_name}'):
        os.makedirs(f'{project_name}/{folder}')


def initalize_poetry(project_name: str, python_version: str) -> None:
    Executable([
        'poetry',
        'init',
        '--no-interaction',
        f'--name={project_name}',
        f'--python={python_version}',
        f'--directory={project_name}',
    ])


def create_gitignore(project_name: str) -> None:
    with open(f'{project_name}/.gitignore', 'w') as gitignore:
        gitignore.write('**/__pycache__/\n.venv')


def main(project_name: str, python_version: str | None) -> None:
    for executable in ('pyenv', 'poetry', 'git', 'gh'):
        check_if_executable_is_installed(executable)
    create_project_folder_skeleton(project_name)
    if not python_version:
        python_version = latest_python_version()
    initalize_poetry(project_name, python_version)
    create_demo_readme_md(project_name)
    create_demo_py_module(project_name, 'example.py')
    # create_example_notebook(project_name, 'example_notebook.ipynb')
    # create example_workflow(project_name)
    create_gitignore(project_name)


if __name__ == '__main__':
    fire.Fire(main)
