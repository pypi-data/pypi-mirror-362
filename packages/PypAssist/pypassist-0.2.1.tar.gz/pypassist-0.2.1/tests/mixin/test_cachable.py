#!/usr/bin/env python3
"""
Test cachable.py.
"""


import unittest
import time
import random
import logging
import datetime
from pypassist.mixin.cachable import Cachable, CacheConfig

# Comments:
# freezegun does not work with deamon threads
# that's why we use time.sleep instead of freezegun


class MyCachable(Cachable):
    """
    Test subclass for Cachable to use in unit tests.
    """

    @Cachable.caching_property
    def cached_property(self):
        """
        Dummy caching property.
        Returns the current UTC time.
        """
        return datetime.datetime.now(datetime.timezone.utc)

    @Cachable.caching_method()
    def cached_method(self, x, y=0):
        """
        Dummy caching method.
        Returns the sum of x and y and a random number.
        """
        z = random.random()
        return x + y + z


class TestCachable(unittest.TestCase):
    """
    Test Cachable class.
    """

    def setUp(self):
        """Initialize for each test."""
        self.instance = MyCachable()
        ## reset the cache settings
        self.instance.cache_config = CacheConfig()

    def test_cached_property(self):
        """Test the caching of the cached_property."""
        value1 = self.instance.cached_property
        value2 = self.instance.cached_property
        self.assertEqual(value1, value2)  # The property should return the cached value

    def test_cached_method(self):
        """Test the caching of the cached_method."""
        result1 = self.instance.cached_method(3, 4)
        result2 = self.instance.cached_method(3, 4)  # Should hit the cache
        self.assertEqual(result1, result2)  # Should return the same result from cache

    # ------------------- Test the cache settings ------------------------------

    def test_cache_enabled_for_property(self):
        """Test enabling and disabling the cache for the cached_property."""
        # Disable caching
        self.instance.deactivate_cache()
        result1 = self.instance.cached_property  # This should not be cached
        result2 = self.instance.cached_property  # This should compute again
        self.assertNotEqual(result1, result2)  # Results should differ

        # Enable caching again
        self.instance.activate_cache()
        result3 = self.instance.cached_property  # This should be cached
        result4 = self.instance.cached_property  # This should hit the cache
        self.assertEqual(result3, result4)  # Results should be the same

    def test_cache_enabled_for_method(self):
        """Test enabling and disabling the cache for the cached_property."""
        # Disable caching
        self.instance.deactivate_cache()
        result1 = self.instance.cached_method(10, 10)  # This should not be cached
        result2 = self.instance.cached_method(10, 10)  # This should compute again
        self.assertNotEqual(result1, result2)  # Results should differ

        # Enable caching again
        self.instance.activate_cache()
        result3 = self.instance.cached_method(10, 12)  # This should be cached
        result4 = self.instance.cached_method(10, 12)  # This should hit the cache
        self.assertEqual(result3, result4)  # Results should be the same

    def test_cache_timeout_for_property(self):
        """Test setting the check interval for the cache cleaner."""
        # pylint: disable=protected-access
        self.instance.cache_config = CacheConfig(
            check_interval=1, timeout={"seconds": 1}
        )
        result1 = self.instance.cached_property  # Cache this result
        result2 = self.instance.cached_property  # Should hit the cache
        self.assertEqual(result1, result2)  # Results should be the same
        time.sleep(3)  # Wait for the cache to expire
        result3 = self.instance.cached_property
        self.assertNotEqual(result1, result3)  # Results should differ

    def test_cache_timeout_for_method(self):
        """Test setting a cache timeout."""
        # pylint: disable=protected-access
        self.instance.cache_config = CacheConfig(
            check_interval=1, timeout={"seconds": 1}
        )
        result1 = self.instance.cached_method(10, 10)  # This should cache the result
        result2 = self.instance.cached_method(10, 10)  # This should hit the cache
        self.assertEqual(result1, result2)  # Results should be the same
        time.sleep(3)  # Wait for the cache to expire
        result3 = self.instance.cached_method(10, 10)  # This should compute again
        self.assertNotEqual(result1, result3)

    # ------------------- Test GLOBAL cache settings ------------------------------

    def test_global_cache_config_update(self):
        """Test setting a cache timeout."""
        CacheConfig(active=False).apply_to_environment()
        tc = MyCachable()
        self.assertFalse(tc.is_cache_active())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
