#!/usr/bin/env python3
"""
Base class for custom source components.
"""

from abc import abstractmethod

from .component import CustomComponent
from ...mixin.source import SourceMixin


class CustomSource(CustomComponent, SourceMixin):
    """Base class for custom source components.

    Users should extend this class to create their own custom sources.
    """

    _REGISTER = {}
    _TYPE_SUBMODULE = None

    def __init__(self, settings, *, workenv=None):
        """Initialize the source.

        Args:
            settings: Source settings
        """
        CustomComponent.__init__(self, settings, workenv=workenv)
        SourceMixin.__init__(self)

    @abstractmethod
    def provide(self, **kwargs):
        """Provide with flexible signature.

        Args:
            **kwargs: Arbitrary keyword arguments including:
                - export: Whether to export the results
                - output_dir: Directory to export results to
                - exist_ok: Whether to overwrite existing files

        Returns:
            The provided data
        """
