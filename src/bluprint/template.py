"""Placeholder file contents for new projects."""

import shutil
from pathlib import Path

from importlib_resources import files


def copy_template_files(
    project_name: str,
    project_dir: str | Path,
) -> None:
    template_path = files('bluprint').joinpath('template')
    shutil.copytree(
        src=Path(template_path),
        dst=project_dir,
        ignore=shutil.ignore_patterns('project', '*.html', '*.Rproj'),
        dirs_exist_ok=True,
    )
    shutil.copytree(
        src=Path(template_path) / 'project',
        dst=Path(project_dir) / project_name,
        dirs_exist_ok=True,
    )


def copy_rproj_files(
    project_name: str,
    project_dir: str | Path,
) -> None:
    template_path = files('bluprint').joinpath('template')
    shutil.copyfile(
        src=Path(template_path) / 'placeholder_name.Rproj',
        dst=Path(project_dir) / f'{project_name}.Rproj',
    )
    shutil.copyfile(
        src=Path(template_path) / 'notebooks' / 'example_rmarkdown.Rmd',
        dst=Path(project_dir) / 'notebooks' / 'example_rmarkdown.Rmd',
    )
