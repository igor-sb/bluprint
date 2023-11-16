import importlib
from pathlib import PosixPath
from omegaconf import DictConfig, OmegaConf


def add_prefix_to_nested_values(conf: DictConfig, prefix: str):
    for key, value in conf.items():
        if isinstance(value, DictConfig):
            add_prefix_to_nested_values(value, prefix)
        else:
            conf[key] = f'{prefix}{value}'


def load_data_yaml(config_file: str = 'data.yaml') -> DictConfig:
    conf_dir: PosixPath = importlib.resources.files('conf')
    conf = OmegaConf.load(str(conf_dir.joinpath(config_file)))
    add_prefix_to_nested_values(
        conf,
        str(importlib.resources.files('data').joinpath('')),
    )
    return conf


def load_config_yaml(config_file: str = 'config.yaml') -> DictConfig:
    conf_dir: PosixPath = importlib.resources.files('conf')
    return OmegaConf.load(str(conf_dir.joinpath(config_file)))
