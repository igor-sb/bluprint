"""Test directory indexing and YAML output."""

import tempfile
from pathlib import Path

from bluprint import cli


def test_index_dir_to_config_yaml(snapshot):
    test_data_dir = Path('tests') / 'index' / 'fixtures'
    expected_yaml = 'data.yaml'
    with tempfile.NamedTemporaryFile('r+') as actual_yaml:
        cli.Bluprint().index(
            input_dir=test_data_dir,
            output_yaml=actual_yaml.name,
        )
        snapshot.snapshot_dir = Path('tests') / 'index' / 'snapshots'
        snapshot.assert_match(
            actual_yaml.read(),
            expected_yaml,
        )
