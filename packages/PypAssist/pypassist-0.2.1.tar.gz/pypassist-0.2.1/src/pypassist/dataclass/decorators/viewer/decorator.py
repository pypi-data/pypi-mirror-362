#!/usr/bin/env python3
"""
Viewer decorator.
"""


import logging

from ..base import BaseDecorator
from .setup import ViewerSetup
from .exceptions import ViewerSetupError
from ...format.base import Formatter
from ...format.info import DataclassInfo

LOGGER = logging.getLogger(__name__)


def viewer(_cls=None, *, setup=None, **kwargs):
    """Viewer dataclass decorator for enhanced data visualization and formatting.

    Args:
        _cls: The class to decorate
        setup: ViewerSetup instance containing display configuration
        kwargs: Setup fields. Will override corresponding field in setup.

    Returns:
        Decorated class with visualization and formatting capabilities

    Raises:
        ViewerSetupError: If setup configuration is invalid

    Example:
        @viewer
        class MyConfig:
            name: str
            _private_field: str  # Will be hidden in output
    """

    def wrap(cls):
        try:
            cls, setup_instance = BaseDecorator.decorate_class(
                cls, ViewerSetup, setup, **kwargs
            )
        except ValueError as err:
            raise ViewerSetupError(str(err)) from err

        class ViewerClass(cls):  # pylint: disable=R0903, C0115
            cls._SETUP_ = setup_instance

            def to_info(self):
                """Convert the instance to DataclassInfo."""
                setup = self._SETUP_
                hide_private = getattr(setup, "hide_private", False)
                return DataclassInfo.from_instance(self, hide_private=hide_private)

            def to_str(self, format_type="yaml", **kwargs):
                """Format the class data to a string representation.

                Args:
                    format_type: Output format (yaml, json, etc.)
                    **kwargs: Additional formatting options

                Returns:
                    Formatted string representation
                """
                formatter = Formatter.get_registered(format_type)()
                formatter.update_settings(**kwargs)
                return formatter.to_str(self.to_info())

            def serialize(self, format_type="json", **kwargs):
                """Convert the class to a serialized object.

                Args:
                    format_type: Serialization format
                    **kwargs: Additional serialization options

                Returns:
                    Serialized representation
                """
                formatter = Formatter.get_registered(format_type)()
                formatter.update_settings(**kwargs)
                return formatter.to_serialized(self.to_info())

            def view(self, format_type="yaml", **kwargs):
                """Display formatted class information.

                Args:
                    format_type: Display format
                    **kwargs: Additional display options
                """
                content = self.to_str(format_type, **kwargs)
                formatter = Formatter.get_registered(format_type)()
                formatter.display(content)

        BaseDecorator.preserve_cls_metadata(ViewerClass, cls)
        return ViewerClass

    if _cls is None:
        return wrap
    return wrap(_cls)
