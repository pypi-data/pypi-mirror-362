#!/usr/bin/env python3
"""
Configuration for custom components.
"""

import dataclasses
from typing import Optional

from .....utils.typing import ParamDict


@dataclasses.dataclass
class CustomConfig:
    """Configuration for custom components."""

    name: str
    settings: Optional[ParamDict] = None

    def get_component(self, workenv=None):
        """Get processor instance.

        Args:
            workenv: Optional work environment instance

        Returns:
            An instance of the processor
        """
        # pylint: disable=no-member
        return self._REG_BASE_CLASS_.get_registered(self.name).init_from_config(
            self, workenv=workenv
        )
