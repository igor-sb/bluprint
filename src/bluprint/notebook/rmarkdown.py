"""RMarkdown notebook executor with a tdqm progress bar."""

import re
import subprocess
import sys
from pathlib import Path

from bluprint_conf import absolute_package_path
from tqdm import tqdm

from bluprint.notebook.progress import tqdm_format


def run_rmarkdown_notebook(  # noqa: WPS210
    notebook_file: str,
    display_prefix: str,
    notebook_dir: str = 'notebooks',
) -> None:
    if not Path(notebook_file).is_absolute():
        notebook_file = (
            Path(absolute_package_path(notebook_dir)) / notebook_file    
        )

    progress_bar_re = re.compile(r'^[\s]*\|[\.\s]*\|[\s]*([0-9]+)%$')
    with (
        tqdm(
            total=100,
            desc=display_prefix,
            bar_format=tqdm_format(),
        ) as tqdm_progress
    ):
        rmd_out = subprocess.Popen(
            ['Rscript', '-e', f'rmarkdown::render("{notebook_file}")'],
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        last_percent = 0
        for line in rmd_out.stdout:  # type: ignore
            if progress_bar_re.match(line):
                current_percent = int(progress_bar_re.sub(r'\1', line))
                tqdm_progress.update(current_percent - last_percent)
                sys.stdout.flush()
                last_percent = current_percent
        rmd_out.stdout.close()  # type: ignore
