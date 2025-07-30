#!/usr/bin/env python3
"""Runner application configuration decorator package."""

from .decorator import runner
from .exceptions import RunnerAttributeError

__all__ = ["runner", "RunnerAttributeError"]
