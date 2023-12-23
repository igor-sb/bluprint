"""Test creating a new Python project."""

from pathlib import Path
from importlib_resources import files
from bluprint import cli


def test_create_init_project(find_files_in_dir, tmp_path):
    template_dir = files('bluprint').joinpath('template')
    project_dir = tmp_path / '{{project}}'
    project_dir.mkdir()
    cli.Bluprint().init(
        project_name='{{project}}',
        project_dir=project_dir,
    )
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
        Path('pdm.lock'),
    ])
    template_files.remove(Path('{{project}}.Rproj'))  # Python-only test
    venv_dir = project_dir / '.venv'
    assert project_files == template_files
    assert (venv_dir / 'bin').exists()
    assert (venv_dir / 'lib').exists()
    assert (venv_dir / 'share').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()
