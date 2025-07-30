#!/usr/bin/env python3
"""
Base export strategy.
"""

import dataclasses
import logging

from pydantic.dataclasses import dataclass

from ..base import ExportStrategy
from ...decorator import exportable
from .....format.info import has_required_fields
from ......fallback.typing import NoneType


LOGGER = logging.getLogger(__name__)


class RegistryExportStrategy(ExportStrategy, register_name="registry"):
    """Export strategy for registry-based configurations."""

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
        """Export strategy for registry dataclasses."""
        # pylint: disable=protected-access
        registry_class = data_cls._REG_BASE_CLASS_
        cls_settings_attr = data_cls._SETUP_.settings_dataclass_attr

        data_cls.reload_registry()  # Reload registry

        # Export schema for each registered type
        for registration_name, registered_cls in registry_class._get_register().items():
            settings_type = getattr(registered_cls, cls_settings_attr, None)
            temp_config = cls._create_exportable_temp_config(
                data_cls, registration_name, settings_type
            )
            temp_config.export(
                output_dir,
                format_type=format_type,
                exist_ok=exist_ok,
                makedirs=makedirs,
                **kwargs,
            )

    @classmethod
    def _create_exportable_temp_config(cls, data_cls, registration_name, settings_type):
        """Create a temporary config class for export."""
        # pylint: disable=protected-access
        settings_attr = data_cls._SETUP_.settings_attr
        register_name_attr = data_cls._SETUP_.register_name_attr

        annotations = dict(data_cls.__annotations__)

        # Special case for NoneType
        if settings_type is None or settings_type is NoneType:
            LOGGER.debug(
                "Skipping settings for %s as it uses NoneType", registration_name
            )
            # Use None as a placeholder for settings_type
            annotations[settings_attr] = type(None)
        else:
            annotations[settings_attr] = settings_type

        annotations[register_name_attr] = str

        @exportable
        @dataclass
        class TempConfig(data_cls):  # pylint: disable=C0115
            _EXPORT_SETUP_ = data_cls._EXPORT_SETUP_
            __annotations__ = annotations

            # pylint: disable=E3701
            locals()[register_name_attr] = dataclasses.field(
                default=registration_name,
                metadata={"_FORCE_REQUIRED_": True},
            )

            # Only add settings field if not NoneType
            if settings_type is not None and settings_type is not NoneType:
                if has_required_fields(settings_type):
                    locals()[settings_attr] = dataclasses.field(
                        default=None,
                        metadata={"_FORCE_REQUIRED_": True},
                    )

        # Update class setup and metadata
        TempConfig._EXPORT_SETUP_.stem_file = registration_name
        TempConfig.__name__ = cls.__name__
        TempConfig.__qualname__ = cls.__qualname__
        TempConfig.__module__ = cls.__module__
        TempConfig.__doc__ = data_cls.__doc__

        return TempConfig
