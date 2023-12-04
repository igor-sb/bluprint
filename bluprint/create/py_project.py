"""Create a bluprint project."""

import json
from pathlib import Path, PosixPath

from bluprint.binary import run
from bluprint.create.errors import (
    PoetryAddError,
    PoetryInitError,
    PoetryRunError,
    PythonVersionError,
)
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
        python_version = get_python_version()
    initalize_poetry(project_name, python_version, project_dir)
    copy_demo_files(project_name, project_dir)
    interpolate_project_name_in_example_nbs(project_name, project_dir)
    for package in ('ipykernel', 'pandas'):
        run(['poetry', 'add', package], PoetryAddError, cwd=project_dir)
    run(['pyenv', 'local', python_version], PoetryRunError, cwd=project_dir)
    tmp = run(['poetry', 'install'], PoetryRunError, cwd=project_dir)
    print(tmp)
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
    run(
        [
            'poetry',
            'init',
            '-n',
            '--name',
            project_name,
            '--python',
            f'~{python_version}',
        ],
        PoetryInitError,
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


def install_project_as_editable_package(project_dir: str | Path = '.') -> None:
    run(
        ['poetry', 'run', 'pip', 'install', '-e', '.'],
        PoetryRunError,
        cwd=project_dir,
    )


def get_python_version() -> str:
    python_out = run(['python', '--version'], PythonVersionError)
    return python_out.strip().replace('Python ', '')
