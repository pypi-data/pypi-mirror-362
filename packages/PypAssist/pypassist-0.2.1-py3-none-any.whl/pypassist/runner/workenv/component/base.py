#!/usr/bin/env python3
"""
Base component protocol for workflow module.
"""

from ....fallback.protocol import Protocol, runtime_checkable


@runtime_checkable
class WorkflowComponent(Protocol):
    """Protocol defining the interface for all workflow components."""

    def get_assetable_func(self):
        """Get function that can be converted to a dagster asset.

        Returns:
            Callable: A function that can be used as a dagster asset
        """
