"""Code for interacting with YAML configuration files."""

import yaml
import importlib
from pathlib import PosixPath
from omegaconf import OmegaConf, DictConfig

def create_simple_config_yaml(contents: dict, file: str) -> None:
	yaml_contents = {
		'raw_table': 'data/raw/table1.csv',
		'transformed_table': 'data/transformed/table2.csv',
	}
	with open(file, 'w') as yaml_file:
		yaml.dump(contents, yaml_file, default_flow_style=False)


def load_config(config_file: str) -> DictConfig:
	absolute_path: PosixPath = importlib.resources.files('conf')
	return OmegaConf.load(absolute_path.joinpath(config_file))
