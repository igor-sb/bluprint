"""Test YAML manipulation."""

import importlib

from bluprint.config import add_prefix_to_nested_config, load_data_yaml


def test_add_prefix_to_nested_values():
    nested_dict = {
        'first_dict': {
            'second_val': 'a',
        },
        'first_val': 'b',
    }
    true_nested_dict_with_prefix = {
        'first_dict': {
            'second_val': '/prefix/a',
        },
        'first_val': '/prefix/b',
    }
    nested_dict_with_prefix = add_prefix_to_nested_config(
        nested_dict,
        '/prefix/',
    )
    assert nested_dict_with_prefix, true_nested_dict_with_prefix


def test_load_config():
    prefix = str(importlib.resources.files('tests').joinpath('') / 'test.yaml')
    true_yaml = {
        'groups': {
            'g1': {
                'opt11': f'{prefix}1',
                'opt12': f'{prefix}a',
            },
            'opt2': f'{prefix}b',
        },
    }
    loaded_yaml = load_data_yaml(
        'test.yaml',
        data_dir='tests',
        config_dir='tests',
    )
    assert loaded_yaml, true_yaml
