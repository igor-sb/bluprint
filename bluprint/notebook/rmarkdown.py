"""Hacky RMarkdown notebook executor with a tdqm progress bar."""

import re
import subprocess
from tqdm import tqdm
from bluprint.notebook.progress import progress


def number_of_r_cells_in_rmd(rmd_file: str) -> int:
	r_cell_re = re.compile(r'^```\{r[^\}]+\}')
	number_of_r_cells = 0
	with open(rmd_file) as rmd:
		for rmd_line in rmd:
			if r_cell_re.match(rmd_line):
				number_of_r_cells += 1
	return number_of_r_cells


def execute_rmd(rmd_file: str) -> None:
	rmd_out = subprocess.run([
		'Rscript',
		'-e',
		'rmarkdown::render()'
	])