"""Test creating a new Python project."""

from pathlib import Path

from bluprint import cli, demo


def test_create_py_project(find_files_in_dir, tmp_path):
    demo_dir = demo.dir_in_package('demo')
    cli.Bluprint().create(
        project_name='project',
        parent_dir=tmp_path,
    )
    project_dir = Path(tmp_path) / 'project'
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
        Path('pdm.lock'),
    ])
    demo_files.remove(Path('project.Rproj'))  # Python-only test
    venv_dir = project_dir / '.venv'
    assert project_files == demo_files
    assert (venv_dir / 'bin').exists()
    assert (venv_dir / 'lib').exists()
    assert (venv_dir / 'share').exists()
    assert (venv_dir / 'pyvenv.cfg').exists()
