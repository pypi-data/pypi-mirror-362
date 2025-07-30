#!/usr/bin/env python3
"""
Base class for custom workflow components.
"""

from abc import ABC, abstractmethod

from .....mixin.registrable import Registrable
from .....mixin.settings import SettingsMixin


class CustomComponent(ABC, Registrable, SettingsMixin):
    """Base class for all custom components.

    This is the base class that users should extend to create their own
    custom workflow components. It provides registration and settings functionality.
    """

    def __init__(self, settings, *, workenv):
        """Initialize the component.

        Args:
            settings: Component settings
        """
        Registrable.__init__(self)
        SettingsMixin.__init__(self, settings)
        self._workenv = workenv

    @classmethod
    @abstractmethod
    def init_from_config(cls, config, workenv=None):
        """Initialize the component from configuration.

        Args:
            config: Component configuration
            workenv: Optional work environment instance

        Returns:
            An instance of the component
        """
