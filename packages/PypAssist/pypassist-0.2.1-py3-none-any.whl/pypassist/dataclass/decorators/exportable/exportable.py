#!/usr/bin/env python3
"""
Base class for exportable dataclass.
"""

import logging

from ...format.info import DataclassInfo
from ...format.base import Formatter
from .strategy.base import ExportStrategy

LOGGER = logging.getLogger(__name__)


class ExportableMixin:
    """Mixin class for exportable dataclass.

    This class provides the core functionality for exporting dataclass schemas
    to various formats using different export strategies.
    """

    _EXPORT_SETUP_ = None
    _EXPORTABLE_ = True

    @classmethod
    def to_schema_info(cls):
        """Convert the class definition to DataclassInfo."""
        return DataclassInfo.from_class(
            cls, hide_private=cls._EXPORT_SETUP_.hide_private
        )

    @classmethod
    def export(
        cls, output_dir, format_type="yaml", exist_ok=False, makedirs=False, **kwargs
    ):
        """Export the class schema definition in the specified format.

        Args:
            output_dir: Output directory
            format_type: Output format (yaml, json, etc.)
            exist_ok: Overwrite existing file
            makedirs: Create missing directories
            **kwargs: Additional formatting options
                - detailed: bool = True    # detailed mode
                - show_docs: bool = True   # Include docstrings
        """
        strategy = cls._get_export_strategy()
        strategy.export(cls, output_dir, format_type, exist_ok, makedirs, **kwargs)

    @classmethod
    def view_schema(cls, format_type="yaml", **kwargs):
        """Display the class schema definition.

        Args:
            format_type: Display format (yaml, json, etc.)
            **kwargs: Additional display options
        """
        schema_info = cls.to_schema_info()
        formatter = Formatter.get_registered(format_type)()
        formatter.update_settings(**kwargs)
        content = formatter.to_str(schema_info)
        formatter.display(content)

    @classmethod
    def _get_export_strategy(cls):
        """Get the appropriate export strategy for the decorated class."""
        strategy_name = cls._get_export_strategy_name()
        return ExportStrategy.get_registered(strategy_name)

    @classmethod
    def _get_export_strategy_name(cls):
        """Get the appropriate strategy for a class."""
        return cls._EXPORT_SETUP_.strategy
