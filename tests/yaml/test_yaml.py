"""Test YAML manipulation."""

from pathlib import Path

from bluprint.config import (
	add_prefix_to_nested_config,
	load_config_yaml,
)


def test_load_data_yaml():
    actual_test_config = load_config_yaml(
        'test.yaml',
        config_dir=Path('tests') / 'yaml' / 'fixtures',
    )
    actual_test_config = add_prefix_to_nested_config(
        actual_test_config,
        prefix='/xyz/',
    )
    expected_test_config = load_config_yaml(
        'prefixed_test.yaml',
        config_dir=Path('tests') / 'yaml' / 'snapshots',
    )
    assert dict(actual_test_config) == dict(expected_test_config)
