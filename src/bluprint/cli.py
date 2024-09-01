"""Command-line interface for bluprint."""

import importlib.metadata
import sys
from pathlib import Path

import fire

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

sys.tracebacklimit = 0


class Bluprint(object):
    """Bluprint sub-commands used by CLI."""

    def create(
        self,
        project_name: str,
        python_version: str | None = None,
        parent_dir: str | None = None,
        template_dir: str | None = None,
        r_project: bool = False,
        omit_examples: bool = False,
    ) -> None:
        """Create a directory with a bluprint project.

        Args:

        project_name (str): Name of the project, also the name of the main
            project directory.

        python_version (str | None, optional): Python version used in the
            project's virtual environment. If None, uses the Python in PATH
            or 3.11, whichever is greater. Must be >=3.11.

        parent_dir (str | None, optional): Parent directory to create a
            PROJECT_NAME directory in. If None, use a current directory.

        template_dir (str | None, optional): Path to a directory with a
            Bluprint template. If None, uses the built-in template.

        r_project (bool, optional): Setup R library using renv to support
            package isolation in RMarkdown notebooks.

        omit_examples (bool, optional): Omit example data and notebooks in the
            new project.

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
            omit_examples=omit_examples,
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
        omit_examples: bool = False,
        overwrite: bool = False,
    ) -> None:
        """Initialize a bluprint project in an existing directory.

        Same functionality as `bluprint create` but from an existing directory.

        Args:

        project_name (str): Name of the project.

        python_version (str | None, optional): Python version used in the
            project's virtual environment. If None, uses the Python in PATH
            or 3.11, whichever is greater. Must be >=3.11.

        project_dir (str | None, optional): Project directory in which to
            initialize a new bluprint project. If None, uses current working
            directory.

        template_dir (str | None, optional): Path to a directory with a
            Bluprint template. If None, uses the built-in template.

        r_project (bool): Setup R library using renv to support package
            isolation in RMarkdown notebooks.

        omit_examples (bool, optional): Omit example data and notebooks in the
            new project.

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
            omit_examples=omit_examples,
            overwrite=overwrite,
        )
        if r_project:
            initialize_r_project(project_name, project_dir)
        styled_print(f'project `{project_name}` created.')

    def index(
        self,
        input_dir: str,
        output_yaml: str,
        include_dot_files: bool = False,
    ) -> None:
        """Index all directory files to yaml config.

        Recursively iterates over all files in INPUT_DIR and creates a
        reasonable yaml config in OUTPUT_YAML. This command helps
        convert an existing data directory into a bluprint project.

        Args:
            input_dir (str): Directory to index.
            output_yaml (str): Output yaml filepath.
            include_dot_files (bool, optional): Include hidden files starting
                with a dot into an index.
        """
        styled_print(f'index {input_dir}/** ❯ {output_yaml}')  # noqa: RUF001
        index_dir_to_config_yaml(input_dir, output_yaml, include_dot_files)

    def version(self) -> None:
        """Show bluprint version."""
        styled_print('version {version}'.format(
            version=importlib.metadata.version('bluprint'),
        ))


def main():
    fire.Fire(Bluprint)  # pragma: no cover


if __name__ == '__main__':  # pragma: no cover
    main()
