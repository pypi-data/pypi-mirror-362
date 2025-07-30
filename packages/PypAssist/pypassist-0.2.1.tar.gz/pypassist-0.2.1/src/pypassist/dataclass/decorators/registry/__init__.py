#!/usr/bin/env python3
"""Registry decorator package."""

from .decorator import registry
from .setup import RegistrySetup
from .exceptions import RegistrySetupError

__all__ = ["registry", "RegistrySetup", "RegistrySetupError"]
