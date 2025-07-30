#!/usr/bin/env python3
"""Fallback for typing.Protocol."""


class DummyProtocol:
    """
    A dummy implementation to replace typing.Protocol for Python 3.7 compatibility.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)


def runtime_checkable(cls):
    """
    A dummy decorator to mimic typing.runtime_checkable.
    """
    return cls


# Fallback mechanism
try:
    from typing import Protocol, runtime_checkable  # pylint: disable=unused-import
except ImportError:
    Protocol = DummyProtocol
    # runtime_checkable already defined above
