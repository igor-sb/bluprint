"""Test code for external binary executables."""

import pytest

from bluprint.binary import (
    MissingExecutableError,
    check_if_executable_is_installed,
)


def test_invalid_workflow():
    with pytest.raises(MissingExecutableError):
        check_if_executable_is_installed('fake_executable')
