#!/usr/bin/env python3
"""Viewer decorator package."""

from .decorator import viewer
from .setup import ViewerSetup
from .exceptions import ViewerSetupError

__all__ = ["viewer", "ViewerSetup", "ViewerSetupError"]
