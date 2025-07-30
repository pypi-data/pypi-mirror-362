#!/usr/bin/env python3
"""
Setup for viewer dataclass decorator.
"""

from dataclasses import dataclass


@dataclass
class ViewerSetup:
    """Setup for viewer decorator."""

    hide_private: bool = True
