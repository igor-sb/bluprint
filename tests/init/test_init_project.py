"""Test creating a new Python project."""

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
