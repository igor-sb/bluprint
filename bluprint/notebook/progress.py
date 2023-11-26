"""Stylized progress bar for running individual notebooks."""

from typing import Iterable

from tqdm import tqdm

from bluprint.colors import Style


def progress(iterable: Iterable, name: str) -> Iterable:
    sep = f'{Style.cyan}─{Style.end}'
    return tqdm(
        iterable,
        desc=name,
        bar_format=(
            '{desc} {percentage:3.0f}% '
            + sep + ' {n_fmt}/{total_fmt} cells '
            + sep + ' Elapsed: {elapsed}'
        ),
    )