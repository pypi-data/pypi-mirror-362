#!/usr/bin/env python3
"""
Default export strategy for simple configurations.
"""

import pathlib
import logging

from ..base import ExportStrategy
from .....format.base import Formatter
from ......utils.export import export_string, create_directory


LOGGER = logging.getLogger(__name__)


class DefaultExportStrategy(ExportStrategy, register_name="default"):
    """Default export strategy for dataclasses."""

    @classmethod
    def export(  # pylint: disable=too-many-arguments
        cls,
        data_cls,
        output_dir,
        format_type="yaml",
        exist_ok=False,
        makedirs=False,
        **kwargs,
    ):
        """Export the configuration."""
        formatter = Formatter.get_registered(format_type)()
        formatter.update_settings(**kwargs)
        schema_info = data_cls.to_schema_info()
        content = formatter.to_str(schema_info)

        base_name = (
            # pylint: disable=protected-access
            data_cls._EXPORT_SETUP_.stem_file
        )
        if base_name is None:
            base_name = data_cls.__name__.lower()

        filename = f"{base_name}.{format_type}"
        if makedirs:
            output_dir = create_directory(output_dir)
        else:
            output_dir = pathlib.Path(output_dir).resolve()
        output_path = output_dir / filename
        export_string(content, output_path, exist_ok=exist_ok)
        LOGGER.info("Saved schema to %s", output_path)
