"""Wrapper for binary executables."""

import shutil
import subprocess  # noqa: S404
from dataclasses import dataclass


@dataclass
class Executable(object):
    args: list[str]

    def run(self) -> str:
        check_if_executable_is_installed(self.args[0])
        out = subprocess.run(self.args, capture_output=True)  # noqa: S603
        if out.stderr != b'':
            raise RuntimeError(out.stderr.decode('UTF-8'))
        return out.stdout.decode('UTF-8')


def check_if_executable_is_installed(executable: str) -> None:
    if not shutil.which(executable):
        raise ValueError(f'Executable not found: {executable}')
