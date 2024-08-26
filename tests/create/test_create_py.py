"""Test creating a new Python project."""

from pathlib import Path

import pytest
from importlib_resources import files

from bluprint import cli
from bluprint.create.errors import LowPythonVersionError
from bluprint.template import default_template_dir, example_files


def test_create_py_project(find_files_in_dir, tmp_path):
    template_dir = default_template_dir()
    project_name = 'placeholder_name'
    cli.Bluprint().create(
        project_name=project_name,
        parent_dir=tmp_path,
    )
    project_dir = Path(tmp_path) / project_name
    project_files = {
        file_path.relative_to(project_dir)
        for file_path in find_files_in_dir(project_dir)
    }
    template_files = {
        file_path.relative_to(template_dir)
        for file_path in find_files_in_dir(template_dir)
    }
    template_files.update([
        Path('pyproject.toml'),
        Path('uv.lock'),
    ])
    template_files.remove(Path(f'{project_name}.Rproj'))  # Python-only test
    template_files.remove(Path('notebooks/example_rmarkdown.Rmd'))

    venv_dir = project_dir / '.venv'
    assert project_files == template_files
    assert (venv_dir / 'bin').exists()
    assert (venv_dir / 'lib').exists()
    assert (venv_dir / 'share').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()


def test_low_python_version():
    with pytest.raises(LowPythonVersionError):
        cli.check_python_version('3.10')


def test_create_py_project_without_examples(find_files_in_dir, tmp_path):
    template_dir = default_template_dir()
    project_name = 'placeholder_name'
    cli.Bluprint().create(
        project_name=project_name,
        parent_dir=tmp_path,
        add_examples=False,
    )
    project_dir = Path(tmp_path) / project_name
    project_files = {
        file_path.relative_to(project_dir)
        for file_path in find_files_in_dir(project_dir)
    }
    project_example_files = example_files(project_name)
    print(project_example_files)
    template_files = {
        file_path.relative_to(template_dir)
        for file_path in find_files_in_dir(template_dir)
        if file_path.relative_to(template_dir) not in project_example_files
    }
    template_files.update([
        Path('pyproject.toml'),
        Path('uv.lock'),
    ])

    template_files.remove(Path('placeholder_name.Rproj'))  # Python-only test

    venv_dir = project_dir / '.venv'
    assert project_files == template_files
    assert (venv_dir / 'bin').exists()
    assert (venv_dir / 'lib').exists()
    assert (venv_dir / 'share').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()
