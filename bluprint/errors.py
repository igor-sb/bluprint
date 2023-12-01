"""List of all errors used within bluprint."""  # noqa: WPS202

from dataclasses import dataclass

from bluprint.colors import Style


@dataclass
class StyledError(Exception):
    """Highlighted error message in Python error dump."""

    message: str = ''

    def __str__(self):
        """Error message formatting."""
        return f'{Style.red}{self.message}{Style.end}'


class MissingExecutableError(StyledError):
    """Raises an exception if a required executable is missing."""


class ProjectExistsError(StyledError):
    """Raises exception when project directory exists."""


class InvalidWorkflowError(StyledError):
    """Raises exception when invalid workflow is specified."""


class InvalidNotebookTypeError(StyledError):
    """Raises exception when invalid notebook type is specified."""
