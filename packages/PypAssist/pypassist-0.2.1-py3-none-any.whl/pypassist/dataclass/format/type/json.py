#!/usr/bin/env python3
"""
JSON formatter.
"""

import logging

import json
from pydantic.dataclasses import dataclass

from ..base import Formatter
from ....utils.ipynb import is_in_ipynb

LOGGER = logging.getLogger(__name__)


@dataclass
class JsonFormatterSettings:
    """JSON formatter settings."""

    indent: int = 4
    sort_keys: bool = False
    detailed: bool = False  # detailed mode
    show_docs: bool = False  # whether to include doc in detailed mode


class JsonFormatter(Formatter, register_name="json"):
    """JSON formatter."""

    SETTINGS_DATACLASS = JsonFormatterSettings

    def __init__(self, settings=None):
        if settings is None:
            settings = JsonFormatterSettings()
        super().__init__(settings)

    def to_str(self, class_info):
        """Format DataclassInfo into JSON string."""
        if self.settings.detailed:
            data = self._build_detailed(class_info)
        else:
            data = self._build_simple(class_info)

        return json.dumps(
            data,
            indent=self.settings.indent,
            sort_keys=self.settings.sort_keys,
        )

    def display(self, content):
        """Display the formatted JSON content."""
        if is_in_ipynb():
            # pylint: disable=import-outside-toplevel
            from IPython.display import (
                display_json,
            )

            LOGGER.debug("Displaying JSON content in Jupyter Notebook.")
            display_json(content, raw=True)
        else:
            LOGGER.debug("Displaying JSON content in terminal.")
            print(content)

    def to_serialized(self, class_info):
        """Convert DataclassInfo to a dictionary for JSON serialization."""
        if self.settings.detailed:
            return self._build_detailed(class_info)
        return self._build_simple(class_info)

    def _build_simple(self, class_info):
        """Build a simple name/value representation for direct instantiation.
        This is the default format, suitable for serialization/deserialization.
        """
        result = {}
        for field_info in class_info.fields:
            if isinstance(field_info.value, type(class_info)):
                result[field_info.name] = self._build_simple(field_info.value)
            else:
                result[field_info.name] = field_info.value
        return result

    def _build_detailed(self, class_info):
        """Build a detailed schema representation including metadata."""
        result = {"name": class_info.name, "fields": {}}

        if self.settings.show_docs:
            result["description"] = class_info.description

        for field_info in class_info.fields:
            field_data = {
                "type": field_info.type_info,
            }

            if self.settings.show_docs:
                field_data["description"] = field_info.description

            if isinstance(field_info.value, type(class_info)):
                field_data["value"] = self._build_detailed(field_info.value)
            else:
                field_data["value"] = field_info.value

            result["fields"][field_info.name] = field_data

        return result
