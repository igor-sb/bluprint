"""List of all errors used within bluprint."""

from dataclasses import dataclass

from bluprint.colors import Style


@dataclass
class StyledError(Exception):
    """Highlighted error message in Python error dump."""

    def __init__(self, message: str = ''):
        self.message = message

    def __str__(self):
        """Error message formatting."""
        return f'{Style.red}{self.message}{Style.end}'


class MissingExecutableError(StyledError):
    """Raises an exception if a required executable is missing."""


class ProjectExistsError(StyledError):
    """Raises exception when project directory exists."""


class InvalidNotebookTypeError(StyledError):
    """Raises exception when invalid notebook type is specified."""


class InvalidProjectNameError(StyledError):
    """Raises exception when user provides invalid project name."""
