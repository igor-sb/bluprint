"""Create a bluprint project."""

from pathlib import Path

import nbformat
from importlib_resources import files

from bluprint.binary import pdm_add, pdm_init, run
from bluprint.create.errors import PythonVersionError


def create_project(
    project_name: str,
    python_version: str | None = None,
    parent_dir: str | None = None,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    project_dir.mkdir(parents=True)
    initialize_project(project_name, python_version, project_dir)


def initialize_project(
    project_name: str,
    python_version: str | None = None,
    project_dir: str | Path = '.',
) -> None:
    if not python_version:
        python_version = default_python_version()
    template_dir = files('bluprint').joinpath('template')
    pdm_init(python_version, str(template_dir), str(project_dir))
    (Path(project_dir) / '{{project}}.Rproj').unlink()
    replace_placeholder_name(
        Path(project_dir) / 'notebooks' / 'example_jupyternb.ipynb',
        project_name,
    )
    pdm_add(['bluprint_conf', 'ipykernel', 'pandas'], project_dir)


def replace_placeholder_name(
    notebook_path: str | Path,
    project_name: str,
    placeholder='{{project}}',
) -> None:
    with open(notebook_path, 'r', encoding='utf-8') as in_notebook_file:
        notebook_content = nbformat.read(in_notebook_file, as_version=4)

    for cell in notebook_content['cells']:
        if 'source' in cell and isinstance(cell['source'], str):
            cell['source'] = cell['source'].replace(placeholder, project_name)

    with open(notebook_path, 'w', encoding='utf-8') as out_notebook_file:
        nbformat.write(notebook_content, out_notebook_file)


def default_python_version() -> str:
    python_out = run(['python', '--version'], PythonVersionError)
    return python_out.strip().replace('Python ', '')
