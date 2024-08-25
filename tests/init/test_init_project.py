"""Test creating a new Python project."""

from pathlib import Path

from importlib_resources import files

from bluprint import cli
from bluprint.template import default_template_dir


def test_init_py_project(find_files_in_dir, tmp_path):
    template_dir = default_template_dir()
    project_name = 'placeholder_name'
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
        file_path.relative_to(template_dir)
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
    assert (venv_dir / 'share').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()


def test_init_pyr_project(find_files_in_dir, tmp_path):
    template_dir = default_template_dir()
    project_name = 'placeholder_name'
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
        file_path.relative_to(template_dir)
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
