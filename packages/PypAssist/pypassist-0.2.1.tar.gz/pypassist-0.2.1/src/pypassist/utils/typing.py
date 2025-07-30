#!/usr/bin/env python3
"""
Type utility functions.
"""

from typing import Union, Any

from ..fallback.typing import get_args, Dict


def type_to_string(type_obj):
    """Converts a Python type to its string representation.

    Args:
        type_obj: Type object to convert.

    Returns:
        str: String representation of the type.

    Note:
        Handles special cases like Union types and types with __origin__.
    """
    if hasattr(type_obj, "__origin__"):
        if type_obj.__origin__ is Union:
            formatted_args = [type_to_string(arg) for arg in get_args(type_obj)]
            return f"Union[{', '.join(formatted_args)}]"
        formatted_args = [type_to_string(arg) for arg in get_args(type_obj)]
        return f"{type_obj.__origin__.__name__}[{', '.join(formatted_args)}]"
    try:
        return type_obj.__name__
    except AttributeError:
        return str(type_obj)


# Alias for typing dict that will be converted to Param dataclass
ParamDict = Dict[str, Any]
