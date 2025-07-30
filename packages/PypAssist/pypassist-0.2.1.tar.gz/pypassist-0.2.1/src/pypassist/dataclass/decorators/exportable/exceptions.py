#!/usr/bin/env python3
"""
Exportable exceptions.
"""


from ...exceptions import DataclassError


class ExportableError(DataclassError):
    """Base exception for exportable decorator."""


class ExportableSetupError(ExportableError):
    """Raised when there is an error in the Exportable setup configuration."""
