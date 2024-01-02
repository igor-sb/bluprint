"""Test creating a new Python project."""

from pathlib import Path
from importlib_resources import files
from bluprint import cli


def test_create_py_project(find_files_in_dir, tmp_path):
    template_dir = files('bluprint').joinpath('template')
    cli.Bluprint().create(
        project_name='placeholder_name',
        parent_dir=tmp_path,
    )
    project_dir = Path(tmp_path) / 'placeholder_name'
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
    template_files.remove(Path('placeholder_name.Rproj'))  # Python-only test
    template_files.remove(Path('notebooks/example_rmarkdown.Rmd'))

    venv_dir = project_dir / '.venv'
    assert project_files == template_files
    assert (venv_dir / 'bin').exists()
    assert (venv_dir / 'lib').exists()
    assert (venv_dir / 'share').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()
