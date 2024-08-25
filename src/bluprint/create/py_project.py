"""Create a bluprint project."""

import os
import shutil
from pathlib import Path

from importlib_resources import files
from packaging.version import Version

from bluprint.binary import run, uv_add, uv_init
from bluprint.colors import progress_log
from bluprint.create.errors import LowPythonVersionError, PythonVersionError
from bluprint.create.template_setup import (
    delete_examples_from_project,
    delete_r_files_from_template,
    replace_git_account_name,
    replace_placeholder_name_in_file,
    replace_placeholder_name_in_notebook,
)

MIN_PYTHON_VERSION = '3.11'


def create_project(
    project_name: str,
    python_version: str | None = None,
    parent_dir: str | None = None,
    template_dir: str | None = None,
    add_examples: bool = True,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    project_dir.mkdir(parents=True)
    initialize_project(
        project_name,
        python_version,
        project_dir,
        template_dir,
        add_examples,
    )


@progress_log('initializing project...')
def initialize_project(
    project_name: str,
    python_version: str | None = None,
    project_dir: str | Path = '.',
    template_dir: str | None = None,
    add_examples: bool = True,
) -> None:
    if not python_version:
        python_version = default_python_version()
    if not template_dir:
        template_dir = files('bluprint').joinpath('template')
    uv_init(python_version, str(project_dir))
    os.remove(Path(project_dir) / 'src' / project_name / '__init__.py')
    os.rmdir(Path(project_dir) / 'src' / project_name)
    os.rmdir(Path(project_dir) / 'src')
    shutil.copytree(
        template_dir,  # type: ignore
        project_dir,
        dirs_exist_ok=True,
    )
    os.rename(
        Path(project_dir) / 'placeholder_name',
        Path(project_dir) / project_name,
    )
    delete_r_files_from_template(project_dir)
    replace_placeholder_name_in_file(
        Path(project_dir) / 'README.md',
        project_name,
    )
    replace_placeholder_name_in_file(
        Path(project_dir) / 'pyproject.toml',
        project_name,
    )
    replace_placeholder_name_in_file(
        Path(project_dir) / 'notebooks' / 'example_quarto.qmd',
        project_name,
    )
    replace_placeholder_name_in_notebook(
        Path(project_dir) / 'notebooks' / 'example_jupyternb.ipynb',
        project_name,
    )
    if not add_examples:
        delete_examples_from_project(project_name, project_dir)
    replace_git_account_name(project_dir)
    uv_add(['bluprint_conf', 'ipykernel', 'pandas'], project_dir)


def default_python_version(min_version: str = MIN_PYTHON_VERSION) -> str:
    python_out = run(['python', '--version'], PythonVersionError)
    py_version = python_out.strip().replace('Python ', '')
    if Version(py_version) >= Version(min_version):
        return py_version
    return min_version


@progress_log('checking Python version...')
def check_python_version(
    python_version: str | None,
) -> None:
    if python_version and (Version(python_version) < Version(MIN_PYTHON_VERSION)):
        raise LowPythonVersionError('Bluprint requires Python >= 3.11.')
