#!/usr/bin/env python3
"""Unit tests for the @exportable decorator."""
# pylint: disable=no-member, protected-access

import os
import tempfile
import unittest
from typing import Optional

from pydantic.dataclasses import dataclass

from pypassist.dataclass.decorators.exportable import exportable
from pypassist.dataclass.decorators.exportable.setup import ExportableSetup


class TestExportableDecorator(unittest.TestCase):
    """Test cases for the @exportable decorator functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def test_basic_decoration(self):
        """Test basic decoration of a dataclass."""

        @exportable
        @dataclass
        class TestConfig:
            """Test configuration class."""

            name: str
            value: int
            description: Optional[str] = None

        # Verify the class is properly decorated
        self.assertTrue(hasattr(TestConfig, "_EXPORTABLE_"))
        self.assertTrue(hasattr(TestConfig, "_EXPORT_SETUP_"))
        self.assertTrue(hasattr(TestConfig, "export"))
        self.assertTrue(hasattr(TestConfig, "view_schema"))

    def test_export_functionality(self):
        """Test schema export functionality."""

        @exportable(stem_file="test_config")
        @dataclass
        class TestConfig:
            """Test configuration class."""

            name: str
            value: int

        # Create an output path
        output_path = os.path.join(self.temp_dir, "test_output")
        os.makedirs(output_path, exist_ok=True)

        # Test YAML export
        TestConfig.export(output_path, format_type="yaml", exist_ok=True)
        yaml_file = os.path.join(output_path, "test_config.yaml")
        self.assertTrue(os.path.exists(yaml_file))

        # Test JSON export
        TestConfig.export(output_path, format_type="json", exist_ok=True)
        json_file = os.path.join(output_path, "test_config.json")
        self.assertTrue(os.path.exists(json_file))

    def test_custom_setup(self):
        """Test custom setup configuration."""
        setup = ExportableSetup(
            stem_file="custom_config", hide_private=True, strategy="default"
        )

        @exportable(setup=setup)
        @dataclass
        class TestConfig:
            """Test configuration class."""

            public_field: str
            _private_field: str

        # Verify setup is properly applied
        self.assertEqual(TestConfig._EXPORT_SETUP_.stem_file, "custom_config")
        self.assertTrue(TestConfig._EXPORT_SETUP_.hide_private)

        # Export and verify private field is hidden
        output_path = os.path.join(self.temp_dir, "custom_output")
        os.makedirs(output_path, exist_ok=True)
        TestConfig.export(output_path, format_type="yaml", exist_ok=True)

        # TODO: Add verification of exported content to ensure private field is hidden

    def test_invalid_setup(self):
        """Test handling of invalid setup configuration."""
        with self.assertRaises(Exception):  # Should raise specific exception

            @exportable(invalid_param="value")
            @dataclass
            class TestConfig:
                """Test configuration class."""

                field: str


if __name__ == "__main__":
    unittest.main()
