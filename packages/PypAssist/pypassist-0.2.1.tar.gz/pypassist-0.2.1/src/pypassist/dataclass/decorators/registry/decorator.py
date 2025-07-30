#!/usr/bin/env python3
"""
Registry decorator for dataclass.
"""

import logging

from ..base import BaseDecorator

from .exceptions import RegistrySetupError
from .setup import RegistrySetup
from .handlers import TypeRegistry, SettingsHandler

LOGGER = logging.getLogger(__name__)


def registry(base_cls, _cls=None, *, setup=None, **kwargs):
    """Exportable decorator for registry-based schema definitions.

    Args:
        _cls: The class to decorate
        base_cls: The base class for the registry
        setup: Optional. Registry setup configuration.
        kwargs: Optional setup overrides

    Example:
        @registry(base_cls=MyBaseClass, setup=MySetup)
        class MyClassConfig:
            name: str
            settings: Dict[str, Any]
    """

    def wrap(cls):
        try:
            cls, setup_instance = BaseDecorator.decorate_class(
                cls, RegistrySetup, setup, **kwargs
            )
        except ValueError as err:
            raise RegistrySetupError(str(err)) from err

        class RegistryClass(cls):  # pylint: disable=R0903, C0115
            cls._SETUP_ = setup_instance
            cls._REG_BASE_CLASS_ = base_cls
            cls._REGISTRY_ = True

            def _handle_parent_post_init(self):
                """Handle parent class post-init if it exists."""
                post_init = getattr(super(), "__post_init__", None)
                if callable(post_init):
                    post_init()  # pylint: disable=not-callable

            def _configure_type_registration(self):
                """Configure type registration and get registered class."""
                type_value = TypeRegistry.validate_type(self, self._SETUP_)
                return TypeRegistry.get_registration(self._REG_BASE_CLASS_, type_value)

            def _setup_settings(self, reg_cls, type_value):
                """Setup settings configuration."""
                SettingsHandler.configure_settings(
                    self, reg_cls, type_value, self._SETUP_
                )

            def __post_init__(self):
                self._handle_parent_post_init()
                reg_cls = self._configure_type_registration()
                type_value = getattr(self, self._SETUP_.register_name_attr)
                self._setup_settings(reg_cls, type_value)

            @classmethod
            def reload_registry(cls, clear=False):
                """Reload registry.

                Args:
                    clear: If True, clears all current registrations before reloading
                """
                LOGGER.debug("Reloading registry from %s", cls.__name__)
                # pylint: disable=protected-access
                submod = cls._REG_BASE_CLASS_._TYPE_SUBMODULE
                cls._REG_BASE_CLASS_.reload(submod=submod, clear=clear)

        BaseDecorator.preserve_cls_metadata(RegistryClass, cls)
        return RegistryClass

    if _cls is None:
        return wrap
    return wrap(_cls)
