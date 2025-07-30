#!/usr/bin/env python3
"""
Exportable validation.
"""

from .setup import ExportableSetup


def is_exportable(obj):
    """
    Return True if the given object is a exportable dataclass or an instance
    of a exportable dataclass.
    """
    if isinstance(obj, type):
        dtcls = obj
    else:
        dtcls = type(obj)

    if hasattr(dtcls, "_EXPORT_SETUP_"):
        setup = getattr(dtcls, "_EXPORT_SETUP_")
        if isinstance(setup, ExportableSetup):
            return True
    return False
