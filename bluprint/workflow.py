"""Simple workflow orchestrator."""

import fire
import pathlib
import logging
from dataclasses import dataclass


def load_workflow_yaml(yaml_file: str | pathlib.Path) -> dict[str]:
	pass


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def format_to_tree(item_list: list[str]) -> list[str]:
	ascii_out = [' ├─── ' + item for item in item_list]
	ascii_out[-1] = ascii_out[-1].replace('├', '└')
	return ascii_out


def main() -> None:
	# load workflows from yaml
	workflows = {
		'test_workflow': ['test1.ipynb', 'test2.ipynb'],
		'xtest_workflow': ['xtest1.ipynb', 'xtest2.ipynb'],
	}

	logging.info('Running workflows:')
	for workflow_name, notebooks in workflows.items():
		formatted_notebook_names = format_to_tree(notebooks)
		logging.info(f' {workflow_name}')
		for formatted_name in formatted_notebook_names:
			logging.info(formatted_name)
	

if __name__ == '__main__':
	logging.basicConfig(
		format='%(asctime)s %(levelname)s  %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		encoding='utf-8',
		level=logging.INFO,
	)
	fire.Fire(main)