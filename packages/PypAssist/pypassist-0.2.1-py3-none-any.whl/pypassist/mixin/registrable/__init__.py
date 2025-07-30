#!/usr/bin/env python3
"""
Registrable mixin module for automatic class registration capabilities.
"""

from .mixin import Registrable
from .exceptions import UnregisteredTypeError

__all__ = [
    "Registrable",
    "UnregisteredTypeError",
]
