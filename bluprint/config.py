"""Code for manipulating YAML configuration files."""

from copy import deepcopy
from importlib import resources
from pathlib import Path, PosixPath, PurePath
from typing import Any
from omegaconf import DictConfig, ListConfig, OmegaConf
from urllib.parse import urlparse

def add_prefix_to_nested_config(
    conf: DictConfig | ListConfig,
    prefix: str,
) -> DictConfig | ListConfig:
    
    def recurse_or_add_suffix(conf_value: Any) -> Any:
        if isinstance(conf_value, DictConfig | ListConfig):
            return add_prefix_to_nested_config(conf_value, prefix)
        if _is_abs_path(conf_value) or _is_uri(conf_value):
            return conf_value
        return str(Path(prefix) / str(conf_value))

    if isinstance(conf, ListConfig):
        return [recurse_or_add_suffix(conf_value) for conf_value in conf]
    elif isinstance(conf, DictConfig):
        return OmegaConf.create({
            conf_key: recurse_or_add_suffix(conf_values)
            for conf_key, conf_values in conf.items()
        })


def _is_abs_path(value: Any) -> bool:
    return PurePath(str(value)).is_absolute()


def _is_uri(value: Any) -> bool:
    result = urlparse(str(value))
    return all([result.scheme, result.netloc])


def load_data_yaml(
    config_file: str = 'data.yaml',
    data_dir: str = 'data',
    config_dir: str = 'conf',
) -> DictConfig | ListConfig:
    conf = load_config_yaml(config_file, config_dir)
    data_path = str(resources.files(data_dir).joinpath(''))
    return add_prefix_to_nested_config(conf, prefix=data_path)


def absolute_path(directory: str | PosixPath) -> PosixPath:
    return (
        resources.files(
            str(directory).strip('/').replace('/', '.'),
        )
        .joinpath('')
    )


def load_config_yaml(
    config_file: str = 'config.yaml',
    config_dir: str | PosixPath = 'conf',
) -> DictConfig | ListConfig:
    absolute_config_dir: PosixPath = absolute_path(config_dir)
    return OmegaConf.load(absolute_config_dir / config_file)
