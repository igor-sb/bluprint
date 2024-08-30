"""Wrapper for binary executables."""

import shutil
import subprocess
from pathlib import Path
from typing import TypeVar

from bluprint.colors import progress_log
from bluprint.create.errors import (
    RenvInitError,
    RenvInstallError,
    RenvSnapshotError,
    UvAddError,
    UvInitError,
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


def uv(
    command: str | list[str],
    exception: type[Error],
    cwd: str | Path,
    **kwargs,
) -> str:
    if isinstance(command, str):
        command = [command]
    return run(['uv', *command], exception, cwd=cwd, **kwargs)


def uv_init(python_version: str, project_dir: str) -> str:
    return uv(
        ['init', '--no-workspace', '--no-readme', '--python', python_version],
        UvInitError,
        cwd=project_dir,
    )


def uv_add(packages: list[str], project_dir: str | Path) -> str:
    return uv(['add', *packages], UvAddError, cwd=project_dir)


def rcmd(rscript: str, exception: type[Error], **kwargs) -> str:
    return run(['Rscript', '-e', rscript], exception, **kwargs)


@progress_log('initalizing renv...')
def renv_init(project_dir: str | Path) -> str:
    return rcmd('renv::init()', RenvInitError, cwd=project_dir)


@progress_log('installing R packages...')
def renv_install(
    packages: str | list[str] | tuple[str, ...],
    project_dir: str | Path,
) -> str:
    if isinstance(packages, str):
        packages = [packages]
    return rcmd(
        'renv::install(c("{packages_str}"), prompt=FALSE)'.format(
            packages_str='", "'.join(packages),
        ),
        RenvInstallError,
        cwd=project_dir,
    )


@progress_log('creating renv snapshot...')
def renv_create_snapshot(project_dir: str | Path) -> None:
    rcmd('renv::snapshot()', RenvSnapshotError, cwd=project_dir)
