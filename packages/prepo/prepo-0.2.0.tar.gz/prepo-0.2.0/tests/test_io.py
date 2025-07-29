"""
Tests for the I/O module.
"""

import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from src.prepo.io import FileReader, FileWriter
from src.prepo.types import FileFormat


class TestFileIO(unittest.TestCase):
    """Test cases for file I/O operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = {
            "numeric_col": [1, 2, 3, 4, 5],
            "string_col": ["A", "B", "C", "D", "E"],
            "float_col": [1.1, 2.2, 3.3, 4.4, 5.5],
            "bool_col": [True, False, True, False, True],
        }
        self.df = pd.DataFrame(self.test_data)

        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_file_reader_initialization(self):
        """Test FileReader initialization with different options."""
        # Test basic initialization
        reader = FileReader()
        self.assertFalse(reader.use_polars)
        self.assertFalse(reader.use_pyarrow)

        # Test with optimizations (will only be True if libraries are available)
        reader_opt = FileReader(use_polars=True, use_pyarrow=True)
        self.assertIsInstance(reader_opt.use_polars, bool)
        self.assertIsInstance(reader_opt.use_pyarrow, bool)

    def test_file_writer_initialization(self):
        """Test FileWriter initialization with different options."""
        # Test basic initialization
        writer = FileWriter()
        self.assertFalse(writer.use_polars)
        self.assertFalse(writer.use_pyarrow)

        # Test with optimizations
        writer_opt = FileWriter(use_polars=True, use_pyarrow=True)
        self.assertIsInstance(writer_opt.use_polars, bool)
        self.assertIsInstance(writer_opt.use_pyarrow, bool)

    def test_detect_format(self):
        """Test file format detection from extensions."""
        reader = FileReader()

        # Test various file extensions
        self.assertEqual(reader._detect_format("test.csv"), FileFormat.CSV)
        self.assertEqual(reader._detect_format("test.json"), FileFormat.JSON)
        self.assertEqual(reader._detect_format("test.xlsx"), FileFormat.XLSX)
        self.assertEqual(reader._detect_format("test.xls"), FileFormat.XLS)
        self.assertEqual(reader._detect_format("test.parquet"), FileFormat.PARQUET)
        self.assertEqual(reader._detect_format("test.feather"), FileFormat.FEATHER)
        self.assertEqual(reader._detect_format("test.pkl"), FileFormat.PICKLE)
        self.assertEqual(reader._detect_format("test.pickle"), FileFormat.PICKLE)
        self.assertEqual(reader._detect_format("test.tsv"), FileFormat.TSV)
        self.assertEqual(reader._detect_format("test.orc"), FileFormat.ORC)

        # Test case insensitive
        self.assertEqual(reader._detect_format("test.CSV"), FileFormat.CSV)
        self.assertEqual(reader._detect_format("test.JSON"), FileFormat.JSON)

        # Test Path objects
        self.assertEqual(reader._detect_format(Path("test.csv")), FileFormat.CSV)

        # Test unknown extension defaults to CSV
        self.assertEqual(reader._detect_format("test.unknown"), FileFormat.CSV)

    def test_csv_round_trip(self):
        """Test CSV read/write round trip."""
        reader = FileReader()
        writer = FileWriter()

        csv_path = os.path.join(self.temp_dir, "test.csv")

        # Write CSV
        writer.write_file(self.df, csv_path)
        self.assertTrue(os.path.exists(csv_path))

        # Read CSV
        df_read = reader.read_file(csv_path)

        # Compare (allowing for minor type differences)
        self.assertEqual(len(df_read), len(self.df))
        self.assertEqual(list(df_read.columns), list(self.df.columns))

    def test_json_round_trip(self):
        """Test JSON read/write round trip."""
        reader = FileReader()
        writer = FileWriter()

        json_path = os.path.join(self.temp_dir, "test.json")

        # Write JSON
        writer.write_file(self.df, json_path)
        self.assertTrue(os.path.exists(json_path))

        # Read JSON
        df_read = reader.read_file(json_path)

        # Compare
        self.assertEqual(len(df_read), len(self.df))
        self.assertEqual(list(df_read.columns), list(self.df.columns))

    def test_excel_round_trip(self):
        """Test Excel read/write round trip."""
        reader = FileReader()
        writer = FileWriter()

        excel_path = os.path.join(self.temp_dir, "test.xlsx")

        try:
            # Write Excel
            writer.write_file(self.df, excel_path)
            self.assertTrue(os.path.exists(excel_path))

            # Read Excel
            df_read = reader.read_file(excel_path)

            # Compare
            self.assertEqual(len(df_read), len(self.df))
            self.assertEqual(list(df_read.columns), list(self.df.columns))

        except ImportError:
            # Skip if openpyxl not available
            self.skipTest("openpyxl not available for Excel support")

    def test_pickle_round_trip(self):
        """Test Pickle read/write round trip."""
        reader = FileReader()
        writer = FileWriter()

        pickle_path = os.path.join(self.temp_dir, "test.pkl")

        # Write Pickle
        writer.write_file(self.df, pickle_path)
        self.assertTrue(os.path.exists(pickle_path))

        # Read Pickle
        df_read = reader.read_file(pickle_path)

        # Compare (pickle should preserve exact data)
        pd.testing.assert_frame_equal(df_read, self.df)

    def test_tsv_round_trip(self):
        """Test TSV read/write round trip."""
        reader = FileReader()
        writer = FileWriter()

        tsv_path = os.path.join(self.temp_dir, "test.tsv")

        # Write TSV
        writer.write_file(self.df, tsv_path)
        self.assertTrue(os.path.exists(tsv_path))

        # Read TSV
        df_read = reader.read_file(tsv_path)

        # Compare
        self.assertEqual(len(df_read), len(self.df))
        self.assertEqual(list(df_read.columns), list(self.df.columns))

    def test_explicit_format_specification(self):
        """Test explicit file format specification."""
        reader = FileReader()
        writer = FileWriter()

        # Test writing with explicit format
        csv_path = os.path.join(self.temp_dir, "test_explicit.csv")
        writer.write_file(self.df, csv_path, file_format=FileFormat.CSV)
        self.assertTrue(os.path.exists(csv_path))

        # Test reading with explicit format
        df_read = reader.read_file(csv_path, file_format=FileFormat.CSV)
        self.assertEqual(len(df_read), len(self.df))

    def test_unsupported_format_error(self):
        """Test error handling for unsupported formats."""
        reader = FileReader()
        writer = FileWriter()

        # Create a mock unsupported format
        class UnsupportedFormat:
            value = "unsupported"

        test_path = os.path.join(self.temp_dir, "test.txt")

        with self.assertRaises(ValueError):
            writer._write_with_pandas(self.df, test_path, UnsupportedFormat())

        # Create a dummy file for read test
        with open(test_path, "w") as f:
            f.write("dummy content")

        with self.assertRaises(ValueError):
            reader._read_with_pandas(test_path, UnsupportedFormat())

    def test_file_kwargs_passing(self):
        """Test that kwargs are properly passed to underlying pandas functions."""
        reader = FileReader()
        writer = FileWriter()

        csv_path = os.path.join(self.temp_dir, "test_kwargs.csv")

        # Write with specific separator
        writer.write_file(self.df, csv_path, sep=";")

        # Read with same separator
        df_read = reader.read_file(csv_path, sep=";")
        self.assertEqual(len(df_read), len(self.df))

    def test_polars_integration(self):
        """Test Polars integration if available."""
        try:
            import polars as pl

            reader = FileReader(use_polars=True)
            writer = FileWriter(use_polars=True)

            if reader.use_polars:  # Only test if Polars is actually available
                csv_path = os.path.join(self.temp_dir, "test_polars.csv")

                # Test CSV with Polars
                writer.write_file(self.df, csv_path)
                df_read = reader.read_file(csv_path)

                self.assertEqual(len(df_read), len(self.df))
                self.assertEqual(list(df_read.columns), list(self.df.columns))

        except ImportError:
            self.skipTest("Polars not available")

    def test_pyarrow_integration(self):
        """Test PyArrow integration if available."""
        try:
            import pyarrow as pa

            reader = FileReader(use_pyarrow=True)
            writer = FileWriter(use_pyarrow=True)

            if reader.use_pyarrow:  # Only test if PyArrow is actually available
                parquet_path = os.path.join(self.temp_dir, "test_pyarrow.parquet")

                # Test Parquet with PyArrow
                writer.write_file(self.df, parquet_path)
                df_read = reader.read_file(parquet_path)

                self.assertEqual(len(df_read), len(self.df))
                self.assertEqual(list(df_read.columns), list(self.df.columns))

        except ImportError:
            self.skipTest("PyArrow not available")

    def test_large_file_handling(self):
        """Test handling of larger datasets."""
        # Create a larger test dataset
        large_data = {"col1": range(1000), "col2": [f"string_{i}" for i in range(1000)], "col3": np.random.random(1000)}
        large_df = pd.DataFrame(large_data)

        reader = FileReader()
        writer = FileWriter()

        csv_path = os.path.join(self.temp_dir, "large_test.csv")

        # Write and read large file
        writer.write_file(large_df, csv_path)
        df_read = reader.read_file(csv_path)

        self.assertEqual(len(df_read), len(large_df))
        self.assertEqual(list(df_read.columns), list(large_df.columns))

    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrames."""
        empty_df = pd.DataFrame()

        reader = FileReader()
        writer = FileWriter()

        csv_path = os.path.join(self.temp_dir, "empty_test.csv")

        # Write empty DataFrame
        writer.write_file(empty_df, csv_path)

        # For empty DataFrames, pandas might create a file that can't be read back
        # So we'll test that the file exists and handle the read gracefully
        self.assertTrue(os.path.exists(csv_path))

        try:
            df_read = reader.read_file(csv_path)
            self.assertEqual(len(df_read), 0)
        except pd.errors.EmptyDataError:
            # This is expected for truly empty DataFrames
            self.skipTest("Empty DataFrame creates unreadable CSV file")

    def test_special_characters_handling(self):
        """Test handling of special characters in data."""
        special_data = {
            "col_with_unicode": ["café", "naïve", "résumé", "测试", "Москва"],
            "col_with_symbols": ["$100", "€200", "£300", "¥400", "₹500"],
            "col_with_newlines": ["line1\nline2", "single_line", "line1\rline2", "tab\tseparated", "normal"],
        }
        special_df = pd.DataFrame(special_data)

        reader = FileReader()
        writer = FileWriter()

        csv_path = os.path.join(self.temp_dir, "special_test.csv")

        # Write and read DataFrame with special characters
        writer.write_file(special_df, csv_path)
        df_read = reader.read_file(csv_path)

        self.assertEqual(len(df_read), len(special_df))
        self.assertEqual(list(df_read.columns), list(special_df.columns))


if __name__ == "__main__":
    unittest.main()
