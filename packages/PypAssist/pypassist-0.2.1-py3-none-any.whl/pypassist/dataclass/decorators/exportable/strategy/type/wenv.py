#!/usr/bin/env python3
"""
Work environment export strategy.
"""

import dataclasses
import pathlib
import logging

from pydantic.dataclasses import dataclass

from ..base import ExportStrategy
from ...validation import is_exportable
from ...decorator import exportable
from ....wenv.validation import is_wenv
from ......fallback.typing import get_args, get_origin, List
from ......utils.typing import type_to_string

LOGGER = logging.getLogger(__name__)

from ......runner.workenv.custom.config.workenv import CustomWorkEnvConfig


class WenvExportStrategy(ExportStrategy, register_name="wenv"):
    """Export strategy for work environment configurations."""

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
        """Export the working environment dataclass.

        Args:
            data_cls: The dataclass to export
            output_dir: Directory where to export the data
            format_type: Format to use for export (default: yaml)
            exist_ok: If True, overwrite existing files
            makedirs: If True, create directories if they don't exist
            **kwargs: Additional export options
        """
        output_dir = pathlib.Path(output_dir).resolve()

        # Export each field of the dataclass
        cls._export_fields(
            data_cls, output_dir, format_type, exist_ok, makedirs, **kwargs
        )

        # Export the default configuration
        cls._export_default_workenv(
            data_cls, output_dir, format_type, exist_ok, makedirs, **kwargs
        )

    # -------------------------------------------------------------------------
    # Field export methods
    # -------------------------------------------------------------------------

    @classmethod
    def _export_fields(  # pylint: disable=too-many-arguments
        cls, data_cls, output_dir, format_type, exist_ok, makedirs, **kwargs
    ):
        """Export the fields of the work environment.

        This method handles the export of different field types:
        - Work environment fields
        - Dictionary fields
        - Basic exportable fields
        """
        for field in dataclasses.fields(data_cls):
            field_type = field.type
            if is_wenv(field_type):
                updated_dir = output_dir / field.name
                cls._export_wenv_field(
                    field_type, updated_dir, format_type, exist_ok, makedirs, **kwargs
                )
                continue

            if get_origin(field_type) is dict:
                cls._export_dict_field(
                    field, output_dir, format_type, exist_ok, makedirs, **kwargs
                )
                continue

            if is_exportable(field_type):
                field_type.export(
                    output_dir / field.name,
                    format_type=format_type,
                    exist_ok=exist_ok,
                    makedirs=makedirs,
                    **kwargs,
                )
                continue

            LOGGER.warning(
                "Field '%s' of type '%s' is not exportable. Will be skipped.",
                field.name,
                type_to_string(field_type),
            )

    @classmethod
    def _export_wenv_field(  # pylint: disable=too-many-arguments
        cls, field_type, output_dir, format_type, exist_ok, makedirs, **kwargs
    ):
        """Export a work environment field."""
        field_type.export(
            output_dir,
            format_type=format_type,
            exist_ok=exist_ok,
            makedirs=makedirs,
            **kwargs,
        )

    @classmethod
    def _export_dict_field(  # pylint: disable=too-many-arguments
        cls, field, output_dir, format_type, exist_ok, makedirs, **kwargs
    ):
        """Export a dictionary field."""
        dict_val_cls = get_args(field.type)[1]
        if is_exportable(dict_val_cls):
            field_outdir = output_dir / field.name
            dict_val_cls.export(
                field_outdir,
                format_type=format_type,
                exist_ok=exist_ok,
                makedirs=makedirs,
                **kwargs,
            )

    # -------------------------------------------------------------------------
    # Default configuration export methods
    # -------------------------------------------------------------------------

    @classmethod
    def _export_default_workenv(  # pylint: disable=too-many-arguments
        cls, data_cls, output_dir, format_type, exist_ok, makedirs, **kwargs
    ):
        """Export the default work environment configuration."""
        # Build the list of defaults from the dataclass fields
        defaults = cls._build_defaults_list(data_cls)
        if not defaults:  # Nothing to export
            return
        # Create and export the default configuration
        default_conf = cls._create_default_config(
            defaults, data_cls._EXPORT_SETUP_.stem_file
        )
        default_conf.export(  # pylint: disable=E1101
            output_dir,
            format_type=format_type,
            exist_ok=exist_ok,
            makedirs=makedirs,
            detailed=False,
        )

    @classmethod
    def _build_defaults_list(cls, data_cls):
        """Build the list of defaults from the dataclass fields.

        This method processes each field in the dataclass and builds appropriate
        default entries based on the field type:
        - For dict fields with exportable values: Uses registry or single defaults
        - For basic exportable fields: Uses simple key-value defaults
        """
        defaults = []

        for field in dataclasses.fields(data_cls):
            # Handle dictionary fields (typically for registries)
            if get_origin(field.type) is dict:
                value_type = get_args(field.type)[1]
                if is_exportable(value_type):
                    defaults.extend(cls._build_field_defaults(field.name, value_type))

            # Handle basic exportable fields
            if is_exportable(field.type):
                defaults.extend(
                    cls._build_field_single_basic_default(field.name, field.type)
                )

        return defaults

    @classmethod
    def _build_field_defaults(cls, field_name, value_type):
        """Build defaults for a field based on its type.

        Returns registry defaults if the type has a registry base class,
        otherwise returns a single default entry.
        """
        if hasattr(value_type, "_REG_BASE_CLASS_"):
            return cls._build_registry_defaults(field_name, value_type)
        return [cls._build_single_default(field_name, value_type)]

    @classmethod
    def _build_registry_defaults(cls, field_name, value_type):
        """Build defaults for a registry type.

        Creates a list of defaults for each registered type in the registry,
        using the format: field_name/reg_type@field_name.reg_type
        """
        base_cls = value_type._REG_BASE_CLASS_  # pylint: disable=protected-access
        return [
            f"{field_name}/{reg_type}@{field_name}.{reg_type}"
            for reg_type in base_cls.list_registered()
        ]

    @classmethod
    def _build_single_default(cls, field_name, value_type):
        """Build a single default entry for a field.

        Uses the format: field_name/stem@field_name.stem
        where stem is either the configured stem_file or the lowercase class name.
        """
        stem = (
            value_type._EXPORT_SETUP_.stem_file  # pylint: disable=protected-access
            or value_type.__name__.lower()
        )
        return f"{field_name}/{stem}@{field_name}.{stem}"

    @classmethod
    def _build_field_single_basic_default(cls, field_name, value_type):
        """Build a default entry for a basic exportable field.

        Returns a list containing a single dictionary with the field name as key
        and stem as value, which will be properly serialized in YAML format.
        """
        stem = (
            value_type._EXPORT_SETUP_.stem_file  # pylint: disable=protected-access
            or value_type.__name__.lower()
        )
        return [{field_name: stem}]

    @classmethod
    def _create_default_config(cls, defaults, stem_file=None):
        """Create the default configuration dataclass.

        Args:
            defaults: List of default entries to include in the configuration

        Returns:
            A dataclass configured with the provided defaults
        """
        if stem_file is None:
            stem_file = "workenv_template"

        @exportable(stem_file=stem_file)
        @dataclass
        class DefaultConfig:  # pylint: disable=C0115
            defaults: List = dataclasses.field(default_factory=lambda: defaults)

        return DefaultConfig
