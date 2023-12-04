"""Exceptions for creating project."""

from bluprint.errors import StyledError


class PythonVersionError(StyledError):
    """Raises exception if python --version fails."""


class PoetryAddError(StyledError):
    """Raises exception if poetry add fails."""


class PoetryInitError(StyledError):
    """Raises exception if poetry init fails."""


class PoetryRunError(StyledError):
    """Raises exception if poetry run fails."""


class PoetryEnvError(StyledError):
    """Raises exception if poetry env fails."""


class RpackageMissingError(StyledError):
    """Raises exception if an R package is not installed in R."""


class RenvInitError(StyledError):
    """Raises exception if renv:init() fails."""


class RenvInstallError(StyledError):
    """Raises exception if renv::install() fails."""
