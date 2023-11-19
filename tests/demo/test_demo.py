"""Tests for installing demo files."""

import importlib
import pathlib
import tempfile
from filecmp import dircmp

from bluprint.demo import copy_demo_files


def test_copy_demo_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = pathlib.Path(temp_dir) / 'project'
        demo_path = importlib.resources.files('demo').joinpath('')
        copy_demo_files(project_path, 'project')
        dir_comp = dircmp(project_path, demo_path)
        assert dir_comp.common == dir_comp.left_list == dir_comp.right_list
