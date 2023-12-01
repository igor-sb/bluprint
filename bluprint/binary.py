"""Wrapper for binary executables."""

import shutil

from bluprint.errors import MissingExecutableError


def check_if_executable_is_installed(executable: str) -> None:
    if not shutil.which(executable):
        raise MissingExecutableError(f'{executable} not found.')
