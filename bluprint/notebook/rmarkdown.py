"""Hacky RMarkdown notebook executor with a tdqm progress bar."""

import re
import subprocess
import sys

from tqdm import tqdm

from bluprint.notebook.progress import tqdm_format


def execute_rmd(rmd_file: str) -> None:  # noqa: WPS210
    progress_bar_re = re.compile(r'^[\s]*\|[\.\s]*\|[\s]*([0-9]+)%$')
    with tqdm(total=100, bar_format=tqdm_format()) as tqdm_progress:
        rmd_out = subprocess.Popen(
            ['Rscript', '-e', f'rmarkdown::render("{rmd_file}")'],
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        last_percent = 0
        for line in rmd_out.stdout:
            if progress_bar_re.match(line):
                current_percent = int(progress_bar_re.sub(r'\1', line))
                tqdm_progress.update(current_percent - last_percent)
                sys.stdout.flush()
                last_percent = current_percent
        rmd_out.stdout.close()
