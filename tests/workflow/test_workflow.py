"""Test workflow execution with progress bar."""

import os
import re
import sys
from io import StringIO
from pathlib import Path

import pytest

from bluprint.cli import Bluprint
from bluprint.workflow import InvalidWorkflowError, run_workflows


def capture_stderr(func, *args, **kwargs):
    buffer = StringIO()
    original_stderr = sys.stderr

    try:  # noqa: WPS501, WPS229
        sys.stderr = buffer
        func(*args, **kwargs)
        return buffer.getvalue()  # noqa: WPS331

    finally:
        sys.stderr = original_stderr


def test_run_workflows(reference_test_log_file, snapshot):
    fixture_path = 'tests/workflow/fixtures'
    os.environ['JUPYTER_PLATFORM_DIRS'] = '1'
    workflow_log = capture_stderr(
        run_workflows,
        workflow_yaml_dir=fixture_path,
        notebook_dir=fixture_path,
    )
    for pattern in (' Elapsed: [0-9:]+', r'\x1b[^m]*m', r'\r'):
        workflow_log = re.sub(pattern, '', workflow_log)

    snapshot.snapshot_dir = os.path.dirname(reference_test_log_file)
    snapshot.assert_match(
        workflow_log,
        reference_test_log_file,
    )


def test_run_workflow_cli(
    reference_xtest_log_file,
    snapshot,
):
    fixture_path = 'tests/workflow/fixtures'
    os.environ['JUPYTER_PLATFORM_DIRS'] = '1'
    bp = Bluprint()
    workflow_log = capture_stderr(
        bp.workflow,
        workflow_name='xtest_workflow',
        workflow_yaml=Path(fixture_path) / 'workflows.yaml',
        notebook_dir=fixture_path,
    )
    for pattern in (' Elapsed: [0-9:]+', r'\x1b[^m]*m', r'\r'):
        workflow_log = re.sub(pattern, '', workflow_log)

    snapshot.snapshot_dir = os.path.dirname(reference_xtest_log_file)
    snapshot.assert_match(
        workflow_log,
        reference_xtest_log_file,
    )


def test_invalid_workflow():
    with pytest.raises(InvalidWorkflowError):
        fixture_path = 'tests/workflow/fixtures'
        os.environ['JUPYTER_PLATFORM_DIRS'] = '1'
        bp = Bluprint()
        bp.workflow(
            workflow_name='fake_workflow',
            workflow_yaml=Path(fixture_path) / 'workflows.yaml',
            notebook_dir=fixture_path,
        )
