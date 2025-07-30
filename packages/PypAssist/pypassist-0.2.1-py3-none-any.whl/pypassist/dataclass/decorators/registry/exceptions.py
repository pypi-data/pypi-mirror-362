#!/usr/bin/env python3
"""
Registry exceptions.
"""

from ...exceptions import DataclassError


class RegistryError(DataclassError):
    """Base exception for all Registry related errors."""


class RegistrySetupError(RegistryError):
    """Raised when there is an error in the Registry setup configuration."""


class RegistrationErrror(RegistryError):
    """Raised when there is an error during type registration."""


class RegistryAttributeError(RegistryError):
    """Raised when there is an error during validation of attributes."""
