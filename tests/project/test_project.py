"""Test project-related functions."""

import shutil
import tempfile
from pathlib import Path

import pytest

from bluprint.errors import ProjectExistsError
from bluprint.project import (
    check_if_project_dir_exists,
    check_if_project_files_exist,
    copy_template,
)

fixtures_path = Path('tests') / 'project' / 'fixtures'


def test_copy_template_without_overwrite():
    src_path = fixtures_path / 'example_src'
    dst_path_files = fixtures_path / 'example_dst'
    with tempfile.TemporaryDirectory() as dst_path:
        shutil.copytree(dst_path_files, dst_path, dirs_exist_ok=True)
        copy_template(src_path, dst_path, overwrite=False)
        example_dst_files = {
            str(Path(dst_path) / 'file1.txt'): 'contents_1',
            str(Path(dst_path) / 'files' / 'file2.txt'): 'contents2',
            str(Path(dst_path) / 'files' / 'file3.txt'): 'contents_3',
            str(Path(dst_path) / 'files' / 'file4.txt'): 'contents4',
        }
        for example_dst_file, true_contents in example_dst_files.items():
            with Path(example_dst_file).open() as example_dst_file_handle:
                assert example_dst_file_handle.read().strip() == true_contents


def test_copy_template_with_overwrite():
    src_path = fixtures_path / 'example_src'
    dst_path_files = fixtures_path / 'example_dst'
    with tempfile.TemporaryDirectory() as dst_path:
        shutil.copytree(dst_path_files, dst_path, dirs_exist_ok=True)
        copy_template(src_path, dst_path, overwrite=True)
        example_dst_files = {
            str(Path(dst_path) / 'file1.txt'): 'contents1',
            str(Path(dst_path) / 'files' / 'file2.txt'): 'contents2',
            str(Path(dst_path) / 'files' / 'file3.txt'): 'contents_3',
            str(Path(dst_path) / 'files' / 'file4.txt'): 'contents4',
        }
        for example_dst_file, true_contents in example_dst_files.items():
            with Path(example_dst_file).open() as example_dst_file_handle:
                assert example_dst_file_handle.read().strip() == true_contents


def test_check_if_project_dir_exists():
    with tempfile.TemporaryDirectory() as dst_path:
        Path.mkdir(Path(dst_path) / 'test_project')
        with pytest.raises(ProjectExistsError):
            check_if_project_dir_exists('test_project', dst_path)


def test_if_project_files_exist_pyproject_toml():
    with tempfile.TemporaryDirectory() as dst_path:
        Path.mkdir(Path(dst_path) / 'test_project')
        (Path(dst_path) / 'test_project' / 'pyproject.toml').write_text('')
        with pytest.raises(ProjectExistsError):
            check_if_project_files_exist('test_project', dst_path)


def test_if_project_files_exist_venv():
    with tempfile.TemporaryDirectory() as dst_path:
        Path.mkdir(Path(dst_path) / 'test_project' / '.venv', parents=True)
        with pytest.raises(ProjectExistsError):
            check_if_project_files_exist('test_project', dst_path)


def test_if_project_files_exist_readme_md():
    with tempfile.TemporaryDirectory() as dst_path:
        Path.mkdir(Path(dst_path) / 'test_project')
        (Path(dst_path) / 'test_project' / 'README.md').write_text('')
        with pytest.raises(ProjectExistsError):
            check_if_project_files_exist('test_project', dst_path)


def test_if_project_files_exist_pyproject_toml_overwrite():
    with tempfile.TemporaryDirectory() as dst_path:
        Path.mkdir(Path(dst_path) / 'test_project')
        (Path(dst_path) / 'test_project' / 'pyproject.toml').write_text('')
        with pytest.raises(ProjectExistsError):
            check_if_project_files_exist(
                project_name='test_project',
                project_dir=Path(dst_path) / 'test_project',
                overwrite=True,
            )


def test_if_project_files_exist_readme_md_overwrite():
    with tempfile.TemporaryDirectory() as dst_path:
        Path.mkdir(Path(dst_path) / 'test_project')
        (Path(dst_path) / 'test_project' / 'README.md').write_text('')
        assert \
            check_if_project_files_exist(
                project_name='test_project',
                project_dir=Path(dst_path) / 'test_project',
                overwrite=True,
            ) == 'overwrite'
