#!/usr/bin/env python3
"""Optional Dagster imports."""

from .exceptions import RunnerDependencyError

try:
    from dagster import (
        asset,
        AssetIn,
        Definitions,
        define_asset_job,
        mem_io_manager,
    )
except ImportError as err:
    raise RunnerDependencyError("dagster") from err


__all__ = [
    "asset",
    "AssetIn",
    "Definitions",
    "define_asset_job",
    "mem_io_manager",
]
