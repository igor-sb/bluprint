"""Command-line interface for bluprint."""

import sys
from pathlib import Path

import fire
from bluprint_conf import load_config_yaml

from bluprint.colors import styled_print
from bluprint.create.py_project import (
    check_python_version,
    create_python_project,
    initialize_python_project,
)
from bluprint.create.r_project import create_r_project, initialize_r_project
from bluprint.index import index_dir_to_config_yaml
from bluprint.project import (
    check_if_project_can_be_created,
    check_if_project_files_exist,
    get_current_working_dir,
)
from bluprint.workflow import run_notebook, run_workflow

# sys.tracebacklimit = 0


class Bluprint(object):
    """Bluprint sub-commands used by CLI."""

    def create(
        self,
        project_name: str,
        python_version: str | None = None,
        parent_dir: str | None = None,
        template_dir: str | None = None,
        r_project: bool = False,
        add_examples: bool = True,
    ) -> None:
        """Create a directory with a bluprint project:

        .
        ├── .venv                         Project's Python virtual environment
        ├── conf                          Yaml configuration files
        │   ├── config.yaml                 Accessible using load_config_yaml()
        │   ├── data.yaml                   Accessible using load_data_yaml()
        │   └── workflow.yaml               Used by bluprint workflow
        ├── data                          Local data (e.g. csv, png, pdf)
        │   └── example_data.csv
        ├── notebooks                     Jupyter/R/Quarto notebooks
        │   ├── example_jupyternb.ipynb
        │   └── example_quarto.qmd
        ├── myproj                        Python package of this project
        │   └── example.py                  Modules within myproj package
        ├── .gitignore                    Files excluded from version control
        ├── README.md                     Readme file describing the project
        ├── pyproject.toml                Project configuration
        └── uv.lock                       Locked version of Python dependencies

        Bluprint also makes all files within PROJECT_NAME/ accessible to
        notebooks as an editable Python package: after changing the files re-run
        the notebook for changes to update.

        Args:

        project_name (str): Name of the project, also the name of the main
            project directory.

        python_version (str | None, optional): Python version to be used. If
            not specified, uses either the latest stable version from
            `pyenv install -l` or 3.11 (whichever is greater). Bluprint requires
            Python >= 3.11.

        parent_dir (str | None, optional): Parent directory to create a
            PROJECT_NAME directory in. If not specific PARENT_DIR is a current
            directory.

        template_dir (str | None, optional): Path to a directory with a
            Bluprint template. If not specified (default), uses Bluprint
            default built-in template.

        r_project (bool, optional): Setup R library using renv to support
            package isolation in RMarkdown notebooks.

        add_examples (bool, optional): Add example data and notebooks in the new
            project.

        """
        styled_print(
            'creating Python{with_r} project {project_name}'.format(
                project_name=project_name,
                with_r='/R' if r_project else '',
            ),
        )
        check_if_project_can_be_created(
            project_name=project_name,
            parent_dir=parent_dir,
            r_project=r_project,
        )
        check_python_version(python_version)
        create_python_project(
            project_name=project_name,
            python_version=python_version,
            parent_dir=parent_dir,
            template_dir=template_dir,
            keep_r_files=r_project,
            add_examples=add_examples,
        )
        if r_project:
            create_r_project(project_name, parent_dir)
        styled_print(f'project `{project_name}` created.')

    def init(
        self,
        project_name: str,
        python_version: str | None = None,
        project_dir: str | None = None,
        template_dir: str | None = None,
        r_project: bool = False,
        add_examples: bool = True,
        overwrite: bool = False,
    ) -> None:
        """Initialize a bluprint project in an existing directory.

        Same functionality as `bluprint create` but from an existing directory.

        Args:

        project_name (str): Name of the project.

        python_version (str | None, optional): Python version to be used. If
            not specified, uses either the latest stable version from
            `pyenv install -l` or 3.11 (whichever is greater). Bluprint requires
            Python >= 3.11.

        project_dir (str | None, optional): Project directory where to
            initialize a new bluprint project. By default uses current working
            directory.

        template_dir (str | None, optional): Path to a directory with a
            Bluprint template. If not specified (default), uses Bluprint
            default built-in template.

        r_project (bool): Setup R library using renv to support package
            isolation in RMarkdown notebooks.

        add_examples (bool, optional): Add example data and notebooks in the new
            project.

        overwrite (bool, optional): Overwrite existing files.

        Raises:

            ProjectExistsError: Raised if pyproject.toml exists in
                the `project_dir`.
        """
        styled_print(
            'initializing Python{with_r} project {project_name}'.format(
                project_name=project_name,
                with_r='/R' if r_project else '',
            ),
        )
        if not project_dir:
            project_dir = get_current_working_dir()
        check_if_project_files_exist(project_name, project_dir, overwrite)
        check_python_version(python_version)
        initialize_python_project(
            project_name=project_name,
            python_version=python_version,
            project_dir=Path(project_dir),
            template_dir=template_dir,
            keep_r_files=r_project,
            add_examples=add_examples,
            overwrite=overwrite,
        )
        if r_project:
            initialize_r_project(project_name, project_dir)
        styled_print(f'project `{project_name}` created.')

    def notebook(
        self,
        notebook_file: str | Path,
    ) -> None:
        """Run a single Jupyter/Rmarkdown notebook.

        Args:
            notebook_file (str | Path): Notebook filename.
        """
        styled_print(f'run notebook {notebook_file}')
        run_notebook(notebook_file)

    def workflow(
        self,
        workflow_name: str,
        workflow_yaml: str | Path = 'conf/workflows.yaml',
        notebook_dir: str = 'notebooks',
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

    def index(
        self,
        input_dir: str,
        output_yaml: str,
        skip_dot_files: bool = True,
    ) -> None:
        """Index all directory files to yaml config.

        Recursively iterates over all files in INPUT_DIR and creates a
        reasonable yaml config in OUTPUT_YAML. This command helps
        convert an existing data directory into a bluprint project.

        Args:
            input_dir (str): Directory to index.
            output_yaml (str): Output yaml filepath.
            skip_dot_files (bool, optional): Skip files starting with a dot.
        """
        styled_print(f'index {input_dir}/** ❯ {output_yaml}')  # noqa: RUF001
        index_dir_to_config_yaml(input_dir, output_yaml, skip_dot_files)


def main():
    fire.Fire(Bluprint)  # pragma: no cover


if __name__ == '__main__':  # pragma: no cover
    main()  # pragma: no cover
