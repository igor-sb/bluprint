"""Wrapper for binary executables."""

import shutil
import sys


def check_if_executable_is_installed(executable: str) -> None:
    if not shutil.which(executable):
        raise ValueError(f'Executable not found: {executable}')
    sys.stderr.write(f'{executable} is installed. ✓\n')
