"""Test data.yaml loading with file parsing."""

from pathlib import Path

from bluprint.config import (
    add_prefix_to_nested_config,
    load_config_yaml,
    load_data_yaml,
    load_data_yamls,
)


def test_add_prefix_to_nested_config():
    actual_test_config = load_config_yaml('tests/config/fixtures/test.yaml')
    actual_test_config = add_prefix_to_nested_config(
        actual_test_config,
        prefix='/xyz/',
    )
    expected_test_config = load_config_yaml(
        'tests/config/snapshots/prefixed_test.yaml',
    )
    assert dict(actual_test_config) == dict(expected_test_config)


def test_load_data_yaml():
    current_dir = Path.cwd()
    expected_data_cfg = {
        'test_data': {
            'absolute': '/a/3a.bin',
            'relative_with_subdir': f'{current_dir}/tests/fixtures/3b/3b2.csv',
            'relative_simple': f'{current_dir}/tests/fixtures/3c.jpeg',
            's3_uri': 's3://example-bucket/path/to/object',
        },
    }
    actual_data_cfg = load_data_yaml(
        'tests/config/fixtures/data.yaml',
        data_dir='tests/fixtures',
    )
    assert actual_data_cfg == expected_data_cfg


def test_load_data_yamls():
    current_dir = Path.cwd()
    expected_data_cfg = {
        'test_data': {
            'absolute': '/a/1a.bin',
            'relative_with_subdir': f'{current_dir}/tests/fixtures/1b/1b2.csv',
            'relative_simple': f'{current_dir}/tests/fixtures/1c.jpeg',
            's3_uri': 's3://example-bucket/path/to/object',
        },
        'test_data2': {
            'absolute': '/a/2a.bin',
            'relative_with_subdir': f'{current_dir}/tests/fixtures/2b/2b2',
            'relative_simple': f'{current_dir}/tests/fixtures/2c.jpeg',
            's3_uri': 's3://example-bucket/path/to/object',
        },
    }
    actual_data_cfg = load_data_yamls(
        'tests/config/fixtures/data_confs',
        data_dir='tests/fixtures',
    )
    assert actual_data_cfg == expected_data_cfg
