#!/usr/bin/env python3
"""Unit tests for custom workflow operators."""

import tempfile
import unittest
from pathlib import Path

from pydantic.dataclasses import dataclass

from pypassist.runner.workenv.custom.base.processor import CustomProcessor
from pypassist.runner.workenv.custom.base.source import CustomSource
from pypassist.dataclass.decorators.viewer import viewer
from pypassist.runner.workenv.mixin.exceptions import InvalidProcessSignatureError
from pypassist.utils.kwargs import validate_kwargs_signature


class TestCustomOperator(unittest.TestCase):
    """Test cases for custom workflow operators."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def test_basic_operator(self):
        """Test basic custom operator functionality."""

        @viewer
        @dataclass
        class ReverserSettings:
            """Settings for string reversal."""

            capitalize: bool = False

        class Reverser(CustomProcessor, register_name="reverse"):
            """A simple string reverser operator."""

            SETTINGS_DATACLASS = ReverserSettings

            def __init__(self, settings=None):
                if settings is None:
                    settings = ReverserSettings()
                CustomProcessor.__init__(self, settings)

            @classmethod
            def init_from_config(cls, config, workenv=None):
                """Initialize the component from configuration."""
                return cls(config.settings)

            def __call__(self, text):
                """Reverse the input text."""
                result = text[::-1]
                if self.settings.capitalize:
                    result = result.upper()
                return result

            def process(
                self, text=None, export=False, output_dir=None, exist_ok=True, **kwargs
            ):
                """Process the text and return the processed text.

                Args:
                    text: The text to process
                    export: Whether to export the results
                    output_dir: Directory to export results to
                    exist_ok: Whether to overwrite existing files
                    **kwargs: Additional keyword arguments

                Returns:
                    The processed text
                """
                if text is None:
                    raise ValueError("Text parameter is required")

                result = self(text)
                if export and output_dir:
                    # Export result
                    result_file = output_dir / f"{self.__class__.__name__.lower()}.txt"
                    result_file.parent.mkdir(parents=True, exist_ok=exist_ok)
                    result_file.write_text(result)

                    # Export settings
                    settings_str = self.settings.to_str(format_type="yaml")
                    settings_file = (
                        output_dir / f"{self.__class__.__name__.lower()}_settings.txt"
                    )
                    settings_file.write_text(settings_str)
                return result

        # Test basic operation
        reverser = Reverser(ReverserSettings(capitalize=False))
        self.assertEqual(reverser("hello"), "olleh")

        # Test with settings
        reverser = Reverser(ReverserSettings(capitalize=True))
        self.assertEqual(reverser("hello"), "OLLEH")

        # Test asset generation
        asset_func = reverser.get_assetable_func()
        result = asset_func(text="hello", export=True, output_dir=self.output_dir)
        self.assertEqual(result, "OLLEH")

        # Verify exported files
        result_file = self.output_dir / "reverser.txt"
        settings_file = self.output_dir / "reverser_settings.txt"
        self.assertTrue(result_file.exists())
        self.assertTrue(settings_file.exists())
        self.assertEqual(result_file.read_text(), "OLLEH")

    def test_operator_registration(self):
        """Test operator registration and retrieval."""

        @viewer
        @dataclass
        class DummySettings:
            """Dummy settings."""

            value: str = "test"

        class DummyOperator(CustomSource, register_name="dummy"):
            """A dummy operator for testing registration."""

            SETTINGS_DATACLASS = DummySettings

            def __init__(self, settings=None):
                if settings is None:
                    settings = DummySettings()
                CustomSource.__init__(self, settings)

            @classmethod
            def init_from_config(cls, config, workenv=None):
                """Initialize the component from configuration."""
                return cls(config.settings)

            def __call__(self, text):
                return f"{text}_{self.settings.value}"

            def provide(self, **kwargs):
                """Provide data with flexible signature.

                Args:
                    **kwargs: Arbitrary keyword arguments including:
                        - text: The text to provide
                        - export: Whether to export the results
                        - output_dir: Directory to export results to
                        - exist_ok: Whether to overwrite existing files

                Returns:
                    The provided data
                """
                text = kwargs.get("text")
                if text is None:
                    raise ValueError("Text parameter is required")
                return self(text)

        # Verify registration
        self.assertTrue(hasattr(DummyOperator, "_REGISTER"))
        self.assertIn("dummy", DummyOperator._REGISTER)

        # Test operator retrieval
        retrieved = CustomSource.get_registered("dummy")
        self.assertEqual(retrieved, DummyOperator)

        # Test operator functionality
        operator = DummyOperator()
        self.assertEqual(operator("input"), "input_test")

    def test_invalid_operator(self):
        """Test handling of invalid operator configurations."""
        with self.assertRaises(TypeError):
            # Missing required methods
            class InvalidOperator(CustomSource, register_name="invalid"):
                """An invalid operator missing required methods."""

                pass

            # This should raise TypeError due to missing required methods
            # pylint: disable=abstract-class-instantiated
            # pylint: disable=no-value-for-parameter
            InvalidOperator()

    def test_process_signature_validation(self):
        """Test process signature validation."""

        @viewer
        @dataclass
        class SignatureSettings:
            """Settings for signature testing."""

            value: str = "test"

        # Test with valid signature
        class ValidProcessor(CustomProcessor, register_name="valid_processor"):
            """A processor with a valid process signature."""

            SETTINGS_DATACLASS = SignatureSettings

            def __init__(self, settings=None):
                if settings is None:
                    settings = SignatureSettings()
                CustomProcessor.__init__(self, settings)

            @classmethod
            def init_from_config(cls, config, workenv=None):
                """Initialize the component from configuration."""
                return cls(config.settings)

            def __call__(self, text):
                return f"{text}_{self.settings.value}"

            def process(self, text, export=False, output_dir=None, exist_ok=True):
                """Process with valid signature including all required parameters.

                Args:
                    text: The text to process
                    export: Whether to export the results
                    output_dir: Directory to export results to
                    exist_ok: Whether to overwrite existing files

                Returns:
                    The processed text
                """
                result = self(text)
                if export and output_dir:
                    result_file = output_dir / f"{self.__class__.__name__.lower()}.txt"
                    result_file.parent.mkdir(parents=True, exist_ok=exist_ok)
                    result_file.write_text(result)
                return result

        # This should work fine
        processor = ValidProcessor()
        asset_func = processor.get_assetable_func()
        result = asset_func(
            text="hello", export=True, output_dir=self.output_dir, exist_ok=True
        )
        self.assertEqual(result, "hello_test")

        # Test with invalid signature
        class InvalidProcessor:
            """A class with an invalid process signature."""

            def __init__(self):
                pass

            def process(self, text):
                """Process method missing required parameters."""
                return text

        # This should raise InvalidProcessSignatureError
        invalid_processor = InvalidProcessor()
        with self.assertRaises(InvalidProcessSignatureError):
            validate_kwargs_signature(
                obj=invalid_processor,
                method_name="process",
                required_params=["export", "output_dir", "exist_ok"],
                exception_type=InvalidProcessSignatureError,
            )


if __name__ == "__main__":
    unittest.main()
