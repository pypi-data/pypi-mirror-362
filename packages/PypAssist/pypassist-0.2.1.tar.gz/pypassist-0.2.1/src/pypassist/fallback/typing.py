#!/usr/bin/env python3
# pylint: disable=import-self
"""
Typing functions for retrocompatibility with older Python versions.
"""
import logging
import sys
from typing import Generic, _GenericAlias

LOGGER = logging.getLogger(__name__)

if sys.version_info >= (3, 9):
    Dict = dict
    List = list
else:
    LOGGER.debug("Using and old definition of Dict")
    from typing import Dict, List


def _log_definition(name, err):
    """
    Load the definition of a function.

    Args:
        name:
            The name of the function begin defined.

        err:
            The import error.
    """
    LOGGER.debug(
        'Defining a simplified version of the function "%s" because'
        "the typing package provided by Python %s does not define it: %s",
        name,
        sys.version,
        err,
    )


try:
    from typing import get_origin
except ImportError as err:
    _log_definition("get_origin", err)

    # https://github.com/python/cpython/blob/6586b171ea842151c24d2228d06a69d2fecaf29f/Lib/typing.py
    def get_origin(tp):
        """
        Simplified version of typing.get_origin() as defined in Python 3.12 for
        older version of Python.
        """
        if tp is Generic:
            return Generic
        return getattr(tp, "__origin__", None)


try:
    from typing import get_args
except ImportError as err:
    _log_definition("get_args", err)

    import collections.abc

    # https://github.com/python/cpython/blob/6586b171ea842151c24d2228d06a69d2fecaf29f/Lib/typing.py

    def _is_param_expr(arg):
        """
        Simplified implementation of typing._is_param_expr from Python 3.12.
        """
        return arg is ... or isinstance(arg, (tuple, list))

    def _should_unflatten_callable_args(typ, args):
        """
        Implementation of typing._should_unflatten_callable_args from Python 3.12.
        """
        return typ.__origin__ is collections.abc.Callable and not (
            len(args) == 2 and _is_param_expr(args[0])
        )

    def get_args(tp):
        """
        Simplified version of typing.get_args() as defined in Python 3.12 for
        older version of Python.
        """
        try:
            return (tp.__origin__,) + tp.__metadata__
        except AttributeError:
            pass
        if isinstance(tp, _GenericAlias):
            res = tp.__args__
            if _should_unflatten_callable_args(tp, res):
                res = (list(res[:-1]), res[-1])
            return res

        return getattr(tp, "__args__", ())


def type_matches_annotation(value, annotation):
    """
    Check if the type of a value matches an annotation. This function will catch
    TypeErrors raised by older versions of Python and use a workaround.

    Args:
        value:
            The value to check.

        annotation:
            The matching annotation.

    Returns:
        True if the type matches the annotation, else False.
    """
    try:
        return isinstance(value, annotation)
    except TypeError:
        args = get_args(annotation)
        return isinstance(value, args)


NoneType = type(None)


__all__ = [
    "Dict",
    "List",
    "get_args",
    "get_origin",
    "type_matches_annotation",
    "NoneType",
]
