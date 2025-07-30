#!/usr/bin/env python3
"""Base exceptions for optional dependencies."""

import inspect
import importlib.metadata


class BaseOptionalDependencyError(ImportError):
    """Base class for optional dependency errors."""

    @staticmethod
    def _find_caller_package():
        """Determine the package that triggered the import."""
        for frame in inspect.stack():
            module = inspect.getmodule(frame[0])
            if module and not module.__name__.startswith("pypassist"):
                try:
                    package_name = module.__name__.split(".")[0]
                    importlib.metadata.metadata(package_name)
                    return package_name
                except importlib.metadata.PackageNotFoundError:
                    continue
        return "pypassist"

    def __init__(self, package_name: str, extra_name: str):
        self.missing_package = package_name
        self.extra_name = extra_name
        parent_package = self._find_caller_package()

        message = (
            f"{package_name} is not installed. Install {parent_package}[{extra_name}] "
            f"to use {package_name}-based features: pip install {parent_package}[{extra_name}]"
        )
        super().__init__(message)
