"""
Tests for the CLI module.
"""

import os
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from src.prepo.cli import create_parser, main, process_file, validate_args


class TestCLI(unittest.TestCase):
    """Test cases for the CLI functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

        # Create test data
        self.test_data = {
            "numeric_col": [1, 2, 3, 4, 5],
            "price_USD": [10.5, 20.3, 30.1, 40.9, 50.2],
            "percentage": [0.1, 0.2, 0.3, 0.4, 0.5],
            "category": ["A", "B", "A", "C", "B"],
        }
        self.df = pd.DataFrame(self.test_data)

        # Create test input file
        self.input_path = os.path.join(self.temp_dir, "test_input.csv")
        self.df.to_csv(self.input_path, index=False)

        self.output_path = os.path.join(self.temp_dir, "test_output.csv")

    def tearDown(self):
        """Clean up test files."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_parser(self):
        """Test argument parser creation."""
        parser = create_parser()

        # Test basic arguments
        args = parser.parse_args([self.input_path, self.output_path])
        self.assertEqual(args.input, self.input_path)
        self.assertEqual(args.output, self.output_path)
        self.assertEqual(args.scaler, "standard")  # default
        self.assertFalse(args.keep_na)  # default
        self.assertFalse(args.no_outliers)  # default
        self.assertFalse(args.polars)  # default
        self.assertFalse(args.pyarrow)  # default
        self.assertFalse(args.info)  # default

    def test_parser_with_options(self):
        """Test parser with various options."""
        parser = create_parser()

        # Test with all options
        args = parser.parse_args(
            [
                self.input_path,
                self.output_path,
                "--scaler",
                "robust",
                "--keep-na",
                "--no-outliers",
                "--polars",
                "--pyarrow",
                "--info",
                "--input-format",
                "csv",
                "--output-format",
                "json",
            ]
        )

        self.assertEqual(args.scaler, "robust")
        self.assertTrue(args.keep_na)
        self.assertTrue(args.no_outliers)
        self.assertTrue(args.polars)
        self.assertTrue(args.pyarrow)
        self.assertTrue(args.info)
        self.assertEqual(args.input_format, "csv")
        self.assertEqual(args.output_format, "json")

    def test_parser_scaler_choices(self):
        """Test that parser accepts valid scaler choices."""
        parser = create_parser()

        valid_scalers = ["standard", "robust", "minmax", "none"]
        for scaler in valid_scalers:
            args = parser.parse_args([self.input_path, self.output_path, "--scaler", scaler])
            self.assertEqual(args.scaler, scaler)

    def test_parser_format_choices(self):
        """Test that parser accepts valid format choices."""
        parser = create_parser()

        valid_formats = ["csv", "json", "excel", "xlsx", "xls", "parquet", "feather", "pickle", "tsv", "orc"]

        for fmt in valid_formats:
            args = parser.parse_args([self.input_path, self.output_path, "--input-format", fmt, "--output-format", fmt])
            self.assertEqual(args.input_format, fmt)
            self.assertEqual(args.output_format, fmt)

    def test_validate_args_valid_input(self):
        """Test validation with valid arguments."""
        parser = create_parser()
        args = parser.parse_args([self.input_path, self.output_path])

        # Should not raise any exception
        try:
            validate_args(args)
        except SystemExit:
            self.fail("validate_args raised SystemExit unexpectedly")

    def test_validate_args_missing_input(self):
        """Test validation with missing input file."""
        parser = create_parser()
        missing_input = os.path.join(self.temp_dir, "missing.csv")
        args = parser.parse_args([missing_input, self.output_path])

        with patch("sys.stderr", new_callable=StringIO):
            with self.assertRaises(SystemExit):
                validate_args(args)

    def test_validate_args_missing_output_directory(self):
        """Test validation with missing output directory."""
        parser = create_parser()
        missing_dir_output = "/nonexistent/directory/output.csv"
        args = parser.parse_args([self.input_path, missing_dir_output])

        with patch("sys.stderr", new_callable=StringIO):
            with self.assertRaises(SystemExit):
                validate_args(args)

    @patch("builtins.print")
    def test_process_file_basic(self, mock_print):
        """Test basic file processing."""
        parser = create_parser()
        args = parser.parse_args([self.input_path, self.output_path])

        # Should not raise any exception
        process_file(args)

        # Check that output file was created
        self.assertTrue(os.path.exists(self.output_path))

        # Check that file contains processed data
        result_df = pd.read_csv(self.output_path)
        self.assertEqual(len(result_df), len(self.df))

    @patch("builtins.print")
    def test_process_file_with_options(self, mock_print):
        """Test file processing with various options."""
        parser = create_parser()

        # Test with robust scaler and keep NA
        args = parser.parse_args([self.input_path, self.output_path, "--scaler", "robust", "--keep-na", "--no-outliers"])

        process_file(args)

        # Check that output file was created
        self.assertTrue(os.path.exists(self.output_path))

    @patch("builtins.print")
    def test_process_file_with_info(self, mock_print):
        """Test file processing with info flag."""
        parser = create_parser()
        args = parser.parse_args([self.input_path, self.output_path, "--info"])

        process_file(args)

        # Check that print was called (info should be displayed)
        self.assertTrue(mock_print.called)

        # Check for specific info messages
        call_args = []
        for call in mock_print.call_args_list:
            if call[0]:  # Check if there are positional arguments
                call_args.append(call[0][0])
        info_messages = [msg for msg in call_args if "Detected data types:" in str(msg)]
        self.assertTrue(len(info_messages) > 0)

    @patch("builtins.print")
    def test_process_file_json_output(self, mock_print):
        """Test processing with JSON output."""
        json_output = os.path.join(self.temp_dir, "test_output.json")

        parser = create_parser()
        args = parser.parse_args([self.input_path, json_output])

        process_file(args)

        # Check that JSON file was created
        self.assertTrue(os.path.exists(json_output))

        # Verify it's valid JSON by reading it back
        result_df = pd.read_json(json_output)
        self.assertEqual(len(result_df), len(self.df))

    @patch("sys.stderr", new_callable=StringIO)
    @patch("builtins.print")
    def test_process_file_read_error(self, mock_print, mock_stderr):
        """Test handling of file read errors."""
        # Create args with non-existent file (should pass validation but fail in processing)
        nonexistent_input = os.path.join(self.temp_dir, "nonexistent.csv")

        parser = create_parser()
        args = parser.parse_args([nonexistent_input, self.output_path])
        args.input = nonexistent_input  # Bypass validation for this test

        with self.assertRaises(SystemExit):
            process_file(args)

    @patch("sys.stderr", new_callable=StringIO)
    @patch("builtins.print")
    def test_process_file_write_error(self, mock_print, mock_stderr):
        """Test handling of file write errors."""
        # Create a path that will definitely cause a write error on all platforms
        if os.name != "nt":
            readonly_output = "/dev/null/output.csv"
        else:
            # On Windows, use a path with invalid characters or non-existent drive
            readonly_output = os.path.join(self.temp_dir, "nonexistent_subdir", "output.csv")
            # Don't create the subdirectory, so write will fail

        parser = create_parser()
        args = parser.parse_args([self.input_path, readonly_output])

        with self.assertRaises(SystemExit):
            process_file(args)

    def test_main_function_integration(self):
        """Test the main function integration."""
        # Mock sys.argv
        test_argv = ["prepo", self.input_path, self.output_path, "--scaler", "standard"]

        with patch.object(sys, "argv", test_argv):
            with patch("builtins.print"):
                # Should not raise any exception
                main()

        # Check that output was created
        self.assertTrue(os.path.exists(self.output_path))

    def test_main_with_version(self):
        """Test main function with version argument."""
        test_argv = ["prepo", "--version"]

        with patch.object(sys, "argv", test_argv):
            with self.assertRaises(SystemExit) as cm:
                main()

            # Version should exit with code 0
            self.assertEqual(cm.exception.code, 0)

    def test_main_with_help(self):
        """Test main function with help argument."""
        test_argv = ["prepo", "--help"]

        with patch.object(sys, "argv", test_argv):
            with self.assertRaises(SystemExit) as cm:
                main()

            # Help should exit with code 0
            self.assertEqual(cm.exception.code, 0)

    def test_main_with_invalid_args(self):
        """Test main function with invalid arguments."""
        test_argv = ["prepo"]  # Missing required arguments

        with patch.object(sys, "argv", test_argv):
            with patch("sys.stderr", new_callable=StringIO):
                with self.assertRaises(SystemExit) as cm:
                    main()

                # Should exit with non-zero code for invalid args
                self.assertNotEqual(cm.exception.code, 0)

    @patch("builtins.print")
    def test_different_file_formats(self, mock_print):
        """Test CLI with different file format combinations."""
        # Test CSV to JSON
        json_output = os.path.join(self.temp_dir, "output.json")
        parser = create_parser()
        args = parser.parse_args([self.input_path, json_output])
        process_file(args)
        self.assertTrue(os.path.exists(json_output))

        # Test with explicit format specification
        csv_output2 = os.path.join(self.temp_dir, "output2.csv")
        args = parser.parse_args([self.input_path, csv_output2, "--input-format", "csv", "--output-format", "csv"])
        process_file(args)
        self.assertTrue(os.path.exists(csv_output2))

    @patch("builtins.print")
    def test_optimization_flags(self, mock_print):
        """Test CLI with optimization flags."""
        parser = create_parser()

        # Test with Polars optimization
        args = parser.parse_args([self.input_path, self.output_path, "--polars"])
        process_file(args)
        self.assertTrue(os.path.exists(self.output_path))

        # Clean up for next test
        os.remove(self.output_path)

        # Test with PyArrow optimization
        args = parser.parse_args([self.input_path, self.output_path, "--pyarrow"])
        process_file(args)
        self.assertTrue(os.path.exists(self.output_path))


if __name__ == "__main__":
    unittest.main()
