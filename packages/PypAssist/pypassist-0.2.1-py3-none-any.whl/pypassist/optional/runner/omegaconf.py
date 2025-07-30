#!/usr/bin/env python3
"""Optional OmegaConf imports."""

from .exceptions import RunnerDependencyError

try:
    from omegaconf import OmegaConf
except ImportError as err:
    raise RunnerDependencyError("omegaconf") from err

__all__ = ["OmegaConf"]
