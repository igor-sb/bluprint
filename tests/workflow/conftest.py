"""Test fixtures."""

from pathlib import Path

import pytest

snapshot_path = Path('tests').absolute() / 'workflow' / 'snapshots'


@pytest.fixture()
def reference_test_log_file():
    return str(snapshot_path / 'test.log')


@pytest.fixture()
def reference_xtest_log_file():
    return str(snapshot_path / 'xtest.log')


@pytest.fixture()
def reference_rtest_log_file():
    return str(snapshot_path / 'rtest.log')
