"""Wrapper for binary executables."""

import shutil
import subprocess
from typing import TypeVar

from bluprint.errors import MissingExecutableError, StyledError

Error = TypeVar('Error', bound=StyledError)


def check_if_executable_is_installed(executable: str) -> None:
    if not shutil.which(executable):
        raise MissingExecutableError(f'{executable} not found.')


def run(command: list[str], exception: type[Error], **kwargs) -> str:
    command_out = subprocess.run(command, capture_output=True, **kwargs)
    if command_out.returncode == 1:
        raise exception(command_out.stderr.decode('utf-8'))
    return command_out.stdout.decode('utf-8')


def poetry(command: str | list[str], exception: type[Error], **kwargs):
    if isinstance(command, str):
        command = [command]
    return run(['poetry', *command], exception, **kwargs)


def rcmd(command: str | list[str], exception: type[Error], **kwargs):
    if isinstance(command, str):
        command = [command]
    return run(['Rscript', '-e', *command], exception, **kwargs)
