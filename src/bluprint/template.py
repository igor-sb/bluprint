"""Functions for modifying project template during project creation."""

import re
from pathlib import Path

from importlib_resources import files

from bluprint.binary import run
from bluprint.colors import styled_print
from bluprint.create.errors import GitError


def example_files(project_name: str = 'placeholder_name') -> tuple[Path, ...]:
    return (
        Path('notebooks') / 'example_jupyternb.ipynb',
        Path('notebooks') / 'example_quarto.qmd',
        Path('notebooks') / 'example_rmarkdown.Rmd',
        Path('data') / 'example_data.csv',
        Path('conf') / 'config.yaml',
        Path('conf') / 'workflows.yaml',
        Path(project_name) / 'example.py',
        Path('README.md'),
    )


def r_files() -> tuple[Path, ...]:
    return (
        Path('placeholder_name.Rproj'),
        Path('notebooks') / 'example_rmarkdown.Rmd',
    )


def replace_placeholder_name_in_file(
    filename: str | Path,
    project_name: str,
    placeholder='{{placeholder_name}}',
) -> None:
    file_lines = []
    with Path(filename).open('r') as in_file:
        for line in in_file:
            file_lines.append(line.replace(placeholder, project_name))
    with Path(filename).open('w') as out_file:
        for line in file_lines:
            out_file.write(line)


def replace_git_account_name_in_readme(readme_file: str | Path) -> None:
    with readme_file.open('r') as readme_r:
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

    with readme_file.open('w') as readme_w:
        readme_w.write(readme_content)


def default_template_dir() -> str:
    template_dir = str(files('bluprint') / 'template')
    styled_print(f'using template: {template_dir}')
    return template_dir
