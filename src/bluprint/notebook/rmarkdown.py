"""RMarkdown notebook executor with a tdqm progress bar."""

import re
import subprocess
import sys
from pathlib import Path

from tqdm import tqdm

from bluprint.notebook.progress import tqdm_format_without_total


def run_rmarkdown_notebook(  # noqa: WPS210
    notebook_file: str | Path,
    display_prefix: str,
    notebook_dir: str | Path | None = 'notebooks',
) -> None:
    progress_bar_pct = re.compile(r'^[\s]*\|[\.]*[\s]*\|[\s]*([0-9]+)%.*$')
    progress_bar_frac = re.compile(r'^([0-9]+)/([0-9]+)\s.*$')
    with (
        tqdm(
            total=100,
            desc=display_prefix,
            bar_format=tqdm_format_without_total(),
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
            if progress_bar_pct.match(line):
                current_percent = int(progress_bar_pct.sub(r'\1', line))
            elif progress_bar_frac.match(line):
                current_cell = int(progress_bar_frac.sub(r'\1', line))
                total_cells = int(progress_bar_frac.sub(r'\2', line))
                current_percent = 100 * current_cell // total_cells
            # else: # debug
            #    sys.stderr.write(line)
            #print(line)
            tqdm_progress.update(current_percent - last_percent)
            sys.stdout.flush()
            last_percent = current_percent

        rmd_out.stdout.close()  # type: ignore
