from nbclient import NotebookClient
from nbformat import NotebookNode
from nbformat import read as nb_read
from nbconvert.preprocessors import ExecutePreprocessor
from jupyter_client.manager import KernelManager
import typing as t
from tqdm import tqdm
from bluprint.config import load_workflow_yaml
import os

os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

workflow = load_workflow_yaml(config_dir='tmp.tmp2', notebook_dir='tmp.tmp2')

class NotebookExecutor(ExecutePreprocessor):
      
    def run_all_cells(self, nb: NotebookNode, resources: t.Any = None, km: KernelManager | None = None
    ) -> tuple[NotebookNode, dict[str, t.Any]]:
        NotebookClient.__init__(self, nb, km)
        self.reset_execution_trackers()
        self._check_assign_resources(resources)

        with self.setup_kernel():
            assert self.kc  # noqa
            info_msg = self.wait_for_reply(self.kc.kernel_info())
            assert info_msg  # noqa
            self.nb.metadata["language_info"] = info_msg["content"]["language_info"]
            for index, cell in enumerate(tqdm(self.nb.cells)):
                self.preprocess_cell(cell, resources, index)
        self.set_widgets_metadata()

        return self.nb, self.resources

with open(workflow['test_workflow'][0], 'r') as f:
	notebook = nb_read(f, as_version=4)
     
executor = NotebookExecutor(timeout=-1, kernel_name='python3')
executor.run_all_cells(notebook, {'metadata': {'path': '.'}})
