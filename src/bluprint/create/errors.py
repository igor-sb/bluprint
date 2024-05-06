"""Exceptions for creating project."""

from bluprint.errors import StyledError


class PythonVersionError(StyledError):
    """Raises exception if python --version fails."""


class LowPythonVersionError(StyledError):
    """Raises exception if user-provided Python version is < 3.11."""


class PdmAddError(StyledError):
    """Raises exception if PDM add fails."""


class PdmInitError(StyledError):
    """Raises exception if PDM init fails."""


class RpackageMissingError(StyledError):
    """Raises exception if an R package is not installed in R."""


class RenvInitError(StyledError):
    """Raises exception if renv:init() fails."""


class RenvInstallError(StyledError):
    """Raises exception if renv::install() fails."""


class RenvSnapshotError(StyledError):
    """Raises exception if renv::snapshot() fails."""


class GitError(StyledError):
    """Raises exception if git config --global user.name errors out."""
