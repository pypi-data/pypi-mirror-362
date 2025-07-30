#!/usr/bin/env python3
"""Runner-specific optional dependency errors."""

from ..exceptions import BaseOptionalDependencyError


class RunnerDependencyError(BaseOptionalDependencyError):
    """Error raised when a Runner-related optional dependency is missing."""

    def __init__(self, package_name: str):
        super().__init__(package_name, extra_name="runner")
