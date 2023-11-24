"""Code for manipulating YAML configuration files."""

from copy import deepcopy
from importlib import resources
from pathlib import Path, PosixPath

from omegaconf import DictConfig, ListConfig, OmegaConf


# MODIFY THIS TO SUPPORT DICTCONFIG AND LISTCONFIG
def add_prefix_to_nested_config(
    conf: DictConfig | ListConfig,
    prefix: str,
) -> DictConfig | ListConfig:
    config = deepcopy(conf)
    if isinstance(config, ListConfig):
        for index, sub_config in enumerate(config):
            if isinstance(sub_config, DictConfig | ListConfig):
                config[index] = add_prefix_to_nested_config(sub_config, prefix)
            else:
                config[index] = f'{prefix}{sub_config}'
            
    elif isinstance(config, DictConfig):
        for key, sub_config in conf.items():
            if isinstance(sub_config, DictConfig | ListConfig):
                config[key] = add_prefix_to_nested_config(sub_config, prefix)
            else:
                config[key] = f'{prefix}{sub_config}'
    return config


def load_data_yaml(
    config_file: str = 'data.yaml',
    data_dir: str = 'data',
    config_dir: str = 'conf',
) -> DictConfig | ListConfig:
    conf = load_config_yaml(config_file, config_dir)
    data_path = str(resources.files(data_dir).joinpath(''))
    return add_prefix_to_nested_config(conf, prefix=data_path)


def absolute_path(directory: str | Path) -> PosixPath:
    return (
        resources.files(
            str(directory).strip('/').replace('/', '.'),
        )
        .joinpath('')
    )


def load_config_yaml(
    config_file: str = 'config.yaml',
    config_dir: str = 'conf',
) -> DictConfig | ListConfig:
    absolute_config_dir: PosixPath = absolute_path(config_dir)
    return OmegaConf.load(absolute_config_dir / config_file)
