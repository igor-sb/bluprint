"""Functions for modifying project template during project creation."""

import re
from pathlib import Path

import nbformat
from importlib_resources import files

from bluprint.binary import run
from bluprint.colors import styled_print
from bluprint.create.errors import GitError


def example_files(project_name: str) -> tuple[Path, ...]:
    return (
        Path('notebooks') / 'example_jupyternb.ipynb',
        Path('notebooks') / 'example_quarto.qmd',
        Path('notebooks') / 'example_rmarkdown.Rmd',
        Path('data') / 'example_data.csv',
        Path('conf') / 'config.yaml',
        Path('conf') / 'workflows.yaml',
        Path(project_name) / 'example.py',
    )


def delete_examples_from_project(
    project_name: str,
    project_dir: str | Path,
) -> None:
    for example_file in example_files(project_name):
        full_example_file = Path(project_dir) / example_file
        if full_example_file.exists():
            full_example_file.unlink()
    open(Path(project_dir) / 'conf' / 'data.yaml', 'w').close()


def delete_r_examples_from_project(
    project_dir: str | Path,
) -> None:
    (Path(project_dir) / 'notebooks' / 'example_rmarkdown.Rmd').unlink()


def delete_r_files_from_project(project_dir: str | Path) -> None:
    (Path(project_dir) / 'placeholder_name.Rproj').unlink()
    (Path(project_dir) / 'notebooks' / 'example_rmarkdown.Rmd').unlink()


def replace_placeholder_name_in_file(
    filename: str | Path,
    project_name: str,
    placeholder='{{placeholder_name}}',
) -> None:
    file_lines = []
    with open(filename, 'r') as in_file:
        for line in in_file:
            file_lines.append(line.replace(placeholder, project_name))
    with open(filename, 'w') as out_file:
        for line in file_lines:
            out_file.write(line)


def replace_placeholder_name_in_notebook(
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
    try:
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


def default_template_dir() -> str:
    template_dir = str(files('bluprint') / 'template')
    styled_print(f'using template: {template_dir}')
    return template_dir
