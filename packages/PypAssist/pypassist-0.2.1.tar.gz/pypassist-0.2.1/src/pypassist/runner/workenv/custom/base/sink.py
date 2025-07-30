#!/usr/bin/env python3
"""
Base class for custom sink components.
"""

from abc import abstractmethod

from .component import CustomComponent
from ...mixin.sink import SinkMixin


class CustomSink(CustomComponent, SinkMixin):
    """Base class for custom sink components.

    Users should extend this class to create their own custom sinks.
    """

    _REGISTER = {}
    _TYPE_SUBMODULE = None

    def __init__(self, settings, *, workenv=None):
        """Initialize the sink.

        Args:
            settings: Sink settings
        """
        CustomComponent.__init__(self, settings, workenv=workenv)
        SinkMixin.__init__(self)

    @abstractmethod
    def consume(self, **kwargs):
        """Consume with flexible signature.

        Args:
            **kwargs: Arbitrary keyword arguments including:
                - export: Whether to export the results
                - output_dir: Directory to export results to
                - exist_ok: Whether to overwrite existing files

        Returns:
            The result of consuming the data
        """
