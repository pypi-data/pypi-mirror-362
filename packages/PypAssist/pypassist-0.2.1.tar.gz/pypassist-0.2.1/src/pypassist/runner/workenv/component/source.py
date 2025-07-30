#!/usr/bin/env python3
"""
Source component protocol for workflow module.
"""

from .base import WorkflowComponent
from ....fallback.protocol import runtime_checkable, Protocol


@runtime_checkable
class SourceComponent(WorkflowComponent, Protocol):
    """Protocol for components that provide data."""

    def provide(self, **kwargs):
        """Provide input data with flexible signature.

        All implementations should support these keyword arguments:
            export (bool): Whether to export the results
            output_dir (str): Directory to export results to
            exist_ok (bool): Whether to overwrite existing files

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            Any: The provided data
        """
