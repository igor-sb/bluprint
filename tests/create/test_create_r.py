"""Test creating a new Python project."""

import tempfile
from importlib import resources
from pathlib import Path

import pytest

import bluprint
from bluprint.create.errors import RenvInstallError, RpackageMissingError
from bluprint.create.r_project import (
    check_if_r_package_is_installed,
    run_renv_install,
)


def test_create_project(find_files_in_dir, monkeypatch):
    # When pytest runs, resources.files() references tests folder and not the
    # main package folder. This restores reference to the package folder.
    def mock_resources_files(arg):  # noqa: WPS430
        return (
            resources.files('demo').joinpath('').parent.parent / 'demo'
        )
    monkeypatch.setattr(bluprint.demo, 'dir_in_package', mock_resources_files)
    demo_dir = bluprint.demo.dir_in_package('demo')

    with tempfile.TemporaryDirectory() as temp_dir:
        bp = bluprint.cli.Bluprint()
        bp.create(
            project_name='project',
            python_version='3.11.2',
            parent_dir=temp_dir,
            r_proj=True,
        )
        project_files = {
            file_path.relative_to(Path(temp_dir) / 'project')
            for file_path in find_files_in_dir(Path(temp_dir) / 'project')
        }
        demo_files = {
            file_path.relative_to(demo_dir)
            for file_path in find_files_in_dir(demo_dir)
        }
        demo_files.update([
            Path('pyproject.toml'),
            Path('poetry.lock'),
            Path('renv.lock'),
            Path('.Rprofile'),
        ])
        assert project_files == demo_files
        assert (Path(temp_dir) / 'project' / '.venv').exists()
        assert (Path(temp_dir) / 'project' / 'renv').exists()


def test_check_if_r_package_is_not_installed():
    with pytest.raises(RpackageMissingError):
        check_if_r_package_is_installed('fake_package')


def test_run_renv_install_fail():
    with pytest.raises(RenvInstallError):
        run_renv_install('fake_package', '.')
