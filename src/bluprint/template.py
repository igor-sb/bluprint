"""Placeholder file contents for new projects."""

import shutil
from pathlib import Path

from importlib_resources import files

from bluprint.colors import progress_log, styled_print


def default_template_dir() -> str:
    template_dir = str(files('bluprint') / 'template')
    styled_print(f'using template: {template_dir}')
    return template_dir


@progress_log('copying R project template files')
def copy_rproj_files(
    project_name: str,
    project_dir: str | Path,
    template_dir: str | None = None,
    add_examples: bool = True,
) -> None:
    if not template_dir:
        template_dir = default_template_dir()
    shutil.copyfile(
        src=Path(template_dir) / 'placeholder_name.Rproj',
        dst=Path(project_dir) / f'{project_name}.Rproj',
    )
    if add_examples:
        shutil.copyfile(
            src=Path(template_dir) / 'notebooks' / 'example_rmarkdown.Rmd',
            dst=Path(project_dir) / 'notebooks' / 'example_rmarkdown.Rmd',
        )
