"""Jupyter's notebook executor but with a tqdm progress bar."""

import os
from pathlib import Path
from typing import Any

from jupyter_client.manager import KernelManager
from nbclient import NotebookClient
from nbconvert import NotebookExporter
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat import NotebookNode
from nbformat import read as read_notebook

from bluprint_conf import absolute_package_path
from bluprint.notebook.progress import progress


def run_jupyter_notebook(
    notebook_file: str,
    display_prefix: str,
    notebook_dir: str = 'notebooks',
    timeout: int = -1,
) -> None:
    os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
    project_path = absolute_package_path(notebook_dir)
    executor = ExecutorWithProgressBar(timeout=timeout)
    notebook_results = executor.run_all_cells(
        Path(project_path) / notebook_file,
        display_prefix,
        {'metadata': {'path': '.'}},
    )
    exporter = NotebookExporter()
    with open(Path(project_path) / notebook_file, 'w') as notebook:
        notebook.write(exporter.from_notebook_node(notebook_results[0])[0])


class ExecutorWithProgressBar(ExecutePreprocessor):

    def run_all_cells(  # noqa: WPS210
        self,
        notebook_path: str | Path,
        prefix: str,
        resources: Any = None,
        km: KernelManager | None = None,
    ) -> tuple[NotebookNode, dict[str, Any]]:

        with open(notebook_path, 'r') as notebook_handle:
            notebook = read_notebook(notebook_handle, as_version=4)

        NotebookClient.__init__(self, notebook, km)  # noqa: WPS609
        self.reset_execution_trackers()
        self._check_assign_resources(resources)

        with self.setup_kernel():
            if not self.kc:
                raise KernelClientError
            info_msg = self.wait_for_reply(self.kc.kernel_info())
            if not info_msg:
                raise InfoMessageError
            self.nb.metadata['language_info'] = (
                info_msg['content']['language_info']
            )
            for cell_id, cell in enumerate(progress(self.nb.cells, prefix)):
                self.preprocess_cell(cell, resources, cell_id)
        self.set_widgets_metadata()
        return self.nb, self.resources


class KernelClientError(Exception):
    """Raised if nbclient kernel client crashes."""


class InfoMessageError(Exception):
    """Raised if info message cannot be obtained from nb kernel."""
