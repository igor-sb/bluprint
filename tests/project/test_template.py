"""Test template operations."""

import os
import tempfile
from pathlib import Path

from bluprint.template import delete_r_examples_from_project


def test_delete_r_examples_from_project():
    with tempfile.TemporaryDirectory() as project_dir:
        notebook_dir = Path(project_dir) / 'notebooks'
        os.mkdir(notebook_dir)
        example_rmarkdown = notebook_dir / 'example_rmarkdown.Rmd'
        open(example_rmarkdown, 'w').close()
        delete_r_examples_from_project(project_dir)
        assert not example_rmarkdown.exists()

