#!/usr/bin/env python3
"""
Base formatter.
"""

from abc import ABC, abstractmethod

from ...mixin.registrable import Registrable
from ...mixin.settings import SettingsMixin


class Formatter(ABC, Registrable, SettingsMixin):
    """Base formatter."""

    _REGISTER = {}
    _TYPE_SUBMODULE = "type"

    def __init__(self, settings):
        Registrable.__init__(self)
        SettingsMixin.__init__(self, settings)

    @abstractmethod
    def to_str(self, class_info):
        """Format the class information."""

    @abstractmethod
    def display(self, content):
        """Display the formatted content."""

    @abstractmethod
    def to_serialized(self, class_info):
        """Convert DataclassInfo to a serialized object."""
