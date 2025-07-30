#!/usr/bin/env python3
"""Unit tests for workflow sink components."""

import tempfile
import unittest
from pathlib import Path
from pydantic.dataclasses import dataclass

from pypassist.dataclass.decorators.viewer import viewer
from pypassist.runner.workenv.mixin.sink import SinkMixin
from pypassist.mixin.settings import SettingsMixin
from pypassist.utils.export import export_string
from pypassist.runner.workenv.mixin.exceptions import InvalidConsumeSignatureError
from pypassist.utils.kwargs import validate_kwargs_signature


class TestSink(unittest.TestCase):
    """Test cases for workflow sink components."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def test_basic_sink(self):
        """Test basic sink functionality."""

        @viewer
        @dataclass
        class FileSinkSettings:
            """Settings for file sink."""

            filename: str = "output.txt"
            append: bool = False

        class FileSink(SettingsMixin, SinkMixin):
            """A simple sink that writes data to a file."""

            SETTINGS_DATACLASS = FileSinkSettings

            def __init__(self, settings=None):
                if settings is None:
                    settings = FileSinkSettings()
                SettingsMixin.__init__(self, settings)
                SinkMixin.__init__(self)
                self.consumed_data = None

            def consume(
                self, data=None, export=False, output_dir=None, exist_ok=True, **kwargs
            ):
                """Consume the input data.

                Args:
                    data: The data to consume
                    export: Whether to export the results
                    output_dir: Directory to export results to
                    exist_ok: Whether to overwrite existing files
                    **kwargs: Additional keyword arguments

                Returns:
                    None
                """
                if data is None:
                    raise ValueError("Data parameter is required")

                self.consumed_data = data

                if export and output_dir:
                    # Save the data to a file
                    filepath = output_dir / self.settings.filename
                    mode = "a" if self.settings.append else "w"
                    filepath.parent.mkdir(parents=True, exist_ok=True)

                    with open(filepath, mode, encoding="utf-8") as f:
                        f.write(str(data) + "\n")

                    # Export settings
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

        # Test basic consumption
        sink = FileSink()
        sink.consume(data="Test data")
        self.assertEqual(sink.consumed_data, "Test data")

        # Test with custom settings
        settings = FileSinkSettings(filename="custom.txt", append=True)
        sink = FileSink(settings)
        sink.consume(data="Line 1", export=True, output_dir=self.output_dir)
        sink.consume(data="Line 2", export=True, output_dir=self.output_dir)

        # Verify exported files
        output_file = self.output_dir / "custom.txt"
        settings_file = self.output_dir / "filesink_settings.txt"
        self.assertTrue(output_file.exists())
        self.assertTrue(settings_file.exists())
        self.assertEqual(output_file.read_text(), "Line 1\nLine 2\n")

        # Test asset generation
        asset_func = sink.get_assetable_func()
        asset_func(data="Asset data", export=True, output_dir=self.output_dir)
        self.assertEqual(sink.consumed_data, "Asset data")
        self.assertEqual(output_file.read_text(), "Line 1\nLine 2\nAsset data\n")

    def test_consume_signature_validation(self):
        """Test consume signature validation."""

        # Test with valid signature
        class ValidSink(SinkMixin):
            """A sink with a valid consume signature."""

            def __init__(self):
                SinkMixin.__init__(self)
                self.consumed_data = None

            def consume(self, data=None, export=False, output_dir=None, exist_ok=True):
                """Consume with valid signature including all required parameters.

                Args:
                    data: The data to consume
                    export: Whether to export the results
                    output_dir: Directory to export results to
                    exist_ok: Whether to overwrite existing files
                """
                self.consumed_data = data

        # This should work fine
        sink = ValidSink()
        asset_func = sink.get_assetable_func()
        asset_func(
            data="Test data", export=True, output_dir=self.output_dir, exist_ok=True
        )
        self.assertEqual(sink.consumed_data, "Test data")

        # Test with invalid signature
        class InvalidSink:
            """A class with an invalid consume signature."""

            def __init__(self):
                pass

            def consume(self, data):
                """Consume method missing required parameters."""
                pass

        # This should raise InvalidConsumeSignatureError
        invalid_sink = InvalidSink()
        with self.assertRaises(InvalidConsumeSignatureError):
            validate_kwargs_signature(
                obj=invalid_sink,
                method_name="consume",
                required_params=["export", "output_dir", "exist_ok"],
                exception_type=InvalidConsumeSignatureError,
            )

    def test_missing_required_params(self):
        """Test that missing required parameters raises an error."""

        class PartialSink(SinkMixin):
            """A sink with a partially valid signature."""

            def __init__(self):
                SinkMixin.__init__(self)

            def consume(self, data=None, export=False):
                """Consume method missing some required parameters.

                Args:
                    data: The data to consume
                    export: Whether to export the results
                """
                pass

        sink = PartialSink()
        with self.assertRaises(InvalidConsumeSignatureError):
            sink.get_assetable_func()


if __name__ == "__main__":
    unittest.main()
