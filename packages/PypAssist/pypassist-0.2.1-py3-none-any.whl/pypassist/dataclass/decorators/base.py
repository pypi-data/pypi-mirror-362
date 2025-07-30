#!/usr/bin/env python3
"""
Base decorator for dataclass decorators.
"""

import dataclasses
import logging

from pydantic.dataclasses import dataclass

from ...fallback.pydantic import is_pydantic_dataclass

LOGGER = logging.getLogger(__name__)


class BaseDecorator:
    """Base decorator for dataclass decorators."""

    @staticmethod
    def decorate_class(decorated_cls, setup_cls, setup=None, **kwargs):
        """Base wrapper for dataclass decorators.

        Args:
            decorated_cls: Class to decorate
            setup_cls: Setup class to use (e.g. ViewerSetup, RegistrySetup)
            setup: Setup instance or dict
            kwargs: Additional setup parameters

        Returns:
            tuple: (processed_class, setup_instance)

        Raises:
            ValueError: If setup is not of the expected type
        """
        # Setup handling
        if setup is None:
            setup = setup_cls()
        if isinstance(setup, dict):
            setup = setup_cls(**setup)
        if not isinstance(setup, setup_cls):
            raise ValueError(
                f"Expected {setup_cls.__name__} but got {type(setup).__name__}"
            )
        if kwargs:
            setup = dataclasses.replace(setup, **kwargs)

        # Ensure pydantic dataclass
        if not is_pydantic_dataclass(decorated_cls):
            LOGGER.warning(
                "Decorator requires pydantic dataclass. "
                "Converting %s to pydantic dataclass. "
                "Use pydantic_dataclass decorator instead to suppress this warning.",
                decorated_cls.__name__,
            )
            decorated_cls = dataclass(decorated_cls)

        return decorated_cls, setup

    @staticmethod
    def preserve_cls_metadata(wrapped_cls, original_cls):
        """Preserve original class metadata.

        Args:
            wrapped_cls: The wrapped class
            original_cls: The original class
        """
        if "__pydantic_validator__" in original_cls.__dict__:
            wrapped_cls.__pydantic_validator__ = original_cls.__pydantic_validator__

        wrapped_cls.__name__ = original_cls.__name__
        wrapped_cls.__qualname__ = original_cls.__qualname__
        wrapped_cls.__module__ = original_cls.__module__
