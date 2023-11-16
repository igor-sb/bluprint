import importlib
from pathlib import PosixPath
from omegaconf import DictConfig, OmegaConf


def add_prefix_to_nested_config(conf: DictConfig, prefix: str) -> None:
    for key, value in conf.items():
        if isinstance(value, DictConfig):
            add_prefix_to_nested_config(value, prefix)
        else:
            conf[key] = f'{prefix}{value}'


def load_data_yaml(config_file: str = 'data.yaml') -> DictConfig:
    conf_dir: PosixPath = importlib.resources.files('conf')
    conf = OmegaConf.load(str(conf_dir.joinpath(config_file)))
    data_dir = str(importlib.resources.files('data').joinpath(''))
    add_prefix_to_nested_config(conf, data_dir)
    return conf


def load_config_yaml(config_file: str = 'config.yaml') -> DictConfig:
    conf_dir: PosixPath = importlib.resources.files('conf')
    return OmegaConf.load(str(conf_dir.joinpath(config_file)))
