"""Create a bluprint project."""

import re
from pathlib import Path

import nbformat
from importlib_resources import files
from packaging.version import Version

from bluprint.binary import uv_add, uv_init, run
from bluprint.create.errors import (
    GitError,
    LowPythonVersionError,
    PythonVersionError,
)

MIN_PYTHON_VERSION = '3.11'


def create_project(
    project_name: str,
    python_version: str | None = None,
    parent_dir: str | None = None,
    template_dir: str | None = None,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    project_dir.mkdir(parents=True)
    initialize_project(project_name, python_version, project_dir, template_dir)


def initialize_project(
    project_name: str,
    python_version: str | None = None,
    project_dir: str | Path = '.',
    template_dir: str | None = None,
) -> None:
    if not python_version:
        python_version = default_python_version()
    if not template_dir:
        template_dir = files('bluprint').joinpath('template')
    uv_init(python_version, str(template_dir), str(project_dir))
    delete_r_files_from_template(project_dir)
    replace_placeholder_name(
        Path(project_dir) / 'notebooks' / 'example_jupyternb.ipynb',
        project_name=project_name,
    )
    replace_git_account_name(project_dir)
    uv_add(['bluprint_conf', 'ipykernel', 'pandas'], project_dir)


def delete_r_files_from_template(project_dir: str | Path) -> None:
    (Path(project_dir) / 'placeholder_name.Rproj').unlink()
    (Path(project_dir) / 'notebooks' / 'example_rmarkdown.Rmd').unlink()


def replace_placeholder_name(
    notebook_path: str | Path,
    project_name: str,
    placeholder='placeholder_name',
) -> None:
    with open(notebook_path, 'r', encoding='utf-8') as in_notebook_file:
        notebook_content = nbformat.read(in_notebook_file, as_version=4)

    for cell in notebook_content['cells']:
        if 'source' in cell and isinstance(cell['source'], str):
            cell['source'] = cell['source'].replace(placeholder, project_name)

    with open(notebook_path, 'w', encoding='utf-8') as out_notebook_file:
        nbformat.write(notebook_content, out_notebook_file)


def replace_git_account_name(
    project_dir: str | Path,
) -> None:

    readme_file = Path(project_dir) / 'README.md'
    with open(readme_file, 'r') as readme_r:
        readme_content = readme_r.read()
    try:  # noqa: WPS229
        git_user = run(['git', 'config', '--global', 'user.name'], GitError)
        if git_user:
            readme_content = readme_content.replace(
                '{{git_account_name}}',
                git_user.strip(),
            )
    except GitError:
        # If there's no git, remove entire installation section
        readme_content = re.sub(
            re.compile(r'## Installation.*?(\n## |\Z)', re.DOTALL),
            '',
            readme_content,
        )

    with open(readme_file, 'w') as readme_w:
        readme_w.write(readme_content)


def default_python_version(min_version: str = MIN_PYTHON_VERSION) -> str:
    python_out = run(['python', '--version'], PythonVersionError)
    py_version = python_out.strip().replace('Python ', '')
    if Version(py_version) >= Version(min_version):
        return py_version
    return min_version


def check_python_version(
    python_version: str | None,
) -> None:
    if python_version:
        if Version(python_version) < Version(MIN_PYTHON_VERSION):
            raise LowPythonVersionError('Bluprint requires Python >= 3.11.')
