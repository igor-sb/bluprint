"""Code for manipulating Bluprint YAML configuration files."""

import os
from pathlib import Path, PurePath
from typing import Any
from urllib.parse import urlparse

from omegaconf import DictConfig, ListConfig, OmegaConf

from bluprint.project import absolute_path_in_project


def load_config_yaml(
    config_file: str | Path = 'conf/config.yaml',
    use_package_path_for_config: bool = True,
) -> DictConfig | ListConfig:
    """Load project configuration yaml

    Parses relative paths and opens yaml configuration using OmegaConf.

    Args:
        config_file (str | Path, optional): Relative or absolute path to the
          yaml configuration.

        use_package_path_for_config (bool, optional): If this is True, then
          relative path of `config_file` is parsed with respect to the project
          root and not with respect to the path of the calling script.

    Returns:
        DictConfig | ListConfig: Return value of OmegaConf.create().
    """
    if not Path(config_file).is_absolute() and use_package_path_for_config:
        config_file = absolute_path_in_project(config_file)
    return OmegaConf.load(config_file)


def load_config_yamls(
    config_dir: str | Path,
    use_package_path_for_config: bool = True,
) -> DictConfig | ListConfig:
    """Load multiple yamls into a single config

    Recursively iterates `config_dir`, loading all .yaml and .yml files, then
    merges them all into a single OmegaConf dictionary.

    Args:

        config_dir (str | Path): Directory with one or more yaml files.

        use_package_path_for_config (bool, optional): If this is True,
          then relative paths are parsed with respect to the project root and
          not with respect to the path of the calling script.

    Returns:

        DictConfig | ListConfig: Return value of OmegaConf.create().
    """
    if not Path(config_dir).is_absolute() and use_package_path_for_config:
        config_dir = absolute_path_in_project(config_dir)
    yaml_files = find_yaml_files_in_dir(config_dir)
    configs = [
        load_config_yaml(yaml_file, use_package_path_for_config)
        for yaml_file in yaml_files
    ]
    return OmegaConf.unsafe_merge(*configs)


def load_data_yaml(
    config_file: str | Path = 'conf/data.yaml',
    data_dir: str | Path = 'data',
    use_package_path_for_config: bool = True,
) -> DictConfig | ListConfig:
    """Load data configuration yaml

    Load yaml configuration with file paths and parses file paths relative to
      the project root directory.

    Args:
        config_file (str | Path, optional): Relative or absolute path to the
          yaml configuration. Defaults to 'conf/data.yaml'.
        data_dir (str | Path, optional): Directory with local data. Defaults to
          'data'.
        use_package_path_for_config (bool, optional): If this is True,
          then relative paths are parsed with respect to the project root and
          not with respect to the path of the calling script.

    Returns:
        DictConfig | ListConfig: Return value of OmegaConf.create().
    """
    if not Path(config_file).is_absolute() and use_package_path_for_config:
        config_file = absolute_path_in_project(config_file)
    conf = load_config_yaml(config_file)
    data_path = str(absolute_path_in_project(data_dir))
    return add_prefix_to_nested_config(conf, prefix=data_path)


def load_data_yamls(
    config_dir: str | Path,
    data_dir: str | Path = 'data',
    use_package_path_for_config: bool = True,
) -> DictConfig | ListConfig:
    """Load multiple data yamls into a single config

    Recursively iterates `config_dir`, loading all .yaml and .yml files, then
    merges them all into a single OmegaConf dictionary.

    Args:
        config_dir (str | Path): Directory with one or more yaml files.

        data_dir (str | Path, optional): Directory with local data.

        use_package_path_for_config (bool, optional): If this is True, then
          relative paths are parsed with respect to the project root and not
          with respect to the path of the calling script.

    Returns:
        DictConfig | ListConfig: Return value of OmegaConf.create().
    """
    if not Path(config_dir).is_absolute() and use_package_path_for_config:
        config_dir = absolute_path_in_project(config_dir)
    yaml_files = find_yaml_files_in_dir(config_dir)
    configs = [
        load_data_yaml(yaml_file, data_dir, use_package_path_for_config)
        for yaml_file in yaml_files
    ]
    return OmegaConf.unsafe_merge(*configs)


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


def find_yaml_files_in_dir(
    index_dir: str | Path,
) -> list[Path]:
    indexed_files = []
    for root, _, indexed_file_list in os.walk(index_dir):
        for indexed_file in indexed_file_list:
            indexed_file_with_path = Path(root) / indexed_file
            if indexed_file.endswith('.yaml') or indexed_file.endswith('.yml'):
                indexed_files.append(indexed_file_with_path)
    indexed_files.sort()
    return indexed_files
