#!/usr/bin/env python3
"""
Component exceptions
"""

from ...exceptions import RunnerError


class ComponentError(RunnerError):
    """Base component error."""


class InvalidComponentError(ComponentError):
    """Invalid component."""
