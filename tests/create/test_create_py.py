"""Test creating a new Python project."""

import tempfile
from importlib import resources
from pathlib import Path

from bluprint import cli, demo


def test_create_py_project(find_files_in_dir, monkeypatch):  # noqa: WPS210
    # When pytest runs, resources.files() references tests folder and not the
    # main package folder. This restores reference to the package folder.
    def mock_resources_files(arg):  # noqa: WPS430
        return (
            resources.files('demo').joinpath('').parent.parent / 'demo'
        )
    monkeypatch.setattr(demo, 'dir_in_package', mock_resources_files)
    demo_dir = demo.dir_in_package('demo')

    with tempfile.TemporaryDirectory() as temp_dir:
        cli.Bluprint().create(
            project_name='project',
            parent_dir=temp_dir,
        )
        project_dir = Path(temp_dir) / 'project'
        project_files = {
            file_path.relative_to(project_dir)
            for file_path in find_files_in_dir(project_dir)
        }
        demo_files = {
            file_path.relative_to(demo_dir)
            for file_path in find_files_in_dir(demo_dir)
        }
        demo_files.update([
            Path('pyproject.toml'),
            Path('poetry.lock'),
            Path('.python-version'),
        ])
        demo_files.remove(Path('project.Rproj'))  # Python-only test
        venv_dir = project_dir / '.venv'
        assert project_files == demo_files
        assert (venv_dir / 'bin').exists()
        assert (venv_dir / 'lib').exists()
        assert (venv_dir / 'share').exists()
        assert (venv_dir / 'pyvenv.cfg').exists()
