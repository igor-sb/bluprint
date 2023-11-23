import os
from typing import Any, Iterable

from jupyter_client.manager import KernelManager
from nbclient import NotebookClient
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat import NotebookNode, read
from tqdm import tqdm

from bluprint.config import load_workflow_yaml


def progress(iterable: Iterable, name: str) -> None:
    return tqdm(
        iterable,
        ncols=60,
        colour='blue',
        desc=name,
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} cells | Elapsed: {elapsed}'
    )


class ExecutorWithProgressBar(ExecutePreprocessor):
      
    def run_all_cells(
        self,
        # nb: NotebookNode,
        notebook_path: str,
        resources: Any = None,
        km: KernelManager | None = None,
    ) -> tuple[NotebookNode, dict[str, Any]]:

        with open(notebook_path, 'r') as f:
            notebook = read(f, as_version=4)

        NotebookClient.__init__(self, notebook, km)
        self.reset_execution_trackers()
        self._check_assign_resources(resources)

        with self.setup_kernel():
            assert self.kc  # noqa
            info_msg = self.wait_for_reply(self.kc.kernel_info())
            assert info_msg  # noqa
            self.nb.metadata["language_info"] = (
                info_msg["content"]["language_info"]
            )
            prefix = '> \033[36m{notebook_name}\033[0m'.format(
                notebook_name=os.path.basename(notebook_path),
            )
            for id, cell in enumerate(progress(self.nb.cells, prefix)):
                self.preprocess_cell(cell, resources, id)
        self.set_widgets_metadata()

        return self.nb, self.resources


def run_notebook(notebook_path: str, timeout: int = -1) -> None:    
    executor = ExecutorWithProgressBar(timeout=timeout, kernel_name='python3')
    executor.run_all_cells(
        notebook_path,
        {'metadata': {'path': '.'}},
    )


if __name__ == '__main__':
    os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

    workflow = load_workflow_yaml(config_dir='tmp.tmp2', notebook_dir='tmp.tmp2')
    
    run_notebook(workflow['test_workflow'][0])