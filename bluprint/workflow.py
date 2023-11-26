"""Bluprint workflow orchestrator."""

from pathlib import PosixPath, Path

from omegaconf import DictConfig, ListConfig

from bluprint.colors import style_notebook, style_workflow, styled_print
from bluprint.config import load_config_yaml
from bluprint.notebook.jupyter import run_jupyter_notebook


class InvalidWorkflowError(Exception):
    """Raises exception when invalid workflow is specified."""


class InvalidNotebookType(Exception):
    """Raises exception when invalid notebook type is specified."""


def run_workflow(
    workflow_name: str,
    workflow_cfg: DictConfig | ListConfig,
    notebook_dir: str | PosixPath = 'notebooks',
) -> None:
    if workflow_name not in workflow_cfg:
        raise InvalidWorkflowError(f'{workflow_name} does not exist.')
    workflow_notebooks = workflow_cfg[workflow_name]  # type: ignore
    styled_print(
        style_workflow(str(workflow_name)),
        print_bluprint=False,
    )
    workflow_notebooks_with_prefixes = zip(
        workflow_notebooks,
        add_graphic_prefixes(workflow_notebooks),
    )
    for notebook_file, graphical_prefix in workflow_notebooks_with_prefixes:
        match Path(notebook_file).suffix:
            case '.ipynb':
                run_jupyter_notebook(
                    notebook_file=notebook_file,
                    display_prefix=graphical_prefix,
                    notebook_dir=str(notebook_dir),
                )
            case '.Rmd':
                pass
            case '.qmd':
                pass
            case nb_extension:
                raise InvalidNotebookType(f'Invalid extension {nb_extension}')


def run_workflows(
    workflow_yaml: str | PosixPath = 'workflows.yaml',
    workflow_yaml_dir: str | PosixPath = 'conf',
    notebook_dir: str | PosixPath = 'notebooks',
):
    workflow_cfg = load_config_yaml(str(workflow_yaml), workflow_yaml_dir)
    styled_print('run all workflows')
    for workflow_name in workflow_cfg.keys():
        run_workflow(str(workflow_name), workflow_cfg, notebook_dir)


def add_graphic_prefixes(notebooks: list[str]) -> list[str]:
    ascii_out = [
        style_notebook(f'├─── {notebook_name}')
        for notebook_name in notebooks
    ]
    ascii_out[-1] = ascii_out[-1].replace('├', '└')
    return ascii_out
