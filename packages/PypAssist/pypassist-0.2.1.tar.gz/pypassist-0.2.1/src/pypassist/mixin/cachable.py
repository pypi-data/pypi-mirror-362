#!/usr/bin/env python3
"""
Base class for all classes with cachable methods.
Cacheable inherits from jrai_common_mixins.cachable. 
In addition, it provides instance-level caching control.
"""

import dataclasses
import logging
import functools
import threading
from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic.types import PositiveInt
from jrai_common_mixins.cachable import Cachable as BaseCachable

from ..dataclass.decorators.exportable.decorator import exportable

LOGGER = logging.getLogger(__name__)


@dataclass
class TimeOut:
    """
    Configuration for timeout.

    Attributes:
        seconds (int): Timeout in seconds.
        minutes (int): Timeout in minutes.
        hours (int): Timeout in hours.
        days (int): Timeout in days.
    """

    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0

    def __bool__(self):
        """
        Check if the timeout is zero.
        """
        return not all(
            (self.seconds == 0, self.minutes == 0, self.hours == 0, self.days == 0)
        )


@exportable(stem_file="caching")
@dataclass
class CacheConfig:
    """
    Configuration for caching.

    Attributes:
        active (bool): Activates or deactivates caching.
        timeout (TimeOut): Timeout for cache items. If zero, no timeout applies.
        timeout_by_atime (bool): Whether to use atime or mtime for cache timeout.
        check_interval (PositiveInt): Interval to check for cache timeouts.
        cm_maxsize (Optional[int]): Max number of items in the cache to maintain.
    """

    active: bool = True
    timeout: TimeOut = dataclasses.field(default_factory=TimeOut)
    timeout_by_atime: bool = True
    check_interval: PositiveInt = 3600  # in seconds = 1 hour
    cm_maxsize: Optional[int] = None

    def __post_init__(self):
        if isinstance(self.timeout, dict):
            self.timeout = TimeOut(**self.timeout)  # pylint: disable=not-a-mapping

    def apply_to_environment(self):
        """
        Apply the configuration in my environment.
        """
        # pylint: disable=protected-access
        Cachable._update_global_cache_config(self)


class Cachable(BaseCachable):
    """
    A mixin that adds both global and instance-specific cache control.
    Inherits from jrai_common_mixins.cachable.
    """

    _GLOBAL_CACHE_CONFIG = CacheConfig()

    def __init__(self):
        """
        Initialize cache configuration for this instance.
        Instance-level settings are set to None by default,
        meaning the global settings will be used.
        """
        super().__init__()
        self._cache_config = None
        self._cleaner_thread = None
        self._cleaner_thread_stop_event = threading.Event()

        # Start cache cleaner if needed
        if self.is_cache_active() and self.cache_config.timeout:
            LOGGER.debug("Starting cache cleaner for instance.")
            self._start_cache_cleaner()

    def is_cache_active(self):
        """
        Returns True if caching is active.
        """
        return self.cache_config.active

    @property
    def cache_config(self):
        """
        Returns the cache configuration for this instance.
        """
        if self._cache_config is None:
            self._cache_config = self._GLOBAL_CACHE_CONFIG
        return self._cache_config

    @cache_config.setter
    def cache_config(self, cache_config):
        """
        Set the cache configuration for this instance.
        """
        if not isinstance(cache_config, CacheConfig):
            raise ValueError(f"Invalid cache config: {cache_config!r}")
        self._cache_config = cache_config
        self._manage_cache_cleaner_thread()

    def activate_cache(self):
        """
        Enable caching specifically for this instance.
        """
        self._cache_config.active = True
        self._manage_cache_cleaner_thread()

    def deactivate_cache(self):
        """
        Disable caching specifically for this instance.
        """
        self._cache_config.active = False
        self._stop_cache_cleaner()
        self.clear_cache()

    def _manage_cache_cleaner_thread(self):
        """
        Restarts the cleaner thread based on instance or global settings.
        """
        if self.is_cache_active() and self.cache_config.timeout:
            self._restart_cache_cleaner()
        else:
            self._stop_cache_cleaner()

    def _start_cache_cleaner(self):
        """
        Start a background thread to clear old cache entries.
        """
        if self._cleaner_thread and self._cleaner_thread.is_alive():
            return  # The thread is already running

        self._cleaner_thread_stop_event.clear()

        def cleaner():
            while not self._cleaner_thread_stop_event.is_set():
                threading.Event().wait(self.cache_config.check_interval)
                if self.cache_config.timeout:
                    LOGGER.debug("Timeout reached. Clearing old cache entries.")
                    self.clear_old_cache_entries(
                        by_atime=self.cache_config.timeout_by_atime,
                        **self.cache_config.timeout.__dict__,
                    )

        self._cleaner_thread = threading.Thread(target=cleaner, daemon=True)
        self._cleaner_thread.start()

    def _stop_cache_cleaner(self):
        """
        Stops the cache cleaner thread for this instance.
        """
        if self._cleaner_thread and self._cleaner_thread.is_alive():
            self._cleaner_thread_stop_event.set()
            self._cleaner_thread.join()

    def _restart_cache_cleaner(self):
        """
        Stop and restart the cache cleaner thread based on updated settings.
        """
        self._stop_cache_cleaner()
        self._start_cache_cleaner()

    @classmethod
    def caching_property(cls, method):
        """
        Decorator to cache the result of a property.
        Based on the caching_property implemented in jrai_common_mixins.cachable
        """

        @property
        @functools.wraps(method)
        def wrapper(self):
            if self.is_cache_active():
                return super().caching_property(method).fget(self)
            return method(self)

        return wrapper

    @classmethod
    def caching_method(cls, *arg_cmps, _cm_maxsize=None, **kwarg_cmps):
        """
        Decorator to cache the result of a method.
        Based on the caching_method implemented in jrai_common_mixins.cachable.
        """

        def decorator(method):
            @functools.wraps(method)
            def cmeth(self, *args, **kwargs):
                cache_activ = self.is_cache_active()
                if cache_activ:
                    cm_maxsize = (
                        _cm_maxsize
                        if _cm_maxsize is not None
                        else self.cache_config.cm_maxsize
                    )
                    return super().caching_method(
                        *arg_cmps, _cm_maxsize=cm_maxsize, **kwarg_cmps
                    )(method)(self, *args, **kwargs)
                return method(self, *args, **kwargs)

            return cmeth

        return decorator

    @classmethod
    def _update_global_cache_config(cls, config):
        """
        Update the global cache configuration.
        """
        cls._GLOBAL_CACHE_CONFIG = config
