"""Command-line interface for bluprint."""

import sys
from os import getcwd
from pathlib import Path, PosixPath

import fire
from bluprint_conf import load_config_yaml

from bluprint.binary import check_if_executable_is_installed
from bluprint.colors import styled_print
from bluprint.create.py_project import create_project, initialize_project
from bluprint.create.r_project import (
    check_if_r_package_is_installed,
    initialize_r_project,
)
from bluprint.errors import ProjectExistsError
from bluprint.index import index_dir_to_config_yaml
from bluprint.workflow import run_workflow

sys.tracebacklimit = 0


class Bluprint(object):
    """Bluprint sub-commands used by CLI."""

    def create(
        self,
        project_name: str,
        python_version: str | None = None,
        parent_dir: str | None = None,
        r_proj: bool = False,
    ) -> None:
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

        Args:

        project_name (str): Name of the project, also the name of the main
        project directory.

        python_version (str | None, optional): Python version to be used. If
        not specified, uses the latest stable version from `pyenv install -l`.

        parent_dir (str | None, optional): Parent directory to create a
        PROJECT_NAME directory in. If not specific PARENT_DIR is a current
        directory.

        r_proj (bool, optional): Setup R library using renv to support package
        isolation in RMarkdown notebooks.

        """
        styled_print(
            'creating Python{with_r} project {project_name}... '.format(
                project_name=project_name,
                with_r='/R' if r_proj else '',
            ),
            endline='',
        )
        self.check_project(project_name, parent_dir, r_proj)
        create_project(project_name, python_version, parent_dir)
        if r_proj:
            initialize_r_project(project_name, parent_dir)
        styled_print('Ok', print_bluprint=False)

    def check_project(
        self,
        project_name: str,
        parent_dir: str | None = None,
        r_proj: bool = False,
    ) -> None:
        check_if_project_exists(project_name, parent_dir)
        check_if_executable_is_installed('pdm')
        if r_proj:
            check_if_executable_is_installed('Rscript')
            check_if_r_package_is_installed('renv')

    def init(
        self,
        project_name: str,
        python_version: str | None = None,
        project_dir: str | None = None,
        r_proj: bool = False,
    ) -> None:
        """Initialize a bluprint project in existing directory.

        Args:

        project_name (str): Name of the project.
        python_version (str | None, optional): Python version to be used.
            If not specified, uses `python --version`.
        project_dir (str | None, optional): Project directory where to
            initialize a new bluprint project. By default uses current working
            directory.
        r_proj (bool): Setup R library using renv to support package
            isolation in RMarkdown notebooks.

        Raises:
            ProjectExistsError: Raised if pyproject.toml exists in the
            `project_dir`.
        """
        if not project_dir:
            project_dir = getcwd()
        styled_print(
            'initializing Python{with_r} project {project_name}... '.format(
                project_name=project_name,
                with_r='/R' if r_proj else '',
            ),
            endline='',
        )
        if (Path(project_dir) / 'pyproject.toml').exists():
            raise ProjectExistsError(
                f'pyproject.toml already exists in {project_dir}: '
                + 'cannot initialize new bluprint project',
            )
        initialize_project(project_name, python_version, Path(project_dir))
        if r_proj:
            initialize_r_project(project_name)
        styled_print('Ok', print_bluprint=False)

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
        cfg = load_config_yaml(workflow_yaml)
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


def check_if_project_exists(project_name: str, parent_dir: str | None) -> None:
    if not parent_dir:
        parent_dir = '.'
    if (Path(parent_dir) / project_name).is_dir():
        raise ProjectExistsError(f'{project_name} directory exists.')


def main():
    fire.Fire(Bluprint)


if __name__ == '__main__':
    main()
