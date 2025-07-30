#!/usr/bin/env python3
"""
Working environment decorator.
"""

import logging

from ....fallback.typing import get_origin
from ..base import BaseDecorator
from .exceptions import WenvSetupError
from .setup import WenvSetup
from .dict_field import DictFieldProcessor

LOGGER = logging.getLogger(__name__)


def wenv(_cls=None, *, setup=None, **kwargs):
    """Work environment configuration decorator.

    This decorator ensures proper initialization of nested dictionary fields,
    converting dict values to their corresponding dataclasses.
    """

    def wrap(cls):
        try:
            cls, setup_instance = BaseDecorator.decorate_class(
                cls, WenvSetup, setup, **kwargs
            )
        except ValueError as err:
            raise WenvSetupError(str(err)) from err

        class WenvClass(cls):  # pylint: disable=R0903, C0115
            cls._SETUP_ = setup_instance
            cls._WENV_ = True

            def __post_init__(self):
                if hasattr(super(), "__post_init__"):  # parent post-init
                    super().__post_init__()

                for field in self.__class__.__dataclass_fields__.values():
                    if get_origin(field.type) is dict:
                        DictFieldProcessor.process_field(self, field)

        BaseDecorator.preserve_cls_metadata(WenvClass, cls)
        return WenvClass

    if _cls is None:
        return wrap
    return wrap(_cls)
