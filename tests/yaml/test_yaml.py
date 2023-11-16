"""Test YAML manipulation."""

from bluprint.config import add_prefix_to_nested_config
from omegaconf import DictConfig, OmegaConf

def test_add_prefix_to_nested_values():
	nested_dict = {
		'first_dict': {
			'second_val': 'a',
		},
		'first_val': 'b',
	}
	add_prefix_to_nested_config(nested_dict, '/prefix/')
	assert nested_dict, {'first_dict': {'second_val': '/prefix/a'}, 'first_val': '/prefix/b'}


def test_load_config():
	