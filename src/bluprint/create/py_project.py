"""Create a bluprint project."""

from importlib import resources
from pathlib import Path

import nbformat

from bluprint.binary import pdm, run
from bluprint.create.errors import (
    PdmAddError,
    PdmInitError,
    PythonVersionError,
)


def create_project(
    project_name: str,
    python_version: str | None = None,
    parent_dir: str | None = None,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    if not python_version:
        python_version = default_python_version()
    project_dir.mkdir(parents=True)
    template_dir = resources.files('demo').joinpath('')
    pdm(
        ['init', '-n', '--python', python_version, template_dir],
        PdmInitError,
        cwd=project_dir,
    )
    (project_dir / 'project.Rproj').unlink()
    replace_placeholder_name(
        project_dir / 'notebooks' / 'example_jupyternb.ipynb',
        project_name,
    )
    pdm(['add', 'ipykernel', 'pandas'], PdmAddError, cwd=project_dir)


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
