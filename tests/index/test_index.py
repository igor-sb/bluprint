"""Test directory indexing and YAML output."""

import tempfile
from pathlib import Path

from bluprint.index import index_dir_to_config_yaml


def test_index_dir_to_config_yaml(snapshot):
    test_data_dir = Path('tests') / 'index' / 'fixtures'
    expected_yaml = 'data.yaml'
    with tempfile.NamedTemporaryFile('r+') as actual_yaml:
        index_dir_to_config_yaml(test_data_dir, actual_yaml.name)
        snapshot.snapshot_dir = Path('tests') / 'index' / 'snapshots'
        snapshot.assert_match(
            actual_yaml.read(),
            expected_yaml,
        )
