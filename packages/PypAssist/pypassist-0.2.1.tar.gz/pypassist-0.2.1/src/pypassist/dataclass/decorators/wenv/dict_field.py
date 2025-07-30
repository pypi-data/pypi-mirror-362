#!/usr/bin/env python3
"""
Working environment handlers for dictionary field processing.
"""

from ....fallback.typing import get_args
from .exceptions import WenvError


class DictFieldProcessor:  # pylint: disable=too-few-public-methods
    """Handles conversion of dictionary fields to dataclass instances."""

    @classmethod
    def process_field(cls, instance, field):
        """Converts a dictionary field to dataclass instances.

        Args:
            instance: The instance being processed
            field: The field to process

        Raises:
            WenvError: If a value cannot be converted to the expected type
        """
        expected_cls = get_args(field.type)[1]
        values = getattr(instance, field.name)
        if not values:  # Handle None or empty dict
            return

        cls._convert_dict_values(values, expected_cls)

    @classmethod
    def _convert_dict_values(cls, values, expected_cls):
        """Converts dictionary values to the expected class.

        Args:
            values: Dictionary of values to convert
            expected_cls: Expected class for the values

        Raises:
            WenvError: If a value cannot be converted to the expected type
        """
        for key, value in values.items():
            if isinstance(value, dict):
                values[key] = expected_cls(**value)
            elif not isinstance(value, expected_cls):
                raise WenvError(f"Unable to convert {value} to {expected_cls.__name__}")
