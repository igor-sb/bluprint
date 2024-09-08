"""Create a bluprint project."""

import re
from pathlib import Path

from packaging.version import Version

from bluprint.binary import run, uv_add, uv_init
from bluprint.colors import progress_log
from bluprint.create.errors import LowPythonVersionError, PythonVersionError
from bluprint.project import copy_template
from bluprint.template import (
    Placeholder,
    activate_data_conf_proj_dirs,
    default_template_dir,
    replace_git_account_name_in_readme,
    replace_placeholder_in_file,
)

MIN_PYTHON_VERSION = '3.11'


def create_python_project(
    project_name: str,
    python_version: str | float | None = None,
    parent_dir: str | None = None,
    template_dir: str | None = None,
    keep_r_files: bool = False,
    omit_examples: bool = False,
) -> None:
    if not parent_dir:
        parent_dir = '.'
    project_dir = Path(parent_dir) / project_name
    project_dir.mkdir(parents=True)
    initialize_python_project(
        project_name=project_name.lower(),
        python_version=python_version,
        project_dir=project_dir,
        template_dir=template_dir,
        keep_r_files=keep_r_files,
        omit_examples=omit_examples,
        overwrite=True,
    )


@progress_log('initializing Python project', print_ok=False)
def initialize_python_project(
    project_name: str,
    python_version: str | float | None = None,
    project_dir: str | Path = '.',
    template_dir: str | None = None,
    keep_r_files: bool = False,
    omit_examples: bool = False,
    overwrite: bool = False,
) -> None:
    python_versions = parse_or_get_default_python_version(python_version)
    if not template_dir:
        template_dir = default_template_dir()
    pkg_project_name = project_name.replace('-', '_').lower()
    uv_init(project_name, python_versions, str(project_dir))
    uv_init_cleanup(project_dir, pkg_project_name)
    copy_template(
        template_dir,
        project_dir,
        project_name=pkg_project_name,
        omit_examples=omit_examples,
        keep_r_files=keep_r_files,
        overwrite=overwrite,
    )
    replace_placeholders_in_dir(
        project_dir=project_dir,
        template_dir=template_dir,
        project_name=pkg_project_name,
        python_versions=python_versions,
        omit_examples=omit_examples,
    )
    uv_add(['bluprint'], project_dir)


def uv_init_cleanup(project_dir: str | Path, pkg_project_name: str) -> None:
    (Path(project_dir) / 'src' / pkg_project_name / '__init__.py').unlink()
    Path.rmdir(Path(project_dir) / 'src' / pkg_project_name)
    Path.rmdir(Path(project_dir) / 'src')


def replace_placeholders_in_dir(
    project_dir: str | Path,
    template_dir: str | Path,
    project_name: str,
    python_versions: str,
    omit_examples: bool,
) -> None:
    if (Path(project_dir) / Placeholder.project_name).exists():
        Path.rename(
            Path(project_dir) / Placeholder.project_name,
            Path(project_dir) / project_name,
        )
    if not (Path(template_dir) / 'pyproject.toml').exists():
        activate_data_conf_proj_dirs(Path(project_dir) / 'pyproject.toml')
    replace_placeholder_in_file(
        Path(project_dir) / 'pyproject.toml',
        placeholder=Placeholder.project_name,
        replacement=project_name,
    )
    replace_placeholder_in_file(
        Path(project_dir) / 'pyproject.toml',
        placeholder=Placeholder.python_version,
        replacement=python_versions,
    )
    if not omit_examples:
        readme_file = Path(project_dir) / 'README.md'
        example_files_with_placeholder = [
            readme_file,
            Path(project_dir) / 'notebooks' / 'example_jupyternb.ipynb',
            Path(project_dir) / 'notebooks' / 'example_quarto.qmd',
        ]
        for example_file in example_files_with_placeholder:
            if example_file.exists():
                replace_placeholder_in_file(
                    example_file,
                    placeholder=Placeholder.project_name,
                    replacement=project_name,
                )
        if readme_file.exists():
            replace_git_account_name_in_readme(readme_file)


def default_python_version(min_version: str = MIN_PYTHON_VERSION) -> str:
    python_out = run(['python', '--version'], PythonVersionError)
    py_version = python_out.strip().replace('Python ', '')
    if Version(py_version) >= Version(min_version):
        return py_version
    return min_version


@progress_log('checking Python version...')
def check_python_version(
    python_version: str | float,
) -> None:
    python_version = str(python_version)
    if (
        re.match(r'^[0-9]', python_version) and
        python_version and
        (Version(python_version) < Version(MIN_PYTHON_VERSION))
    ):
        raise LowPythonVersionError('Bluprint requires Python >= 3.11.')


def parse_or_get_default_python_version(
    python_version: str | float | None,
) -> str:
    if not python_version:
        python_version = default_python_version()
    else:
        python_version = str(python_version)
        if re.match('^[0-9]', python_version):
            python_version = f'=={python_version}'
    return python_version
