#!/usr/bin/env python3
"""
Setup for registry dataclass decorator.
"""

from pydantic.dataclasses import dataclass


@dataclass
class WenvSetup:
    """Setup for wenv decorator."""
