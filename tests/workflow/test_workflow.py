"""Test workflow execution with progress bar."""

import os
import re

from bluprint.capture_output import capture_stderr
from bluprint.workflow import run_workflow


def test_run_workflow_cli(reference_test_log_file, snapshot):
    fixture_path = 'tests/workflow/fixtures'
    os.environ['JUPYTER_PLATFORM_DIRS'] = '1'
    workflow_log = capture_stderr(
        run_workflow,
        yaml_dir=fixture_path,
        notebook_dir=fixture_path,
    )
    for pattern in (' Elapsed: [0-9:]+', r'\x1b[^m]*m', r'\r'):
        workflow_log = re.sub(pattern, '', workflow_log)

    snapshot.snapshot_dir = os.path.dirname(reference_test_log_file)
    snapshot.assert_match(
        workflow_log,
        reference_test_log_file,
    )
