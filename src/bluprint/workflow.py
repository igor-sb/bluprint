"""Bluprint workflow orchestrator."""

from pathlib import Path

from bluprint_conf import absolute_package_path, load_config_yaml
from omegaconf import DictConfig, ListConfig

from bluprint.colors import style_notebook, style_workflow, styled_print
from bluprint.errors import InvalidNotebookTypeError, InvalidWorkflowError
from bluprint.notebook.jupyter import run_jupyter_notebook
from bluprint.notebook.rmarkdown import run_rmarkdown_notebook


def run_workflow(
    workflow_name: str,
    workflow_cfg: DictConfig | ListConfig,
    notebook_dir: str = 'notebooks',
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
        run_notebook(notebook_file, notebook_dir, graphical_prefix)


def run_notebook(
    notebook_file: str | Path,
    notebook_dir: str = 'notebooks',
    graphical_prefix: str = '',
) -> None:
    if not Path(notebook_file).is_absolute() and notebook_dir is not None:
        if Path(notebook_dir).is_absolute():
            notebook_file = Path(notebook_dir) / notebook_file
        else:
            notebook_file = str(
                Path(absolute_package_path(notebook_dir)) / notebook_file,
            )

    match Path(notebook_file).suffix:
        case '.ipynb':
            run_jupyter_notebook(
                notebook_file=notebook_file,
                display_prefix=graphical_prefix,
            )
        case '.Rmd':
            run_rmarkdown_notebook(
                notebook_file=notebook_file,
                display_prefix=graphical_prefix,
            )
        case '.qmd':
            pass  # noqa: WPS420
        case nb_extension:
            raise InvalidNotebookTypeError(
                f'Invalid extension {nb_extension} in {notebook_file}',
            )


def run_workflows(
    workflow_yaml: str | Path = 'conf/workflows.yaml',
    notebook_dir: str | Path = 'notebooks',
):
    workflow_cfg = load_config_yaml(workflow_yaml)
    styled_print('run all workflows')
    for workflow_name in workflow_cfg.keys():
        run_workflow(str(workflow_name), workflow_cfg, str(notebook_dir))


def add_graphic_prefixes(notebooks: list[str]) -> list[str]:
    ascii_out = [
        style_notebook(f'├─── {notebook_name}')
        for notebook_name in notebooks
    ]
    ascii_out[-1] = ascii_out[-1].replace('├', '└')
    return ascii_out
