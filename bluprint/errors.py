"""List of all errors used within bluprint."""

from dataclasses import dataclass

from bluprint.colors import Style


@dataclass
class StyledError(Exception):
    """Highlighted error message in Python error dump."""
    message: str = ''

    def __str__(self):
        return f'{Style.red}{self.message}{Style.end}'
    

class MissingExecutableError(StyledError):
    """Raises an exception if a required executable is missing."""


class InvalidWorkflowError(StyledError):
    """Raises exception when invalid workflow is specified."""


class InvalidNotebookTypeError(StyledError):
    """Raises exception when invalid notebook type is specified."""


class RpackageMissingError(StyledError):
    """Raise this exception if an R package is not installed in R."""
