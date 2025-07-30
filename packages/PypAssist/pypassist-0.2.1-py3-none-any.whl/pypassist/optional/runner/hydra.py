#!/usr/bin/env python3
"""Optional Hydra imports."""

from .exceptions import RunnerDependencyError

try:
    from hydra import main as hydra_main
except ImportError as err:
    raise RunnerDependencyError("omegaconf") from err


__all__ = ["hydra_main"]
