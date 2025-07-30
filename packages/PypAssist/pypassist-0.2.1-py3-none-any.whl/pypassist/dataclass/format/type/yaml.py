#!/usr/bin/env python3
"""
YAML formatter.
"""

from collections import OrderedDict
import dataclasses
import logging

import textwrap
import yaml
from pydantic.dataclasses import dataclass

from ..base import Formatter
from ..info import DataclassInfo
from ....utils.ipynb import is_in_ipynb
from ....utils.convert import to_dict_recursive

LOGGER = logging.getLogger(__name__)


@dataclass
class YamlFormatterSettings:
    """YAML formatter settings."""

    max_width: int = 80
    indent: str = "  "
    indent_level: int = 0
    show_header: bool = False  # whether to show header
    detailed: bool = True  # whether to use detailed mode
    show_docs: bool = True  # whether to show docs in detailed mode


class YamlFormatter(Formatter, register_name="yaml"):
    """YAML formatter."""

    SETTINGS_DATACLASS = YamlFormatterSettings

    def __init__(self, settings=None):
        if settings is None:
            settings = YamlFormatterSettings()
        super().__init__(settings)

    def to_serialized(self, class_info):
        """Convert DataclassInfo to a serialized object."""
        return self.to_str(class_info)

    def to_str(self, class_info):
        """Format DataclassInfo into YAML string."""
        if self.settings.detailed:
            return self._format_detailed(class_info)
        return self._format_simple(class_info)

    def display(self, content):
        """Display the formatted content."""
        if is_in_ipynb():
            # pylint: disable=import-outside-toplevel
            from IPython.display import display_markdown

            LOGGER.debug("Displaying content in Jupyter Notebook.")
            display_markdown(f"```yaml\n{content}\n```", raw=True)
        else:
            LOGGER.debug("Displaying content in terminal.")
            print(content)

    def _format_detailed(self, class_info):
        """Format class info in detailed mode."""
        content = []

        if self.settings.show_header:
            content.extend(self._format_header(class_info))

        if class_info.is_empty:
            content.append(class_info.empty_message)
        else:
            content.extend(self._format_detailed_fields(class_info))

        return "\n".join(content)

    def _format_detailed_fields(self, class_info):
        """Format the fields of a non-empty dataclass in detailed mode."""
        content = []
        current_indent = self.settings.indent * self.settings.indent_level

        for field in class_info.fields:
            if self.settings.show_docs:
                if field.description:
                    content.extend(self._wrap_comment(field.description))
                content.append(f"{current_indent}## Type: {field.type_info}")

            if isinstance(field.value, DataclassInfo):
                nested_settings = dataclasses.replace(
                    self.settings, indent_level=self.settings.indent_level + 1
                )
                nested_formatter = YamlFormatter(settings=nested_settings)
                content.append(f"{current_indent}{field.name}:")
                nested_content = nested_formatter.to_str(field.value)
                content.extend(
                    f"{current_indent}{self.settings.indent}{line}"
                    for line in nested_content.splitlines()
                )
            else:
                value_str = yaml.safe_dump(
                    {field.name: field.value}, **self._yaml_dump_kwargs
                ).rstrip()
                content.extend(
                    f"{current_indent}{line}" for line in value_str.splitlines()
                )

        return content

    def _format_simple(self, class_info):
        """Format class info in simple mode (attributes = values)."""
        if class_info.is_empty:
            return class_info.empty_message

        data = self._build_simple(class_info)
        data_dict = to_dict_recursive(data)  # OrderedDict -> dict
        return yaml.safe_dump(data_dict, **self._yaml_dump_kwargs)

    def _build_simple(self, class_info):
        """Build a simple dictionary representation."""
        result = OrderedDict()
        for field_info in class_info.fields:
            if isinstance(field_info.value, DataclassInfo):
                result[field_info.name] = self._build_simple(field_info.value)
            else:
                result[field_info.name] = field_info.value
        return result

    def _format_header(self, class_info):
        """Format the header section with class name and description."""
        result = []
        base_indent = self.settings.indent * self.settings.indent_level
        header_width = self.settings.max_width // 2

        result.append(f"{base_indent}# {'~'*header_width}")
        result.append(f"{base_indent}# {class_info.name.upper()}")

        if self.settings.show_docs and class_info.description:
            result.extend(self._wrap_comment(class_info.description))

        result.append(f"{base_indent}# {'~'*header_width}")
        return result

    def _wrap_comment(self, text):
        """Wrap text into YAML comments."""
        indent_level = self.settings.indent_level
        indent = self.settings.indent * indent_level
        wrapped = textwrap.wrap(
            text,
            width=self.settings.max_width - len(indent) - 2,
            break_long_words=False,
            break_on_hyphens=False,
        )
        return [f"{indent}## {line}" for line in wrapped]

    @property
    def _yaml_dump_kwargs(self):
        """Common yaml.safe_dump parameters."""
        return {
            "default_flow_style": False,
            "indent": len(self.settings.indent),
            "width": self.settings.max_width,
            "allow_unicode": True,
        }
