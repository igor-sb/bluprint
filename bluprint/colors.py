"""Color styling for CLI output."""


class Style(object):
    magenta = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


def style_workflow(string: str) -> str:
    return f'{Style.magenta}{Style.bold}{string}{Style.end}'


def style_notebook(string: str) -> str:
    return f'{Style.cyan}{Style.bold}{string}{Style.end}'
