"""Code for manipulating YAML configuration files."""

from importlib import resources
from pathlib import Path, PosixPath, PurePath
from typing import Any
from urllib.parse import urlparse

from omegaconf import DictConfig, ListConfig, OmegaConf


def add_prefix_to_nested_config(
    conf: DictConfig | ListConfig,
    prefix: str,
) -> DictConfig | ListConfig:

    def recurse_or_add_suffix(conf_value: Any) -> Any:  # noqa: WPS430
        if isinstance(conf_value, DictConfig | ListConfig):
            return add_prefix_to_nested_config(conf_value, prefix)
        if _is_abs_path(conf_value) or _is_uri(conf_value):
            return conf_value
        return str(Path(prefix) / str(conf_value))

    if isinstance(conf, ListConfig):
        return OmegaConf.create([
            recurse_or_add_suffix(conf_value)
            for conf_value in conf
        ])
    elif isinstance(conf, DictConfig):
        return OmegaConf.create({
            conf_key: recurse_or_add_suffix(conf_values)
            for conf_key, conf_values in conf.items()
        })


def _is_abs_path(conf_value: Any) -> bool:
    return PurePath(str(conf_value)).is_absolute()


def _is_uri(conf_value: Any) -> bool:
    parsed_url = urlparse(str(conf_value))
    return all([parsed_url.scheme, parsed_url.netloc])


def load_data_yaml(
    config_file: str = 'data.yaml',
    data_dir: str = 'data',
    config_dir: str = 'conf',
) -> DictConfig | ListConfig:
    conf = load_config_yaml(config_file, config_dir)
    data_path = str(resources.files(data_dir).joinpath(''))
    return add_prefix_to_nested_config(conf, prefix=data_path)


def absolute_path(directory: str | PosixPath | Path) -> str:
    path_as_module = str(directory).strip('/').replace('/', '.')
    return str(resources.files(path_as_module).joinpath(''))


def load_config_yaml(
    config_file: str = 'config.yaml',
    config_dir: str | PosixPath | Path = 'conf',
) -> DictConfig | ListConfig:
    absolute_config_dir = absolute_path(config_dir)
    return OmegaConf.load(Path(absolute_config_dir) / config_file)
