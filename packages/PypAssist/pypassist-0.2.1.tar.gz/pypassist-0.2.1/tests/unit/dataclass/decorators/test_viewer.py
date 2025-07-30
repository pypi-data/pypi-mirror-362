#!/usr/bin/env python3
"""Unit tests for the @viewer decorator."""

import unittest
from typing import Optional

from pydantic.dataclasses import dataclass

from pypassist.dataclass.decorators.viewer import viewer
from pypassist.dataclass.decorators.viewer.setup import ViewerSetup


class TestViewerDecorator(unittest.TestCase):
    """Test cases for the @viewer decorator functionality."""

    def test_basic_decoration(self):
        """Test basic decoration of a dataclass."""

        @viewer
        @dataclass
        class TestConfig:
            """Test configuration class."""

            name: str
            value: int
            description: Optional[str] = None

        # Create an instance
        config = TestConfig(name="test", value=42)

        # Verify instance has viewer methods
        self.assertTrue(hasattr(config, "to_info"))
        self.assertTrue(hasattr(config, "to_str"))
        self.assertTrue(hasattr(config, "serialize"))
        self.assertTrue(hasattr(config, "view"))

    def test_string_conversion(self):
        """Test conversion to string formats."""

        @viewer
        @dataclass
        class TestConfig:
            """Test configuration class."""

            name: str
            value: int

        config = TestConfig(name="test", value=42)

        # Test YAML format
        yaml_str = config.to_str(format_type="yaml")
        self.assertIsInstance(yaml_str, str)
        self.assertIn("name: test", yaml_str)
        self.assertIn("value: 42", yaml_str)

        # Test JSON format
        json_str = config.to_str(format_type="json")
        self.assertIsInstance(json_str, str)
        self.assertIn('"name": "test"', json_str)
        self.assertIn('"value": 42', json_str)

    def test_serialization(self):
        """Test serialization functionality."""

        @viewer
        @dataclass
        class TestConfig:
            """Test configuration class."""

            name: str
            value: int

        config = TestConfig(name="test", value=42)

        # Test JSON serialization
        json_obj = config.serialize(format_type="json")
        self.assertIsInstance(json_obj, dict)
        self.assertEqual(json_obj["name"], "test")
        self.assertEqual(json_obj["value"], 42)

    def test_custom_setup(self):
        """Test custom setup configuration."""
        setup = ViewerSetup(hide_private=True)

        @viewer(setup=setup)
        @dataclass
        class TestConfig:
            """Test configuration class."""

            public_field: str
            _private_field: str

        config = TestConfig(public_field="public", _private_field="private")

        # Verify private field is hidden in string representation
        yaml_str = config.to_str(format_type="yaml")
        self.assertIn("public_field:", yaml_str)
        self.assertNotIn("_private_field:", yaml_str)

    def test_invalid_setup(self):
        """Test handling of invalid setup configuration."""
        with self.assertRaises(Exception):  # Should raise specific exception

            @viewer(invalid_param="value")
            @dataclass
            class TestConfig:
                """Test configuration class."""

                field: str


if __name__ == "__main__":
    unittest.main()
