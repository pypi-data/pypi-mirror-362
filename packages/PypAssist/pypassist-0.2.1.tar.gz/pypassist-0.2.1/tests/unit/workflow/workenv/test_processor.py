#!/usr/bin/env python3
"""Unit tests for workflow processor components."""

import tempfile
import unittest
from pathlib import Path
from pydantic.dataclasses import dataclass

from pypassist.dataclass.decorators.viewer import viewer
from pypassist.runner.workenv.mixin.processor import ProcessorMixin
from pypassist.mixin.settings import SettingsMixin
from pypassist.utils.export import export_string
from pypassist.runner.workenv.mixin.exceptions import InvalidProcessSignatureError
from pypassist.utils.kwargs import validate_kwargs_signature


class TestProcessor(unittest.TestCase):
    """Test cases for workflow processor components."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def test_basic_processor(self):
        """Test basic processor functionality."""

        @viewer
        @dataclass
        class ProcessorSettings:
            """Settings for test processor."""

            multiplier: int = 2

        class BasicProcessor(SettingsMixin, ProcessorMixin):
            """A simple processor that multiplies input by a factor."""

            SETTINGS_DATACLASS = ProcessorSettings

            def __init__(self, settings=None):
                if settings is None:
                    settings = ProcessorSettings()
                SettingsMixin.__init__(self, settings)
                ProcessorMixin.__init__(self)

            def process(
                self, value=None, export=False, output_dir=None, exist_ok=True, **kwargs
            ):
                """Process the input value.

                Args:
                    value: The value to process
                    export: Whether to export the results
                    output_dir: Directory to export results to
                    exist_ok: Whether to overwrite existing files
                    **kwargs: Additional keyword arguments

                Returns:
                    The processed value
                """
                if value is None:
                    raise ValueError("Value parameter is required")

                result = value * self.settings.multiplier

                if export and output_dir:
                    filepath = (
                        output_dir / f"{self.__class__.__name__.lower()}_result.txt"
                    )
                    export_string(
                        str(result), filepath=filepath, exist_ok=exist_ok, makedirs=True
                    )

                    settings_content = self.settings.to_str(format_type="yaml")
                    settings_filepath = (
                        output_dir / f"{self.__class__.__name__.lower()}_settings.txt"
                    )
                    export_string(
                        settings_content,
                        filepath=settings_filepath,
                        exist_ok=exist_ok,
                        makedirs=True,
                    )

                return result

        # Test basic processing
        processor = BasicProcessor()
        self.assertEqual(processor.process(value=5), 10)

        # Test with custom settings
        settings = ProcessorSettings(multiplier=3)
        processor = BasicProcessor(settings)
        self.assertEqual(processor.process(value=5), 15)

        # Test asset generation
        asset_func = processor.get_assetable_func()
        result = asset_func(value=5, export=True, output_dir=self.output_dir)
        self.assertEqual(result, 15)

        # Verify exported files
        result_file = self.output_dir / "basicprocessor_result.txt"
        settings_file = self.output_dir / "basicprocessor_settings.txt"
        self.assertTrue(result_file.exists())
        self.assertTrue(settings_file.exists())
        self.assertEqual(result_file.read_text(), "15")

    def test_process_signature_validation(self):
        """Test process signature validation."""

        # Test with valid signature
        class ValidProcessor(ProcessorMixin):
            """A processor with a valid process signature."""

            def __init__(self):
                ProcessorMixin.__init__(self)

            def process(self, value=None, export=False, output_dir=None, exist_ok=True):
                """Process with valid signature including all required parameters.

                Args:
                    value: The value to process
                    export: Whether to export the results
                    output_dir: Directory to export results to
                    exist_ok: Whether to overwrite existing files

                Returns:
                    The processed value
                """
                return value * 2

        # This should work fine
        processor = ValidProcessor()
        asset_func = processor.get_assetable_func()
        result = asset_func(
            value=5, export=True, output_dir=self.output_dir, exist_ok=True
        )
        self.assertEqual(result, 10)

        # Test with invalid signature
        class InvalidProcessor:
            """A class with an invalid process signature."""

            def __init__(self):
                pass

            def process(self, value):
                """Process method missing required parameters."""
                return value * 2

        # This should raise InvalidProcessSignatureError
        invalid_processor = InvalidProcessor()
        with self.assertRaises(InvalidProcessSignatureError):
            validate_kwargs_signature(
                obj=invalid_processor,
                method_name="process",
                required_params=["export", "output_dir", "exist_ok"],
                exception_type=InvalidProcessSignatureError,
            )

    def test_missing_required_params(self):
        """Test that missing required parameters raises an error."""

        class PartialProcessor(ProcessorMixin):
            """A processor with a partially valid signature."""

            def __init__(self):
                ProcessorMixin.__init__(self)

            def process(self, value=None, export=False):
                """Process method missing some required parameters.

                Args:
                    value: The value to process
                    export: Whether to export the results

                Returns:
                    The processed value
                """
                return value * 2

        processor = PartialProcessor()
        with self.assertRaises(InvalidProcessSignatureError):
            processor.get_assetable_func()


if __name__ == "__main__":
    unittest.main()
