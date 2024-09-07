"""Test multiple YAML loading."""

from pathlib import Path

from bluprint.config import load_config_yaml, load_config_yamls


def test_load_configs():
    actual_config = load_config_yamls('tests/config/fixtures/confs')
    expected_config = load_config_yaml(
        'tests/config/snapshots/first_and_second.yaml',
    )
    assert actual_config == expected_config


def test_absolute_load_configs():
    abs_cfg_path = Path.cwd() / 'tests' / 'config' / 'fixtures' / 'confs'
    actual_config = load_config_yamls(abs_cfg_path)
    expected_config = load_config_yaml(
        'tests/config/snapshots/first_and_second.yaml',
    )
    assert actual_config == expected_config
