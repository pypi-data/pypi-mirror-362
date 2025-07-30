#!/usr/bin/env python3
"""
Configuration for custom processors.
"""

from pydantic.dataclasses import dataclass

from .....dataclass.decorators.registry.decorator import registry
from .....dataclass.decorators.exportable.decorator import exportable

from ..base.processor import CustomProcessor
from .base import CustomConfig


@registry(base_cls=CustomProcessor)
@exportable(strategy="registry")
@dataclass
class CustomProcessorConfig(CustomConfig):
    """Custom processor configuration."""
