"""Tests for installing demo files."""

import tempfile
from filecmp import DEFAULT_IGNORES, dircmp
from importlib import resources
from pathlib import Path

import bluprint
from bluprint.demo import copy_demo_files


def test_copy_demo_files(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = Path(temp_dir) / 'project'

        def mock_resources_files(*args):  # noqa: WPS430
            return (
                resources.files('demo').joinpath('').parent.parent / 'demo'
            )
        monkeypatch.setattr(
            bluprint.demo,
            'dir_in_package',
            mock_resources_files,
        )
        demo_path = bluprint.demo.dir_in_package('demo')
        copy_demo_files('project', project_path)
        dir_comp = dircmp(
            project_path,
            demo_path,
            ignore=[*DEFAULT_IGNORES, 'project.Rproj'],
        )
        assert dir_comp.common == dir_comp.left_list == dir_comp.right_list
