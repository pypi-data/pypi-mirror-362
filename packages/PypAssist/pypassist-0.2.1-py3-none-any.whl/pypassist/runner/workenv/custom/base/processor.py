#!/usr/bin/env python3
"""
Base class for custom processor components.
"""

from abc import abstractmethod

from .component import CustomComponent
from ...mixin.processor import ProcessorMixin


class CustomProcessor(CustomComponent, ProcessorMixin):
    """Base class for custom processor components.

    Users should extend this class to create their own custom processors.
    """

    _REGISTER = {}
    _TYPE_SUBMODULE = None

    def __init__(self, settings, *, workenv=None):
        """Initialize the processor.

        Args:
            settings: Processor settings
        """
        CustomComponent.__init__(self, settings, workenv=workenv)
        ProcessorMixin.__init__(self)

    @abstractmethod
    def process(self, **kwargs):
        """Process with flexible signature.

        Args:
            **kwargs: Arbitrary keyword arguments including:
                - export: Whether to export the results
                - output_dir: Directory to export results to
                - exist_ok: Whether to overwrite existing files

        Returns:
            The processed data
        """
