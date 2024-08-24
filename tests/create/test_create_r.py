"""Test creating a new Python project."""

from pathlib import Path

import pytest
from importlib_resources import files

from bluprint import cli
from bluprint.create.errors import RpackageMissingError
from bluprint.create.r_project import check_if_r_package_is_installed


def test_create_pyr_project(find_files_in_dir, tmp_path):
    template_dir = files('bluprint').joinpath('template')
    bp = cli.Bluprint()
    bp.create(
        project_name='placeholder_name',
        parent_dir=tmp_path,
        r_proj=True,
    )
    project_files = {
        file_path.relative_to(tmp_path / 'placeholder_name')
        for file_path in find_files_in_dir(tmp_path / 'placeholder_name')
    }
    template_files = {
        file_path.relative_to(template_dir)
        for file_path in find_files_in_dir(template_dir)
    }
    template_files.update([
        Path('pyproject.toml'),
        Path('uv.lock'),
        Path('renv.lock'),
        Path('.Rprofile'),
    ])
    venv_dir = tmp_path / 'placeholder_name' / '.venv'
    assert project_files == template_files
    assert (tmp_path / 'placeholder_name' / 'renv').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()


def test_check_if_r_package_is_not_installed():
    with pytest.raises(RpackageMissingError):
        check_if_r_package_is_installed('fake_package')
