"""Test creating a new Python project."""

import tempfile
from importlib import resources
from pathlib import Path

import bluprint


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
        bluprint.cli.Bluprint().create(
            project_name='project',
            python_version='3.11.2',
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
        assert project_files == demo_files
        assert (project_dir / '.venv' / 'bin').exists()
        assert (project_dir / '.venv' / 'lib').exists()
        assert (project_dir / '.venv' / 'share').exists()
        assert (project_dir / '.venv' / 'pyvenv.cfg').exists()
