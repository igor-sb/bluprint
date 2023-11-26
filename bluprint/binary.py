"""Wrapper for binary executables."""

import shutil


class MissingExecutableError(Exception):
    """Raises an exception if a required executable is missing."""


def check_if_executable_is_installed(executable: str) -> None:
    if not shutil.which(executable):
        raise MissingExecutableError(f'{executable} not found.')
