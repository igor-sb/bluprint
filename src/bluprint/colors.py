"""Color styling for CLI output."""

import functools
import sys
from typing import Callable


class Style(object):
    magenta = '\033[95m'
    blue = '\033[94m'
    blue2 = '\033[34m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    gray = '\033[90m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


def style_workflow(string: str) -> str:
    return f'{Style.magenta}{Style.bold}{string}{Style.end}'


def style_notebook(string: str) -> str:
    return f'{Style.cyan}{Style.bold}{string}{Style.end}'


def bluprint_title() -> str:
    return f'{Style.cyan}{Style.bold}Bluprint{Style.end}'


def bluprint_command(command: str) -> str:
    return '{bluprint}{separator}{command}'.format(
        bluprint=bluprint_title(),
        separator=': ',
        command=command,
    )


def styled_print(
    command: str,
    print_bluprint: bool = True,
    endline: str = '\n',
) -> None:
    if print_bluprint:
        command = bluprint_command(command)
    sys.stderr.write(
        '{command}{endline}'.format(
            command=command,
            endline=endline,
        ),
    )
    sys.stderr.flush()


def progress_log(log_message: str, print_ok=True) -> Callable:
    def decorate(func: Callable) -> Callable:
        @functools.wraps(func)
        def print_wrapper(*args, **kwargs) -> None:
            if print_ok:
                styled_print(log_message, endline='')
            else:
                styled_print(log_message)
            func(*args, **kwargs)
            if print_ok:
                styled_print(' Ok.', print_bluprint=False)
        return print_wrapper
    return decorate
