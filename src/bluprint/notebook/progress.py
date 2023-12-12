"""Stylized progress bar for running individual notebooks."""

from typing import Iterable

from tqdm import tqdm

from bluprint.colors import Style


def tqdm_format() -> str:
    sep = f'{Style.cyan}─{Style.end}'
    return (
        '{desc} {percentage:3.0f}% '
        + sep + ' {n_fmt}/{total_fmt} cells '
        + sep + ' Elapsed: {elapsed}'
    )


def progress(iterable: Iterable, name: str) -> Iterable:
    return tqdm(iterable, desc=name, bar_format=tqdm_format())
