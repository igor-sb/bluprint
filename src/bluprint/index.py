"""Indexing directory contents into a YAML config."""

import os
from pathlib import Path, PosixPath

from omegaconf import DictConfig, OmegaConf


def _index_files_in_dir(
    index_dir: str | PosixPath,
    skip_dot_files: bool = True,
) -> list[tuple[str, ...]]:
    indexed_files = []
    for root, _, files in os.walk(index_dir):
        for file in files:  # noqa: WPS110
            file_path = Path(root) / file
            if file.startswith('.') and skip_dot_files:
                continue
            indexed_files.append(
                file_path.parts[len(Path(index_dir).parts):],
            )
    return sorted(indexed_files)


def _create_config_from_indexed_files(  # noqa: WPS210
    indexed_files: list[tuple[str, ...]],
) -> DictConfig:
    config_dotlist = []
    unique_dotkeys = []
    for indexed_file in indexed_files:
        final_key = Path(indexed_file[-1]).stem.replace('.', '_')
        nonfinal_keys = [part.replace('.', '_') for part in indexed_file[:-1]]
        dotkey = '.'.join([*nonfinal_keys, final_key])
        if dotkey in unique_dotkeys:
            dotkey = '.'.join([
                *nonfinal_keys,
                indexed_file[-1].replace('.', '_'),
            ])
        unique_dotkeys.append(dotkey)
        config_dotlist.append(
            '{key}={value}'.format(
                key=dotkey,
                value='/'.join(indexed_file),
            ),
        )
    return OmegaConf.from_dotlist(config_dotlist)


def index_dir_to_config_yaml(
    input_dir: str | PosixPath,
    output_yaml: str | PosixPath,
    skip_dot_files: bool = True,
) -> int:
    indexed_files = _index_files_in_dir(input_dir, skip_dot_files)
    OmegaConf.save(
        _create_config_from_indexed_files(indexed_files),
        output_yaml,
    )
    return len(indexed_files)
