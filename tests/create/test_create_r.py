"""Test creating a new Python project."""

import tempfile
from importlib import resources
from pathlib import Path

import pytest

from bluprint import cli, demo
from bluprint.create.errors import RpackageMissingError
from bluprint.create.r_project import check_if_r_package_is_installed


def test_create_pyr_project(find_files_in_dir, monkeypatch):  # noqa: 210
    # When pytest runs, resources.files() references tests folder and not the
    # main package folder. This restores reference to the package folder.
    def mock_resources_files(arg):  # noqa: WPS430
        return (
            resources.files('demo').joinpath('').parent.parent / 'demo'
        )
    monkeypatch.setattr(demo, 'dir_in_package', mock_resources_files)
    demo_dir = demo.dir_in_package('demo')

    with tempfile.TemporaryDirectory() as temp_dir:
        bp = cli.Bluprint()
        bp.create(
            project_name='project',
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
        venv_dir = Path(temp_dir) / 'project' / '.venv'
        assert project_files == demo_files
        assert (Path(temp_dir) / 'project' / 'renv').exists()
        assert (venv_dir / 'pyvenv.cfg').exists()


def test_check_if_r_package_is_not_installed():
    with pytest.raises(RpackageMissingError):
        check_if_r_package_is_installed('fake_package')
