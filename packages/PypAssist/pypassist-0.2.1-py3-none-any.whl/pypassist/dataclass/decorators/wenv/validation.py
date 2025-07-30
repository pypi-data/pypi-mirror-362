#!/usr/bin/env python3
"""
Dataclass validation.
"""

from .setup import WenvSetup


def is_wenv(obj):
    """
    Return True if the given object is a wenv dataclass or an instance
    of a wenv dataclass.
    """
    if isinstance(obj, type):
        dtcls = obj
    else:
        dtcls = type(obj)
    if hasattr(dtcls, "_SETUP_"):
        setup = getattr(dtcls, "_SETUP_")
        if isinstance(setup, WenvSetup):
            return True
    return False
