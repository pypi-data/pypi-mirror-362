#!/usr/bin/env python3
"""
Configuration for custom sinks.
"""

from pydantic.dataclasses import dataclass

from .....dataclass.decorators.registry.decorator import registry
from .....dataclass.decorators.exportable.decorator import exportable

from ..base.sink import CustomSink
from .base import CustomConfig


@registry(base_cls=CustomSink)
@exportable(strategy="registry")
@dataclass
class CustomSinkConfig(CustomConfig):
    """Custom sink configuration."""
