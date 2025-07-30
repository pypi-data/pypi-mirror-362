#!/usr/bin/env python3
"""
Setup for registry dataclass decorator.
"""

from pydantic.dataclasses import dataclass


@dataclass
class RegistrySetup:
    """Registry Setup."""

    register_name_attr: str = "name"
    settings_attr: str = "settings"
    settings_dataclass_attr: str = "SETTINGS_DATACLASS"
