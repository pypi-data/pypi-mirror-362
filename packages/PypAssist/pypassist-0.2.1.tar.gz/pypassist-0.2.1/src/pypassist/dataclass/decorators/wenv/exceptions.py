#!/usr/bin/env python3
"""
Working environment exceptions.
"""

from ...exceptions import DataclassError


class WenvError(DataclassError):
    """Base exception for work environment related errors."""


class WenvSetupError(WenvError):
    """Exception for work environment setup errors."""
