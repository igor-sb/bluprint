"""Test workflow execution with progress bar."""

import logging
import subprocess
import os
import tempfile
from pathlib import Path
from contextlib import redirect_stderr

from bluprint.workflow import run_workflow


def test_run_workflow_cli():
    fixture_path = 'tests/workflow/fixtures'
    with tempfile.NamedTemporaryFile(delete=False) as log, redirect_stderr(log):
        print(f'Log file: {log.name}')
        
        run_workflow(yaml_dir=fixture_path, notebook_dir=fixture_path)
        