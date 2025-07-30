#!/usr/bin/env python3
"""
Exportable decorator for dataclass.
"""

import logging

from ..base import BaseDecorator
from .setup import ExportableSetup
from .exportable import ExportableMixin
from .exceptions import ExportableSetupError

LOGGER = logging.getLogger(__name__)


def exportable(_cls=None, *, setup=None, **kwargs):
    """Exportable decorator for enhanced data export capabilities.

    Args:
        _cls: The class to decorate
        setup: ExportableSetup instance containing export configuration
        kwargs: Setup fields. Will override corresponding field in setup.

    Example:
        @exportable
        class MyConfig:
            name: str
            value: int
    """

    def wrap(cls):
        try:
            cls, setup_instance = BaseDecorator.decorate_class(
                cls, ExportableSetup, setup, **kwargs
            )
        except ValueError as err:
            raise ExportableSetupError(str(err)) from err

        class ExportableClass(cls, ExportableMixin):  # pylint: disable=R0903, C0115
            cls._EXPORT_SETUP_ = setup_instance

        BaseDecorator.preserve_cls_metadata(ExportableClass, cls)
        return ExportableClass

    if _cls is None:
        return wrap
    return wrap(_cls)
