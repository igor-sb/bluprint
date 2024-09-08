"""Test creating a new Python project."""

import tempfile
import textwrap
import tomllib
from pathlib import Path

import pytest

from bluprint import cli
from bluprint.errors import ProjectExistsError
from bluprint.template import Placeholder, default_template_dir, example_files


def test_init_py_project(find_files_in_dir, tmp_path):
    template_dir = default_template_dir()
    project_name = 'test_project'
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    cli.Bluprint().init(
        project_name=project_name,
        project_dir=project_dir,
    )
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
    template_files.remove(Path(f'{project_name}.Rproj'))  # Python-only test
    template_files.remove(Path('notebooks/example_rmarkdown.Rmd'))
    venv_dir = project_dir / '.venv'
    assert project_files == template_files
    assert (venv_dir / 'bin').exists()
    assert (venv_dir / 'lib').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()


def test_init_pyr_project(find_files_in_dir, tmp_path):
    template_dir = default_template_dir()
    project_name = 'test_project'
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    cli.Bluprint().init(
        project_name=project_name,
        project_dir=project_dir,
        r_project=True,
    )
    project_files = {
        file_path.relative_to(tmp_path / project_name)
        for file_path in find_files_in_dir(tmp_path / project_name)
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
        Path('renv.lock'),
        Path('.Rprofile'),
    ])
    venv_dir = tmp_path / project_name / '.venv'
    assert project_files == template_files
    assert (tmp_path / project_name / 'renv').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()


def test_init_existing_with_pyproject_toml(tmp_path):
    project_name = 'placeholder_name'
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    (project_dir / 'pyproject.toml').open('w').close()
    with pytest.raises(ProjectExistsError):
        cli.Bluprint().init(
            project_name=project_name,
            project_dir=project_dir,
            overwrite=True,
        )


def test_init_existing_without_examples_with_yamls(find_files_in_dir, tmp_path):
    project_name = 'test_project'
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    (project_dir / 'data').mkdir()
    (project_dir / 'conf').mkdir()
    with (project_dir / 'conf' / 'data.yaml').open('w') as data_yaml:
        data_yaml.write('mydata: "mydata.csv"')
    with (project_dir / 'conf' / 'conf.yaml').open('w') as conf_yaml:
        conf_yaml.write('mykey: "myval"')
    cli.Bluprint().init(
        project_name=project_name,
        project_dir=project_dir,
        omit_examples=True,
        overwrite=True,
    )
    template_dir = default_template_dir()
    project_example_files = example_files(project_name)
    template_files = {
        Path(
            str(file_path.relative_to(template_dir))
            .replace(Placeholder.project_name, project_name)
        )
        for file_path in find_files_in_dir(template_dir)
        if file_path.relative_to(template_dir) not in project_example_files
    }
    template_files.remove(Path(f'{project_name}.Rproj'))  # Python-only test
    template_files.update([
        Path('conf') / 'conf.yaml',
        Path('pyproject.toml'),
        Path('uv.lock'),
    ])
    project_files = {
        file_path.relative_to(tmp_path / project_name)
        for file_path in find_files_in_dir(tmp_path / project_name)
    }
    assert project_files == template_files
    with (project_dir / 'conf' / 'data.yaml').open() as data_yaml:
        assert data_yaml.read().strip() == "example: 'example_data.csv'"
    with (project_dir / 'conf' / 'conf.yaml').open() as conf_yaml:
        assert conf_yaml.read().strip() == 'mykey: "myval"'


def test_init_py_project_mixed_case(tmp_path):
    project_name = 'aAa'
    project_dir = Path(tmp_path) / project_name
    project_dir.mkdir()
    cli.Bluprint().init(
        project_name=project_name,
        project_dir=project_dir,
    )
    with (project_dir / 'pyproject.toml').open('rb') as pyproject_toml_file:
        pyproject_toml = tomllib.load(pyproject_toml_file)
    assert (project_dir / 'aaa').exists()
    assert pyproject_toml['project']['name'] == 'aaa'


def test_init_py_project_template_wo_pyproject_toml(
    find_files_in_dir,
    tmp_path,
):
    project_name = 'init_from_template'
    python_version = '3.11.9'
    project_dir = Path(tmp_path) / project_name
    project_dir.mkdir()
    with tempfile.TemporaryDirectory() as template_dir:
        (Path(template_dir) / 'conf').mkdir()
        (Path(template_dir) / 'conf' / 'myconf.yaml').write_text('')
        (Path(template_dir) / 'readme.md').write_text('read me!')
        (Path(template_dir) / Placeholder.project_name).mkdir()
        (Path(template_dir) / Placeholder.project_name / 'test.py').write_text(
            'print("hello!")',
        )
        pyproject_toml_temp = textwrap.dedent(f"""
            [project]
            name = "{Placeholder.project_name}"
            version = "0.1.0"
            description = "Add your description here"
            requires-python = "=={python_version}"
            dependencies = []

            [build-system]
            requires = ["hatchling"]
            build-backend = "hatchling.build"
        """).strip()
        (Path(template_dir) / 'pyproject.toml').write_text(pyproject_toml_temp)
        cli.Bluprint().init(
            project_name=project_name,
            project_dir=project_dir,
            template_dir=template_dir,
            python_version=python_version,
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
        template_files.update([Path('uv.lock')])
        template_files_with_replaced_placeholder = {
            Path(
                str(template_file)
                .replace(Placeholder.project_name, project_name)
            )
            for template_file in template_files
        }

        assert project_files == template_files_with_replaced_placeholder
        # Check that venv is correctly created
        assert (project_dir / '.venv' / 'bin').exists()
        assert (project_dir / '.venv' / 'lib').exists()
        assert (project_dir / '.venv' / 'pyvenv.cfg').exists()
        # Check file contents
        assert (project_dir / 'readme.md').read_text().strip() == 'read me!'
        assert (project_dir / project_name / 'test.py').read_text() \
            == 'print("hello!")'
        assert (project_dir / 'pyproject.toml').exists()
        assert (project_dir / 'pyproject.toml').read_text().strip() == \
            pyproject_toml_temp.replace(
                Placeholder.project_name, project_name.replace('_', '-'),
            )
