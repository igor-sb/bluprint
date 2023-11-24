"""Test fixtures."""

from pathlib import Path

import pytest

snapshot_path = Path('tests').absolute() / 'workflow' / 'snapshots'


@pytest.fixture()
def reference_test_log_file():
    return str(snapshot_path / 'test.log')
