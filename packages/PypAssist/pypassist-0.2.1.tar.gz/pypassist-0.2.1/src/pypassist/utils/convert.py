#!/usr/bin/env python3
"""Convert Utility functions."""

from collections import OrderedDict
from collections.abc import Iterable


def to_dict_recursive(obj):
    """Convert any object containing OrderedDict to standard dict recursively.

    This function handles nested data structures and converts OrderedDict
    to standard dict while preserving the order of keys. It can process:
    - OrderedDict
    - dict
    - list
    - tuple
    - any other type (returned as is)

    Args:
        obj: The object to convert, can be of any type

    Returns:
        The converted object with all OrderedDict replaced by standard dict

    Examples:
        >>> data = OrderedDict([('a', 1), ('b', OrderedDict([('c', 2)]))])
        >>> result = to_dict_recursive(data)
        >>> isinstance(result, dict)
        True
        >>> isinstance(result['b'], dict)
        True
    """
    if isinstance(obj, (OrderedDict, dict)):
        return {key: to_dict_recursive(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [to_dict_recursive(item) for item in obj]
    if isinstance(obj, tuple):
        return tuple(to_dict_recursive(item) for item in obj)
    return obj


def ensure_list(obj):
    """
    Ensures that the input is returned as a list.

    - If the input is already a list, it is returned unchanged.
    - If the input is an iterable (e.g., tuple, set, numpy array), it is converted to a list.
    - If the input is a scalar or a string/bytes, it is wrapped in a single-element list.

    Args:
        obj (Any): The object to convert to a list.

    Returns:
        List: A list version of the input object.
    """
    if isinstance(obj, list):
        return obj
    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        return list(obj)
    return [obj]
