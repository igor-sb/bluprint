"""Placeholder file contents for new projects."""

import shutil
import sys
from importlib import resources
from pathlib import Path, PosixPath


def create_demo_readme_md(
    project_name: str,
    project_dir: str | PosixPath,
    readme_md: str = 'README.md',
) -> None:
    sys.stderr.write('Creating readme:')
    with open(Path(project_dir) / readme_md, 'w') as readme:
        readme.write(f'# {project_name}\nEnter project description.')
    sys.stderr.write(' ✓\n')


def copy_demo_files(
    project_name: str,
    project_dir: str | Path | PosixPath,
) -> None:
    demo_path = str(resources.files('demo').joinpath(''))
    sys.stderr.write('Copying demo generic files:')
    shutil.copytree(
        src=Path(demo_path),
        dst=project_dir,
        ignore=shutil.ignore_patterns('project'),
        dirs_exist_ok=True,
    )
    sys.stderr.write(' ✓\n')
    sys.stderr.write('Copying demo project files:')
    shutil.copytree(
        src=Path(demo_path) / 'project',
        dst=Path(project_dir) / project_name,
        dirs_exist_ok=True,
    )
    sys.stderr.write(' ✓\n')
