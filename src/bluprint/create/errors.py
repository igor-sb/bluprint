"""Exceptions for creating project."""

from bluprint.errors import StyledError


class PythonVersionError(StyledError):
    """Raises exception if python --version fails."""


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
