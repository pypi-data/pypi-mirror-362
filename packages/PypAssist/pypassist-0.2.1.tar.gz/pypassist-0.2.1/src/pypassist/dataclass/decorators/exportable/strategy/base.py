#!/usr/bin/env python3
"""
Base export strategy.
"""

from abc import ABC, abstractmethod

from .....mixin.registrable import Registrable


class ExportStrategy(ABC, Registrable):
    """Base export strategy."""

    _REGISTER = {}
    _TYPE_SUBMODULE = "type"

    # pylint: disable=R0913
    @classmethod
    @abstractmethod
    def export(
        cls,
        data_cls,
        output_dir,
        format_type="yaml",
        exist_ok=False,
        makedirs=True,
        **kwargs,
    ):
        """Export the configuration.

        Args:
            cls: The class to export
            output_dir: Output directory
            format_type: Output format (yaml, json, etc.)
            exist_ok: Overwrite existing files
            makedirs: Create missing directories
            **kwargs: Additional formatting options
        """
