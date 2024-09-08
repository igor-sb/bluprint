"""Test bluprint version command."""

import io
import re
import tomllib
from contextlib import redirect_stderr
from pathlib import Path

from bluprint import cli


def test_pyproject_version_matches_output():
    with Path('pyproject.toml').open('rb') as pyproject_toml_file:
        pyproject_toml = tomllib.load(pyproject_toml_file)
    cli_out = io.StringIO()
    with redirect_stderr(cli_out):
        cli.Bluprint().version()
    cli_version = re.sub(r'^.*version (.*)$', r'\1', cli_out.getvalue().strip())
    assert pyproject_toml['project']['version'] == cli_version
