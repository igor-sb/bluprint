"""Test creating a new project."""

from bluprint.project import create_project
import tempfile


def test_create_project():
    with tempfile.TemporaryDirectory() as tmp_dir:
        pass