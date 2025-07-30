#!/usr/bin/env python3
"""
Custom work environment.
"""

from ...workenv.base.workenv import BaseWorkEnv
from ....mixin.cachable import Cachable


class CustomWorkEnv(BaseWorkEnv, Cachable):
    """Custom work environment."""

    def __init__(self, config, parent_env=None):
        BaseWorkEnv.__init__(self, config, parent_env)
        Cachable.__init__(self)

    @Cachable.caching_property
    def sinks(self):
        """
        The dict of instantiated custom sinks.
        """
        return self._get_custom_components("sinks")

    @Cachable.caching_property
    def sources(self):
        """
        The dict of instantiated custom sources.
        """
        return self._get_custom_components("sources")

    @Cachable.caching_property
    def processors(self):
        """
        The dict of instantiated custom processors.
        """
        return self._get_custom_components("processors")

    def _get_custom_components(self, section_name):
        """
        Get custom components from nested sections.
        """
        section = getattr(self.config, section_name)
        return {
            name: conf.get_component(workenv=self.parent_env)
            for (name, conf) in section.items()
        }
