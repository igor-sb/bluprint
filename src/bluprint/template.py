"""Placeholder file contents for new projects."""

import shutil
from pathlib import Path

from importlib_resources import files


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
