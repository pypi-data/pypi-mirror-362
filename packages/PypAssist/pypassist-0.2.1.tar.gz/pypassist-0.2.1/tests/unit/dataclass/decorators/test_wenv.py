#!/usr/bin/env python3
"""Unit tests for the @wenv decorator."""

import unittest
from typing import Dict, Any
from pydantic.dataclasses import dataclass

from pypassist.dataclass.decorators.wenv import wenv, WenvSetupError
from pypassist.dataclass.decorators.wenv.setup import WenvSetup


class TestWenvDecorator(unittest.TestCase):
    """Test cases for the @wenv decorator functionality."""

    def test_basic_decoration(self):
        """Test basic decoration of a dataclass."""

        @wenv
        @dataclass
        class NestedConfig:
            """Nested configuration class."""

            value: str

        @wenv
        @dataclass
        class TestConfig:
            """Test configuration class."""

            name: str
            settings: Dict[str, Any]
            nested: Dict[str, NestedConfig]

        # Create an instance with nested dictionary
        config = TestConfig(
            name="test",
            settings={"param": "value"},
            nested={
                "item1": NestedConfig(value="test1"),
                "item2": {"value": "test2"},  # This should be converted to NestedConfig
            },
        )

        # Verify the class is properly decorated
        self.assertTrue(hasattr(TestConfig, "_SETUP_"))
        self.assertTrue(hasattr(TestConfig, "_WENV_"))

        # Verify dictionary field processing
        self.assertIsInstance(config.nested["item1"], NestedConfig)
        self.assertIsInstance(config.nested["item2"], NestedConfig)
        self.assertEqual(config.nested["item2"].value, "test2")

    def test_invalid_setup(self):
        """Test handling of invalid setup configuration."""
        with self.assertRaises(WenvSetupError):

            @wenv(setup=123)  # Invalid setup type - should be WenvSetup instance
            @dataclass
            class TestConfig:
                """Test configuration class."""

                settings: Dict[str, Any]


if __name__ == "__main__":
    unittest.main()
