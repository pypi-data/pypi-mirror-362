#!/usr/bin/env python3
"""
Base work environment functionality.
"""

from ....dataclass.decorators.wenv.validation import is_wenv

from ..component.exceptions import InvalidComponentError


class BaseWorkEnv:
    """Base class for work environments."""

    def __init__(self, config, parent_env=None):
        self.config = config
        self._validate_config()
        self.parent_env = parent_env

    def _validate_config(self):
        if not is_wenv(self.config):
            raise ValueError(
                "Invalid work environment configuration. "
                "Expected a pydantic dataclass decorated with @wenv."
            )

    def get_component(self, path):
        """
        Get component by path.

        Args:
            path: Component path in format "section.name"

        Returns:
            Component instance

        Raises:
            ValueError: If component path is invalid or component not found
        """
        try:
            section_name, component_name = path.split(".")
        except ValueError as err:
            raise ValueError(
                f"Invalid component path: {path}. Expected format: 'section.name'"
            ) from err

        section = getattr(self, section_name)
        if component_name not in section:
            raise InvalidComponentError(
                f"{self.__class__.__name__}: Component '{component_name}' not found in section '{section_name}'. "
                f"Available components: {', '.join(section.keys())}"
            )

        return section[component_name]
