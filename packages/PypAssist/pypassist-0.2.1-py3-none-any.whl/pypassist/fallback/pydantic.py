#!/usr/bin/env python3
"""Fallback for pydantic."""

from dataclasses import is_dataclass


def is_pydantic_dataclass(cls):
    """
    Check if a class has been decorated with @pydantic.dataclasses.dataclass.

    Args:
        cls: The class to check

    Returns:
        bool: True if the class uses the pydantic.dataclasses.dataclass decorator
    """
    if not is_dataclass(cls):
        return False

    # Check for Pydantic v1 specific attributes
    if hasattr(cls, "__pydantic_model__"):
        return True

    # Check for Pydantic v2 specific attributes
    if hasattr(cls, "__pydantic_core_schema__"):
        return True

    # Check if any of the class attributes start with "__pydantic_"
    for attr in dir(cls):
        if attr.startswith("__pydantic_"):
            return True

    # If no Pydantic marker is found, it's a standard dataclass
    return False
