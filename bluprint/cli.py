"""Command-line interface for bluprint."""

import sys
from pathlib import Path, PosixPath

import fire

from bluprint.config import load_config_yaml
from bluprint.project import create_project
from bluprint.workflow import run_workflow


class Bluprint(object):
    """Bluprint sub-commands used by CLI."""

    def create(self, project_name: str):
        """Create a new directory with a bluprint project."""
        print(f'Creating a new project {project_name}.')  # noqa: WPS421
        create_project(project_name)

    def init(self):
        """Initialize a bluprint project in existing directory."""
        print('Initializing project.')  # noqa: WPS421

    def workflow(
        self,
        workflow_name: str,
        workflow_yaml: str | PosixPath = 'workflows.yaml',
        workflow_yaml_dir: str | PosixPath = 'conf',
        notebook_dir: str | PosixPath = 'notebooks',
    ):
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
        sys.stderr.write('Running single workflow:\n')
        cfg = load_config_yaml(workflow_yaml, workflow_yaml_dir)
        run_workflow(
            workflow_name=workflow_name,
            workflow_cfg=cfg,
            notebook_dir=notebook_dir,
        )
        sys.stderr.write('Done.\n')

    def index(self, input_dir: str, output_yaml: str):
        """Automatically create yaml config from files in input_dir."""
        print('Generating config.')  # noqa: WPS421


def main():
    fire.Fire(Bluprint)


if __name__ == '__main__':
    main()
