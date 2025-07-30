#!/usr/bin/env python3
"""
Common mixin to handle settings.
"""

import dataclasses

import logging

from ..utils.export import export_string
from ..fallback.typing import NoneType

LOGGER = logging.getLogger(__name__)


class SettingsMixin:
    """
    Enhanced mixin for handling settings with nested updates support.

    Attributes:
        SETTINGS_DATACLASS: The dataclass to be used for settings.
    """

    SETTINGS_DATACLASS = NoneType

    def __init__(self, settings):
        settings = self._check_settings_type(settings)
        self._settings = settings

    @property
    def settings(self):
        """Get the current settings."""
        if self.SETTINGS_DATACLASS is NoneType:
            LOGGER.warning(
                "%s does not have settings. Returning None", self.__class__.__name__
            )
            return None
        return self._settings

    def _replace_settings_if_not_none(self, new_settings):
        """Replace settings if the new settings are not None."""
        if new_settings is not None:
            self._check_settings_type(new_settings)
            self._settings = dataclasses.replace(new_settings)

    def update_settings(self, settings=None, **kwargs):
        """
        Update the settings either with a new settings object or individual values.

        Args:
            settings: New settings object to update from
            **kwargs: Individual settings to update using dot notation for nested attributes
        """
        if self.SETTINGS_DATACLASS is NoneType:
            LOGGER.warning(
                "%s does not have settings. Ignoring update_settings call",
                self.__class__.__name__,
            )
            return

        self._replace_settings_if_not_none(settings)

        if not kwargs:
            return

        updates = {}
        nested_updates = {}

        for key, value in kwargs.items():
            if "." in key:
                nested_updates[key] = value
            else:
                updates[key] = value

        if updates:
            try:
                self._settings = dataclasses.replace(self._settings, **updates)
            except (AttributeError, TypeError) as err:
                raise ValueError(f"Invalid settings update: {err}") from err

        for path, value in nested_updates.items():
            try:
                self._update_nested_attribute(path, value)
            except AttributeError as err:
                LOGGER.warning("Failed to update nested setting `%s`: %s", path, err)

        self._trigger_post_init()

    def export_settings(
        self, output_dir, format_type="yaml", exist_ok=False, makedirs=False
    ):
        """
        Export the settings to a file.

        Args:
            output_dir: Directory where to export the settings
            format_type: Format to use for export (default: yaml)
            exist_ok: Whether to overwrite existing files (default: False)
            makedirs: Whether to create directories if they don't exist (default: False)
        """
        if self.SETTINGS_DATACLASS is NoneType:
            LOGGER.info(
                "%s does not have settings. Skipping settings export.",
                self.__class__.__name__,
            )
            return

        content = self.settings.to_str(
            format_type=format_type,
            output_dir=output_dir,
            detailed=False,
            exist_ok=exist_ok,
        )
        filepath = output_dir / f"{self.__class__.__name__.lower()}_settings.txt"
        export_string(content, filepath=filepath, exist_ok=exist_ok, makedirs=makedirs)

    def _update_nested_attribute(self, path, value):
        """
        Update a nested attribute using dot notation.

        Args:
            path: Dot-separated path to the attribute (e.g., "optimizer.params.lr")
            value: New value to set
        """
        attrs = path.split(".")
        current = self._settings

        for attr in attrs[:-1]:
            if not hasattr(current, attr):
                raise AttributeError(f"Invalid nested attribute `{attr}` in `{path}`")
            current = getattr(current, attr)

        last_attr = attrs[-1]
        if not hasattr(current, last_attr):
            raise AttributeError(f"Invalid final attribute `{last_attr}` in `{path}`")

        if dataclasses.is_dataclass(current):
            setattr(current, last_attr, value)
            current = dataclasses.replace(current, **{last_attr: value})
        else:
            setattr(current, last_attr, value)

    def _check_settings_type(self, settings=None):
        """
        Validate settings type and convert dict to proper settings instance if needed.
        """
        # Handle NoneType class (no settings)
        if self.SETTINGS_DATACLASS is NoneType:
            LOGGER.info(
                "%s does not support settings. Returning None.", self.__class__.__name__
            )
            return None

        if isinstance(settings, dict):
            try:
                settings = self.SETTINGS_DATACLASS(**settings)  # pylint: disable=E1102
            except (TypeError, ValueError) as err:
                raise TypeError(f"Invalid settings dictionary: {err}") from err

        if not isinstance(settings, self.SETTINGS_DATACLASS):  # pylint: disable=W1116
            raise TypeError(
                f"Invalid settings type: {type(settings).__name__}. "
                f"Expected: {self.SETTINGS_DATACLASS.__name__}"
            )

        return settings

    def _trigger_post_init(self):
        """Trigger post_init if available on the settings."""
        if hasattr(self._settings, "__post_init__"):
            self._settings.__post_init__()
