#!/usr/bin/env python3
"""
Runner app configuration exceptions.
"""

from ...exceptions import DataclassError


class RunnerError(DataclassError):
    """Base exception for runner application configuration related errors."""


class RunnerAttributeError(RunnerError):
    """Exception for runner application configuration attribute errors."""
