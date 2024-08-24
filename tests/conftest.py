"""Fixtures shared across entire test suite."""

import os
from pathlib import Path, PosixPath

import pytest


@pytest.fixture
def find_files_in_dir():
    def _find_files_in_dir(
        lookup_dir: str | PosixPath,
    ) -> set[PosixPath]:
        venv_renv_dirs = (
            str(Path(lookup_dir) / '.venv'),
            str(Path(lookup_dir) / 'renv'),
        )
        file_list = set()
        for root, _dirs, files in os.walk(lookup_dir):
            if not root.startswith(venv_renv_dirs):
                for file in files:
                    file_list.add(Path(root) / file)
        return file_list
    return _find_files_in_dir
