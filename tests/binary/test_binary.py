"""Test code for external binary executables."""

import re
import shutil

import pytest

from bluprint.binary import (
    MissingExecutableError,
    check_if_executable_is_installed,
    uv,
)


def test_missing_executable():
    with pytest.raises(MissingExecutableError):
        check_if_executable_is_installed('fake_executable')


def test_if_uv_is_installed():
    assert bool(shutil.which('uv'))


def test_uv_command_passed_as_string():
    uv_version = uv('version', MissingExecutableError, '.').strip()
    assert re.match(r'^uv [0-9]+\.[0-9]+\.[0-9]+$', uv_version)
