#!/usr/bin/env python3
"""
Viewer validation.
"""

from .setup import ViewerSetup


def is_viewer(obj):
    """
    Return True if the given object is a viewer dataclass or an instance
    of a viewer dataclass.
    """
    dataclass_type = type(obj)
    if hasattr(dataclass_type, "_SETUP_"):
        setup = getattr(dataclass_type, "_SETUP_")
        if isinstance(setup, ViewerSetup):
            return True
    return False
