"""Simple workflow orchestrator."""

import logging

import fire

from bluprint.colors import style_notebook, style_workflow
from bluprint.config import load_config_yaml
from bluprint.notebook import run_notebook


def add_graphic_prefixes(notebooks: list[str]) -> list[str]:
    ascii_out = [
        style_notebook(f'├─── {notebook_name}')
        for notebook_name in notebooks
    ]
    ascii_out[-1] = ascii_out[-1].replace('├', '└')
    return ascii_out


def run_workflow(
    workflow_yaml: str = 'workflows.yaml',
    yaml_dir: str = 'conf',
    notebook_dir: str = 'notebooks',
) -> None:
    workflows = load_config_yaml(workflow_yaml, yaml_dir)
    logging.info('Running workflows:')
    for workflow_name, notebooks in workflows.items():
        logging.info(style_workflow(workflow_name))
        for nb_file, prefix in zip(notebooks, add_graphic_prefixes(notebooks)):
            run_notebook(
                notebook_file=nb_file,
                display_prefix=prefix,
                notebook_dir=notebook_dir,
            )
    logging.info('Done.')


if __name__ == '__main__':
    logging.basicConfig(
        style='{',
        format='{message}',
        encoding='utf-8',
        level=logging.INFO,
    )
    fire.Fire(run_workflow)
