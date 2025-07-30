#!/usr/bin/env python3
"""Helper mixin to convert strings to enum values."""


import json
import yaml


class EnumStrMixin:
    """
    Mixin class that provides a classmethod to parse a string into an Enum.
    and a property to get the value as a string.
    """

    def __init_subclass__(cls, **kwargs):
        """Called when a class inherits from this mixin."""
        super().__init_subclass__(**kwargs)

        def enum_representer(dumper, data):
            """Use __str__ for YAML representation."""
            return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))

        yaml.add_representer(cls, enum_representer, Dumper=yaml.SafeDumper)

        json.JSONEncoder.default = lambda self, data: (
            str(data) if isinstance(data, cls) else json.JSONEncoder.default(self, data)
        )

    @classmethod
    def from_str(cls, value, info=None):  # pylint: disable=unused-argument
        """Parse a string into an Enum value.

        Handles various string formats intelligently:
        - Case-insensitive matching
        - Strips whitespace

        Args:
            value (Any): The string to parse or an existing enum value.
            info (pydantic.ValidationInfo, optional): Additional validation metadata
                provided by Pydantic. This parameter is ignored but included for compatibility.

        Returns:
            EnumStrMixin: An instance of the Enum.

        Raises:
            ValueError: If the string cannot be converted to a valid enum value.
            TypeError: If the input is not a string or an instance of the Enum.
        """
        if isinstance(value, cls):
            return value

        if not isinstance(value, str):
            raise ValueError(
                f"Expected string or {cls.__name__}, " f"got {type(value).__name__}"
            )

        # Normalize input
        value = value.strip().upper()

        try:
            return cls[value]
        except KeyError as err:
            valid_values = ", ".join(f"'{v.name.lower()}'" for v in cls)
            raise ValueError(
                f"Invalid {cls.__name__.lower()}: '{value}'. "
                f"Valid values are: {valid_values}"
            ) from err

    @property
    def label(self):
        """
        Returns a lowercase, human-readable version of the enum name.
        """
        return self.name.upper()

    def upper(self):
        """
        Returns a uppercase, human-readable version of the enum name.
        """
        return self.name.upper()

    def lower(self):
        """
        Returns a lowercase, human-readable version of the enum name.
        """
        return self.name.lower()

    def __str__(self):
        """Returns string representation for serialization."""
        return self.label

    @classmethod
    def __get_validators__(cls):
        """Pydantic hook to use `from_str` automatically during validation."""
        yield cls.from_str
