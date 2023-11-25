"""Command-line interface for bluprint."""

from pathlib import Path, PosixPath

import fire

from bluprint.colors import styled_print
from bluprint.config import load_config_yaml
from bluprint.index import index_dir_to_config_yaml
from bluprint.project import create_project
from bluprint.workflow import run_workflow


class Bluprint(object):
    """Bluprint sub-commands used by CLI."""

    def create(self, project_name: str):
        """Create a directory with a bluprint project.

        Creates a project directory structure:
        - .venv/: virtual environment
        - conf/: yaml configurations
        - data/: tables and other data files
        - PROJECT_NAME/: source (non-notebook) code for this project
        - notebooks/: Jupyter notebooks
        - pyproject.toml: project package configuration
        - README.md: readme file

        Also, initalizes, a python package PROJECT_NAME in editable mode. This
        means that files within PROJECT_NAME/ are accessible in notebooks
        as a Python package, without a need to `pip install` them each time
        there is a change.

        """
        styled_print(f'create {project_name}')
        create_project(project_name)

    def init(self):
        """Initialize a bluprint project in existing directory."""
        print('Initializing project.')  # noqa: WPS421

    def workflow(
        self,
        workflow_name: str,
        workflow_yaml: str | PosixPath = 'conf/workflows.yaml',
        notebook_dir: str | PosixPath = 'notebooks',
    ) -> None:
        """Run a single workflow.

        Run a single workflow by its name, which a key in the workflow_yaml
        config file. E.g. if workflow_yaml is:

        test_workflow:
          - test1.ipynb
          - test2.ipynb

        then the workflow name is `test_workflow`.

        Args:

        workflow_name (str): Key in the workflow_yaml config that labels a
        workflow (a list of notebooks).

        workflow_yaml (str | PosixPath, optional): Workflow YAML filename.

        workflow_yaml_dir (str | PosixPath, optional): Root directory
        containing workflow YAML.

        notebook_dir (str | PosixPath, optional): Root directory containing
        all the notebooks.

        """
        styled_print(f'run workflow {workflow_name}')
        cfg = load_config_yaml(
            Path(workflow_yaml).name,
            Path(workflow_yaml).parent,
        )
        run_workflow(
            workflow_name=workflow_name,
            workflow_cfg=cfg,
            notebook_dir=notebook_dir,
        )

    def index(self, input_dir: str, output_yaml: str) -> None:
        """Index all directory files to yaml config.

        Recursively iterates over all files in INPUT_DIR and creates a
        reasonable yaml config in OUTPUT_YAML. This command helps
        convert an existing data directory into a bluprint project.

        """
        styled_print(f'index {input_dir}/** ❯ {output_yaml}')
        index_dir_to_config_yaml(input_dir, output_yaml)


def main():
    fire.Fire(Bluprint)


if __name__ == '__main__':
    main()
