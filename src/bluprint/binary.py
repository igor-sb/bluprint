"""Wrapper for binary executables."""

import shutil
import subprocess
from pathlib import Path
from typing import TypeVar

from bluprint.create.errors import (
    PdmAddError,
    PdmInitError,
    RenvInitError,
    RenvInstallError,
)
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


def pdm(
    command: str | list[str],
    exception: type[Error],
    cwd: str | Path,
    **kwargs,
) -> str:
    if isinstance(command, str):
        command = [command]
    return run(['pdm', *command], exception, cwd=cwd, **kwargs)


def pdm_init(python_version: str, template_dir: str, project_dir: str) -> str:
    return pdm(
        ['init', '--lib', '-n', '--python', python_version, template_dir],
        PdmInitError,
        cwd=project_dir,
    )


def pdm_add(packages: list[str], project_dir: str | Path) -> str:
    return pdm(['add', *packages], PdmAddError, cwd=project_dir)


def rcmd(rscript: str, exception: type[Error], **kwargs) -> str:
    return run(['Rscript', '-e', rscript], exception, **kwargs)


def renv_init(project_dir: str | Path) -> str:
    return rcmd('renv::init()', RenvInitError, cwd=project_dir)


def renv_install(packages: str | list[str], project_dir: str | Path) -> str:
    if isinstance(packages, str):
        packages = [packages]
    return rcmd(
        'renv::install(c("{packages_str}"))'.format(
            packages_str='", "'.join(packages),
        ),
        RenvInstallError,
        cwd=project_dir,
    )
