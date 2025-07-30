#!/usr/bin/env python3
"""
Dataclass information classes supporting both instances and schema definitions.
"""

import dataclasses
import inspect
from typing import Any
from docstring_parser import parse as parse_docstring

from ...utils.typing import type_to_string
from ...fallback.typing import List, NoneType
from ...fallback.pydantic import is_pydantic_dataclass

# from ...utils.empty_settings import NoneType
from ..exceptions import DataclassError


def _get_extra_metadata(field):
    """Get field metadata if any."""
    return getattr(field, "metadata", None)


def is_metadata_required(field, required_flag="_FORCE_REQUIRED_"):
    """Check if field is required through metadata override."""
    extra = _get_extra_metadata(field)
    return extra is not None and extra.get(required_flag, False) is True


def is_default_missing(field):
    """Check if field has no default value."""
    return (
        field.default is dataclasses.MISSING
        and field.default_factory is dataclasses.MISSING
    )


def is_required_field(field):
    """Check if field should be treated as required."""
    return is_metadata_required(field) or is_default_missing(field)


@dataclasses.dataclass
class DataclassFieldInfo:
    """Information about a dataclass field."""

    name: str
    type_info: str
    description: str
    value: Any

    @classmethod
    def from_field(cls, field, instance=None, docs=None):
        """Create DataclassFieldInfo from a dataclass Field."""
        type_string = type_to_string(field.type)
        field_description = docs.get(field.name) if docs else "UNDOCUMENTED"

        required_field = is_required_field(field)

        if instance is not None:
            # Instance mode
            field_value = getattr(instance, field.name)

            if field_value is None and not required_field:
                field_value = field.default

            if field_value is not None and is_pydantic_dataclass(type(field_value)):
                field_value = DataclassInfo.from_instance(field_value)
        else:
            # Schema mode
            if not required_field or is_metadata_required(field):
                if field.default is not dataclasses.MISSING:
                    field_value = field.default
                else:
                    field_value = field.default_factory()
            else:
                field_value = "..."

            if is_pydantic_dataclass(field.type):
                field_value = DataclassInfo.from_class(field.type)

        required_status = " [REQUIRED]" if required_field else " [OPTIONAL]"
        type_info = f"{type_string}{required_status}"

        return cls(
            name=field.name,
            type_info=type_info,
            description=field_description,
            value=field_value,
        )


@dataclasses.dataclass
class DataclassInfo:
    """Information about a dataclass."""

    name: str
    description: str
    fields: List[DataclassFieldInfo] = None
    is_empty: bool = dataclasses.field(init=False, default=False)
    empty_message: str = dataclasses.field(init=False, default="")

    _DEFAULT_EMPTY_MESSAGE = "## No field defined in: {name}"

    def __post_init__(self):
        if self.fields is None:
            self.fields = []

        # is dataclass empty
        self.is_empty = len(self.fields) == 0
        if self.is_empty:
            self.empty_message = (
                f"\n{self._DEFAULT_EMPTY_MESSAGE.format(name=self.name)}"
            )

    @staticmethod
    def parse_docstring(docstring):
        """Parse docstring using docstring_parser."""
        if not docstring:
            return "", {}

        parsed = parse_docstring(docstring)
        description_parts = []

        if parsed.short_description:
            description_parts.append(parsed.short_description)
        if parsed.long_description:
            description_parts.append(parsed.long_description)

        description = "\n\n".join(description_parts)
        attr_docs = {param.arg_name: param.description for param in parsed.params}

        description = description.strip() or "UNDOCUMENTED"
        return description, attr_docs

    @classmethod
    def from_instance(cls, instance, hide_private=True):
        """Create DataclassInfo from a dataclass instance."""
        dataclass_type = instance.__class__
        cls._check_type(dataclass_type)
        docstring = inspect.getdoc(dataclass_type)
        class_desc, attr_docs = cls.parse_docstring(docstring)

        dc_fields = [
            f
            for f in dataclasses.fields(instance)
            if not (hide_private and f.name.startswith("_"))
        ]

        field_infos = [
            DataclassFieldInfo.from_field(field=f, instance=instance, docs=attr_docs)
            for f in dc_fields
        ]

        return cls(
            name=dataclass_type.__name__,
            description=class_desc,
            fields=field_infos,
        )

    @classmethod
    def from_class(cls, dataclass_type, hide_private=True):
        """Create DataclassInfo from a dataclass type for schema definition."""
        cls._check_type(dataclass_type)

        docstring = inspect.getdoc(dataclass_type)
        class_desc, attr_docs = cls.parse_docstring(docstring)

        dc_fields = [
            f
            for f in dataclasses.fields(dataclass_type)
            if not (hide_private and f.name.startswith("_"))
        ]

        field_infos = [
            DataclassFieldInfo.from_field(field=f, docs=attr_docs) for f in dc_fields
        ]

        return cls(
            name=dataclass_type.__name__,
            description=class_desc,
            fields=field_infos,
        )

    @classmethod
    def _check_type(cls, dataclass_type):
        validate_pydantic_dataclass(dataclass_type)


def validate_pydantic_dataclass(dataclass_type):
    """Check if the given object is a pydantic dataclass or NoneType."""
    # Special case for NoneType
    if dataclass_type is NoneType:
        return

    if not is_pydantic_dataclass(dataclass_type):
        raise DataclassError(
            f"Expected pydantic dataclass, got {dataclass_type.__name__}"
        )


def has_required_fields(datacls):
    """
    Check if at least one fields in a dataclass are required.

    A field is considered required if:
    - It has no default value and no default_factory
    - OR if its metadata contains '_FORCE_REQUIRED_': True

    Args:
        datacls: The dataclass to check

    Returns:
        bool: True if all fields are required, False otherwise
    """
    # Special case for NoneType
    if datacls is NoneType:
        return False

    validate_pydantic_dataclass(datacls)
    fields = dataclasses.fields(datacls)
    return any(is_required_field(field) for field in fields)
