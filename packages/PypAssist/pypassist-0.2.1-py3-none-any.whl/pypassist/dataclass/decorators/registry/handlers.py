#!/usr/bin/env python3
"""
Registry handlers for type and settings management.
"""

from .exceptions import RegistrySetupError, RegistryAttributeError


class TypeRegistry:
    """Handles type validation and registration."""

    @classmethod
    def validate_type(cls, instance, setup):
        """Validates and normalizes the type.

        Args:
            instance: The instance being processed
            setup: Registry setup configuration

        Returns:
            str: The validated type value

        Raises:
            RegistrySetupError: If the required attribute is missing
            RegistryAttributeError: If the type value is None
        """

        if not hasattr(instance, setup.register_name_attr):
            raise RegistrySetupError(
                f"Missing required attribute '{setup.register_name_attr}'"
            )
        type_value = getattr(instance, setup.register_name_attr)
        if type_value is None:
            raise RegistryAttributeError(f"'{setup.register_name_attr}' cannot be None")
        setattr(instance, setup.register_name_attr, str(type_value))
        return type_value

    @classmethod
    def get_registration(cls, registration_base_class, register_name):
        """Gets the registered class for the type.

        Args:
            registration_base_class: The registration base class
            register_name: The register name for the type to get

        Returns:
            The registered class for the type

        Raises:
            RegistrySetupError: If registration_base_class is not set
        """
        if registration_base_class is None:
            raise RegistrySetupError(
                "registration_base_class must be set in the configuration"
            )
        return registration_base_class.get_registered(register_name)


class SettingsHandler:  # pylint: disable=R0903
    """Handles settings configuration and validation."""

    @classmethod
    def configure_settings(cls, instance, reg_cls, type_value, setup):
        """Configures settings for the instance.

        Args:
            instance: The instance being processed
            reg_cls: The registered class
            type_value: The type value
            setup: Registry setup configuration

        Raises:
            RegistryAttributeError: If the registered class is missing required attributes
            TypeError: If settings value is of invalid type
        """
        if not hasattr(instance, setup.settings_attr):
            return

        settings_value = getattr(instance, setup.settings_attr)
        # pylint : disable=protected-access
        cls._validate_settings_class(reg_cls, setup)
        conf_dcls = getattr(reg_cls, setup.settings_dataclass_attr)
        cls._process_settings(instance, settings_value, conf_dcls, type_value, setup)

    @classmethod
    def _validate_settings_class(cls, reg_cls, setup):
        """Validates that the registered class has the required settings attribute.

        Args:
            reg_cls: The registered class to validate
            setup: Registry setup configuration

        Raises:
            RegistryAttributeError: If the required attribute is missing
        """
        if not hasattr(reg_cls, setup.settings_dataclass_attr):
            raise RegistryAttributeError(
                f"Registered class '{reg_cls.__name__}' missing required "
                f"attribute '{setup.settings_dataclass_attr}'"
            )

    @classmethod
    def _process_settings(  # pylint: disable=too-many-arguments
        cls, instance, settings_value, conf_dcls, type_value, setup
    ):
        """Processes and validates settings value.

        Args:
            instance: The instance being processed
            settings_value: The settings value to process
            conf_dcls: The settings dataclass
            type_value: The type value
            setup: Registry setup configuration

        Raises:
            TypeError: If settings value is of invalid type
        """
        if settings_value is None:
            # Handle None by creating an instance of the expected settings class
            # If it pass validation, it will be set on the instance
            settings_value = conf_dcls()
        if isinstance(settings_value, dict):
            setattr(instance, setup.settings_attr, conf_dcls(**settings_value))
        elif not isinstance(settings_value, conf_dcls):
            raise TypeError(
                f"Invalid type for {type_value} configuration: "
                f"expected {conf_dcls.__name__}, got {type(settings_value).__name__}"
            )
