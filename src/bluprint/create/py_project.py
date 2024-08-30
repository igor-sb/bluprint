"""Create a bluprint project."""

from pathlib import Path

from packaging.version import Version

from bluprint.binary import run, uv_add, uv_init
from bluprint.colors import progress_log
from bluprint.create.errors import LowPythonVersionError, PythonVersionError
from bluprint.project import copy_template
from bluprint.template import (
    default_template_dir,
    replace_git_account_name,
    replace_placeholder_name_in_file,
    replace_placeholder_name_in_notebook,
)

MIN_PYTHON_VERSION = '3.11'


def create_python_project(
    project_name: str,
    python_version: str | None = None,
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
        project_name=project_name,
        python_version=python_version,
        project_dir=project_dir,
        template_dir=template_dir,
        keep_r_files=keep_r_files,
        omit_examples=omit_examples,
    )


@progress_log('initializing Python project', print_ok=False)
def initialize_python_project(
    project_name: str,
    python_version: str | None = None,
    project_dir: str | Path = '.',
    template_dir: str | None = None,
    keep_r_files: bool = False,
    omit_examples: bool = False,
    overwrite: bool = False,
) -> None:
    if not python_version:
        python_version = default_python_version()
    if not template_dir:
        template_dir = default_template_dir()
    uv_init(python_version, str(project_dir))
    (Path(project_dir) / 'src' / project_name / '__init__.py').unlink()
    Path.rmdir(Path(project_dir) / 'src' / project_name)
    Path.rmdir(Path(project_dir) / 'src')
    copy_template(
        template_dir,
        project_dir,
        project_name=project_name,
        omit_examples=omit_examples,
        keep_r_files=keep_r_files,
        overwrite=overwrite,
    )
    Path.rename(
        Path(project_dir) / 'placeholder_name',
        Path(project_dir) / project_name,
    )
    replace_placeholder_name_in_file(
        Path(project_dir) / 'pyproject.toml',
        project_name,
    )
    if not omit_examples:
        replace_placeholder_name_in_file(
            Path(project_dir) / 'README.md',
            project_name,
        )
        replace_placeholder_name_in_file(
            Path(project_dir) / 'notebooks' / 'example_quarto.qmd',
            project_name,
        )
        replace_placeholder_name_in_notebook(
            Path(project_dir) / 'notebooks' / 'example_jupyternb.ipynb',
            project_name,
        )
        replace_git_account_name(project_dir)
    uv_add(['bluprint_conf', 'ipykernel', 'pandas'], project_dir)


def default_python_version(min_version: str = MIN_PYTHON_VERSION) -> str:
    python_out = run(['python', '--version'], PythonVersionError)
    py_version = python_out.strip().replace('Python ', '')
    if Version(py_version) >= Version(min_version):
        return py_version
    return min_version


@progress_log('checking Python version...')
def check_python_version(
    python_version: str | None,
) -> None:
    if (
        python_version and
        (Version(python_version) < Version(MIN_PYTHON_VERSION))
    ):
        raise LowPythonVersionError('Bluprint requires Python >= 3.11.')
