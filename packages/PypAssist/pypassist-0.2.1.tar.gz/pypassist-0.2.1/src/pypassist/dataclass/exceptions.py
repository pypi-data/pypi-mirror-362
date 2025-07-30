#!/usr/bin/env python3
"""
Common exceptions for dataclass decorators.
"""

from ..exceptions import PypassistError


class DataclassError(PypassistError):
    """Base exception for all dataclass-related errors."""


class FormattingError(DataclassError):
    """Exception for formatting-related errors."""
