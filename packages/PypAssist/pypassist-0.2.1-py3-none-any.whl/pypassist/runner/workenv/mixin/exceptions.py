#!/usr/bin/env python3
"""
Component mixin exceptions.
"""

from ..component.exceptions import ComponentError


REQUIRE_KWARGS_SIGNATURE = ["export", "output_dir", "exist_ok"]


class InvalidProcessSignatureError(ComponentError):
    """
    Invalid process signature.

    Raise when the required kwargs are not met in the process method.
    """


class InvalidProvideSignatureError(ComponentError):
    """
    Invalid provide signature.
    Raise when the required kwargs are not met in the provide method.
    """


class InvalidConsumeSignatureError(ComponentError):
    """
    Invalid consume signature.
    Raise when the required kwargs are not met in the consume method.
    """
