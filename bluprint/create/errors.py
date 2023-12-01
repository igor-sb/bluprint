"""Exceptions for creating project."""

from bluprint.errors import StyledError


class PoetryAddError(StyledError):
    """Raises exception if poetry add fails."""


class RpackageMissingError(StyledError):
    """Raises exception if an R package is not installed in R."""


class RenvInitError(StyledError):
    """Raises exception if renv:init() fails."""
