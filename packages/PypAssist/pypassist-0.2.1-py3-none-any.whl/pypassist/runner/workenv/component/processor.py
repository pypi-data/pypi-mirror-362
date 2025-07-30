#!/usr/bin/env python3
"""
Processor component protocol for workflow module.
"""

from .base import WorkflowComponent
from ....fallback.protocol import runtime_checkable, Protocol


@runtime_checkable
class ProcessorComponent(WorkflowComponent, Protocol):
    """Protocol for components that process input data."""

    def process(self, **kwargs):
        """Process input data with flexible signature.

        All implementations should support these keyword arguments:
            export (bool): Whether to export the results
            output_dir (str): Directory to export results to
            exist_ok (bool): Whether to overwrite existing files

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            Any: The processed data
        """
