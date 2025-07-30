#!/usr/bin/env python3
# pylint: disable=too-few-public-methods
"""
Viewer exceptions.
"""


from ...exceptions import DataclassError


class ViewerError(DataclassError):
    """Base exception for viewer decorator."""


class ViewerSetupError(ViewerError):
    """Raised when there is an error in the Viewer setup configuration."""


class ViewerFormattingError(ViewerError):
    """Raised when there is an error during formatting operations."""
