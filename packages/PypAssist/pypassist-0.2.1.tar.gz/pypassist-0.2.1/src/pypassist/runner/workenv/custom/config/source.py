#!/usr/bin/env python3
"""
Configuration for custom sources.
"""

from pydantic.dataclasses import dataclass

from .....dataclass.decorators.registry.decorator import registry
from .....dataclass.decorators.exportable.decorator import exportable

from ..base.source import CustomSource
from .base import CustomConfig


@registry(base_cls=CustomSource)
@exportable(strategy="registry")
@dataclass
class CustomSourceConfig(CustomConfig):
    """Custom source configuration."""
