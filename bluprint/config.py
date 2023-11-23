"""Code for manipulating YAML configuration files."""

import importlib
from copy import deepcopy
from pathlib import Path, PosixPath

from omegaconf import DictConfig, OmegaConf


def add_prefix_to_nested_config(conf: DictConfig, prefix: str) -> None:
    config = deepcopy(conf)
    for key, sub_config in conf.items():
        if isinstance(sub_config, DictConfig):
            config[key] = add_prefix_to_nested_config(sub_config, prefix)
        else:
            config[key] = f'{prefix}{sub_config}'
    return config


def load_data_yaml(
    config_file: str = 'data.yaml',
    data_dir: str = 'data',
    config_dir: str = 'conf',
) -> DictConfig:
    conf = load_config_yaml(config_file, config_dir)
    data_path = str(importlib.resources.files(data_dir).joinpath(''))
    return add_prefix_to_nested_config(conf, prefix=data_path)


def absolute_path(directory: str | Path) -> PosixPath:
    return (
        importlib.resources.files(
            str(directory).strip('/').replace('/', '.')
        )
        .joinpath('')
    )


def load_config_yaml(
    config_file: str = 'config.yaml',
    config_dir: str = 'conf',
) -> DictConfig:
    absolute_config_dir: PosixPath = absolute_path(config_dir)
    return OmegaConf.load(absolute_config_dir / config_file)
