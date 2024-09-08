"""Test creating a new Python project."""

import tempfile
import tomllib
from pathlib import Path

import pytest

from bluprint import cli
from bluprint.create.errors import LowPythonVersionError
from bluprint.errors import InvalidProjectNameError
from bluprint.template import Placeholder, default_template_dir, example_files


def test_create_py_project(find_files_in_dir, tmp_path):
    template_dir = default_template_dir()
    project_name = 'test_project'
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
        Path(
            str(file_path.relative_to(template_dir))
            .replace(Placeholder.project_name, project_name)
        )
        for file_path in find_files_in_dir(template_dir)
    }
    template_files.update([
        Path('pyproject.toml'),
        Path('uv.lock'),
    ])
    template_files.remove(Path(f'{project_name}.Rproj'))
    template_files.remove(Path('notebooks/example_rmarkdown.Rmd'))

    venv_dir = project_dir / '.venv'
    assert project_files == template_files
    assert (venv_dir / 'bin').exists()
    assert (venv_dir / 'lib').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()


def test_low_python_version():
    with pytest.raises(LowPythonVersionError):
        cli.check_python_version('3.10')


def test_create_py_project_without_examples(find_files_in_dir, tmp_path):
    template_dir = default_template_dir()
    project_name = 'test_project'
    cli.Bluprint().create(
        project_name=project_name,
        parent_dir=tmp_path,
        omit_examples=True,
    )
    project_dir = Path(tmp_path) / project_name
    project_files = {
        file_path.relative_to(project_dir)
        for file_path in find_files_in_dir(project_dir)
    }
    project_example_files = example_files(project_name)
    template_files = {
        Path(
            str(file_path.relative_to(template_dir))
            .replace(Placeholder.project_name, project_name)
        )
        for file_path in find_files_in_dir(template_dir)
        if file_path.relative_to(template_dir) not in project_example_files
    }
    template_files.update([
        Path('pyproject.toml'),
        Path('uv.lock'),
    ])

    template_files.remove(Path(f'{project_name}.Rproj'))  # Python-only test

    venv_dir = project_dir / '.venv'
    assert project_files == template_files
    assert (venv_dir / 'bin').exists()
    assert (venv_dir / 'lib').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()


def test_create_py_project_custom_template(find_files_in_dir, tmp_path):
    project_name = 'placeholder_name'
    with tempfile.TemporaryDirectory() as template_dir:
        # Create a custom template
        (Path(template_dir) / 'conf').mkdir()
        (Path(template_dir) / 'conf' / 'myconf.yaml').write_text('')
        (Path(template_dir) / 'readme.md').write_text('read me!')
        (Path(template_dir) / 'placeholder_name').mkdir()
        (Path(template_dir) / 'placeholder_name' / 'test.py').write_text(
            'print("hello!")',
        )
        # Create a bluprint project with this template
        cli.Bluprint().create(
            project_name=project_name,
            parent_dir=tmp_path,
            template_dir=template_dir,
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
        venv_dir = project_dir / '.venv'
        # Check that all filenames match
        assert project_files == template_files
        # Check that venv is correctly created
        assert (venv_dir / 'bin').exists()
        assert (venv_dir / 'lib').exists()
        assert (venv_dir / 'pyvenv.cfg').exists()
        # Check file contents
        assert (project_dir / 'readme.md').read_text().strip() == 'read me!'
        assert (project_dir / 'placeholder_name' / 'test.py').read_text() \
            == 'print("hello!")'
        assert (project_dir / 'pyproject.toml').exists()


def test_create_py_project_with_invalid_names(tmp_path):
    project_names = ('invalid-name', '0', 'invalid_', '_invalid')
    for project_name in project_names:
        with pytest.raises(InvalidProjectNameError):
            cli.Bluprint().create(
                project_name=project_name,
                parent_dir=tmp_path,
            )


def test_create_py_project_mixed_case(tmp_path):
    project_name = 'aAa'
    cli.Bluprint().create(
        project_name=project_name,
        parent_dir=tmp_path,
    )
    project_dir = Path(tmp_path) / project_name
    with (project_dir / 'pyproject.toml').open('rb') as pyproject_toml_file:
        pyproject_toml = tomllib.load(pyproject_toml_file)
    assert (project_dir / 'aaa').exists()
    assert pyproject_toml['project']['name'] == 'aaa'


def test_create_py_project_specific_python(tmp_path):
    python_version = '3.11.2'
    project_name = 'py3_11_2'
    project_dir = Path(tmp_path) / project_name
    cli.Bluprint().create(
        project_name=project_name,
        parent_dir=tmp_path,
        python_version=python_version,
    )
    with (project_dir / 'pyproject.toml').open('rb') as pyproject_toml_file:
        pyproject_toml = tomllib.load(pyproject_toml_file)
    assert pyproject_toml['project']['requires-python'] == f'=={python_version}'


def test_create_py_project_specific_python_string(tmp_path):
    python_version = '==3.11.2'
    project_name = 'pyeq3_11_2'
    project_dir = Path(tmp_path) / project_name
    cli.Bluprint().create(
        project_name=project_name,
        parent_dir=tmp_path,
        python_version=python_version,
    )
    with (project_dir / 'pyproject.toml').open('rb') as pyproject_toml_file:
        pyproject_toml = tomllib.load(pyproject_toml_file)
    assert pyproject_toml['project']['requires-python'] == python_version
