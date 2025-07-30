#!/usr/bin/env python3
"""Unit tests for workflow source components."""

import tempfile
import unittest
from pathlib import Path
from pydantic.dataclasses import dataclass

from pypassist.dataclass.decorators.viewer import viewer
from pypassist.runner.workenv.mixin.source import SourceMixin
from pypassist.mixin.settings import SettingsMixin
from pypassist.utils.export import export_string
from pypassist.runner.workenv.mixin.exceptions import InvalidProvideSignatureError
from pypassist.utils.kwargs import validate_kwargs_signature


class TestSource(unittest.TestCase):
    """Test cases for workflow source components."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

        # Create a test file for file source
        self.test_file = Path(self.temp_dir) / "test_input.txt"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("line1\nline2\nline3\n")

    def test_basic_source(self):
        """Test basic source functionality."""

        @viewer
        @dataclass
        class FileSourceSettings:
            """Settings for file source."""

            filename: str = "input.txt"
            strip_lines: bool = True

        class FileSource(SettingsMixin, SourceMixin):
            """A simple source that reads data from a file."""

            SETTINGS_DATACLASS = FileSourceSettings

            def __init__(self, settings=None):
                if settings is None:
                    settings = FileSourceSettings()
                SettingsMixin.__init__(self, settings)
                SourceMixin.__init__(self)

            def provide(
                self,
                filepath=None,
                export=False,
                output_dir=None,
                exist_ok=True,
                **kwargs,
            ):
                """Provide data from a file.

                Args:
                    filepath: Path to the file to read (overrides settings.filename)
                    export: Whether to export the results
                    output_dir: Directory to export results to
                    exist_ok: Whether to overwrite existing files
                    **kwargs: Additional keyword arguments

                Returns:
                    The file contents as a list of lines
                """
                if filepath is None:
                    raise ValueError("Filepath parameter is required")

                # Read the file
                with open(filepath, "r", encoding="utf-8") as f:
                    if self.settings.strip_lines:
                        lines = [line.strip() for line in f.readlines()]
                    else:
                        lines = f.readlines()

                if export and output_dir:
                    # Export the data
                    result_content = "\n".join([line.strip() for line in lines])
                    result_filepath = (
                        output_dir / f"{self.__class__.__name__.lower()}_result.txt"
                    )
                    export_string(
                        result_content,
                        filepath=result_filepath,
                        exist_ok=exist_ok,
                        makedirs=True,
                    )

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

                return lines

        # Test basic source
        source = FileSource()
        lines = source.provide(filepath=self.test_file)
        self.assertEqual(lines, ["line1", "line2", "line3"])

        # Test with custom settings
        settings = FileSourceSettings(strip_lines=False)
        source = FileSource(settings)
        lines = source.provide(filepath=self.test_file)
        self.assertEqual(lines, ["line1\n", "line2\n", "line3\n"])

        # Test asset generation
        asset_func = source.get_assetable_func()
        result = asset_func(
            filepath=self.test_file, export=True, output_dir=self.output_dir
        )
        self.assertEqual(result, ["line1\n", "line2\n", "line3\n"])

        # Verify exported files
        result_file = self.output_dir / "filesource_result.txt"
        settings_file = self.output_dir / "filesource_settings.txt"
        self.assertTrue(result_file.exists())
        self.assertTrue(settings_file.exists())
        self.assertEqual(result_file.read_text(), "line1\nline2\nline3")

    def test_provide_signature_validation(self):
        """Test provide signature validation."""

        # Test with valid signature
        class ValidSource(SourceMixin):
            """A source with a valid provide signature."""

            def __init__(self):
                SourceMixin.__init__(self)

            def provide(self, data=None, export=False, output_dir=None, exist_ok=True):
                """Provide with valid signature including all required parameters.

                Args:
                    data: The data to provide
                    export: Whether to export the results
                    output_dir: Directory to export results to
                    exist_ok: Whether to overwrite existing files

                Returns:
                    The provided data
                """
                return data

        # This should work fine
        source = ValidSource()
        asset_func = source.get_assetable_func()
        result = asset_func(
            data="Test data", export=True, output_dir=self.output_dir, exist_ok=True
        )
        self.assertEqual(result, "Test data")

        # Test with invalid signature
        class InvalidSource:
            """A class with an invalid provide signature."""

            def __init__(self):
                pass

            def provide(self, data):
                """Provide method missing required parameters."""
                return data

        # This should raise InvalidProvideSignatureError
        invalid_source = InvalidSource()
        with self.assertRaises(InvalidProvideSignatureError):
            validate_kwargs_signature(
                obj=invalid_source,
                method_name="provide",
                required_params=["export", "output_dir", "exist_ok"],
                exception_type=InvalidProvideSignatureError,
            )

    def test_missing_required_params(self):
        """Test that missing required parameters raises an error."""

        class PartialSource(SourceMixin):
            """A source with a partially valid signature."""

            def __init__(self):
                SourceMixin.__init__(self)

            def provide(self, data=None, export=False):
                """Provide method missing some required parameters.

                Args:
                    data: The data to provide
                    export: Whether to export the results

                Returns:
                    The provided data
                """
                return data

        source = PartialSource()
        with self.assertRaises(InvalidProvideSignatureError):
            source.get_assetable_func()


if __name__ == "__main__":
    unittest.main()
