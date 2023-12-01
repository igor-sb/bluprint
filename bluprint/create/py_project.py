"""Create a bluprint project."""

import json
import re
import subprocess
from pathlib import Path, PosixPath

from bluprint.create.errors import PoetryAddError
from bluprint.demo import copy_demo_files


def create_project(
    project_name: str,
    python_version: str | None = None,
    parent_dir: str | None = None,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    create_project_directory_skeleton(project_name, parent_dir)
    if not python_version:
        python_version = latest_python_version()
    initalize_poetry(project_name, python_version, project_dir)
    copy_demo_files(project_name, project_dir)
    interpolate_project_name_in_example_nbs(project_name, project_dir)
    for package in ('ipykernel', 'pandas'):
        install_python_package(package, project_dir)
    install_project_as_editable_package(project_dir)


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


def interpolate_project_name_in_example_nbs(
    project_name: str,
    project_dir: str | Path | PosixPath,
) -> None:
    example_ipynb = Path(project_dir) / 'notebooks' / 'example_jupyternb.ipynb'
    with open(example_ipynb) as example_ipynb_file:
        example_ipynb_data = json.load(example_ipynb_file)

    example_ipynb_data['cells'][2]['source'] = (
        example_ipynb_data['cells'][2]['source'][0]  # noqa: WPS219
        .replace('{{project}}', project_name)
    )
    with open(example_ipynb, 'w') as example_ipynb_file:  # noqa: WPS440
        json.dump(example_ipynb_data, example_ipynb_file)


def install_python_package(
    package: str,
    project_dir: str | Path | PosixPath,
) -> None:
    subprocess.run(
        ['poetry', 'env', 'use', '3.11.2'],
        cwd=project_dir,
        capture_output=True,
    )
    poetry_err = subprocess.run(
        ['poetry', 'add', package],
        cwd=project_dir,
        capture_output=True,
    ).stderr.decode('utf-8')
    if poetry_err:
        raise PoetryAddError(poetry_err)


def install_project_as_editable_package(project_dir: str | Path = '.') -> None:
    subprocess.run(
        ['poetry', 'run', 'pip', 'install', '-e', '.'],
        cwd=project_dir,
        capture_output=True,
    )


def latest_python_version() -> str:
    pyenv_out = subprocess.run(['pyenv', 'install', '-l'], capture_output=True)
    stable_re = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+$')

    for pyenv_version in pyenv_out.stdout.decode('utf-8').split('\n'):
        stable_version = stable_re.match(pyenv_version.strip())
        if stable_version:
            latest_stable_version = stable_version.group(0)
    return latest_stable_version
