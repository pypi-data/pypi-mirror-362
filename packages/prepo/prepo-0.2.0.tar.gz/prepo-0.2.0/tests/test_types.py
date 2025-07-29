"""
Tests for the types module.
"""

import unittest

from src.prepo.types import DataType, FileFormat, ScalerType


class TestDataTypes(unittest.TestCase):
    """Test cases for type-safe enums."""

    def test_data_type_enum(self):
        """Test DataType enum values and methods."""
        # Test enum values
        self.assertEqual(DataType.STRING.value, "string")
        self.assertEqual(DataType.NUMERIC.value, "numeric")
        self.assertEqual(DataType.INTEGER.value, "integer")
        self.assertEqual(DataType.PERCENTAGE.value, "percentage")
        self.assertEqual(DataType.PRICE.value, "price")
        self.assertEqual(DataType.BINARY.value, "binary")
        self.assertEqual(DataType.TEMPORAL.value, "temporal")
        self.assertEqual(DataType.CATEGORICAL.value, "categorical")
        self.assertEqual(DataType.ID.value, "id")
        self.assertEqual(DataType.TEXT.value, "text")
        self.assertEqual(DataType.UNKNOWN.value, "unknown")

        # Test string representation
        self.assertEqual(str(DataType.NUMERIC), "numeric")
        self.assertEqual(str(DataType.PRICE), "price")

        # Test enum membership
        self.assertIn(DataType.STRING, DataType)
        self.assertIn(DataType.NUMERIC, DataType)

    def test_scaler_type_enum(self):
        """Test ScalerType enum values and methods."""
        # Test enum values
        self.assertEqual(ScalerType.STANDARD.value, "standard")
        self.assertEqual(ScalerType.ROBUST.value, "robust")
        self.assertEqual(ScalerType.MINMAX.value, "minmax")
        self.assertEqual(ScalerType.NONE.value, "none")

        # Test string representation
        self.assertEqual(str(ScalerType.STANDARD), "standard")
        self.assertEqual(str(ScalerType.ROBUST), "robust")

        # Test enum membership
        self.assertIn(ScalerType.STANDARD, ScalerType)
        self.assertIn(ScalerType.NONE, ScalerType)

    def test_file_format_enum(self):
        """Test FileFormat enum values and methods."""
        # Test enum values
        self.assertEqual(FileFormat.CSV.value, "csv")
        self.assertEqual(FileFormat.JSON.value, "json")
        self.assertEqual(FileFormat.EXCEL.value, "excel")
        self.assertEqual(FileFormat.XLSX.value, "xlsx")
        self.assertEqual(FileFormat.XLS.value, "xls")
        self.assertEqual(FileFormat.PARQUET.value, "parquet")
        self.assertEqual(FileFormat.FEATHER.value, "feather")
        self.assertEqual(FileFormat.PICKLE.value, "pickle")
        self.assertEqual(FileFormat.TSV.value, "tsv")
        self.assertEqual(FileFormat.ORC.value, "orc")

        # Test string representation
        self.assertEqual(str(FileFormat.CSV), "csv")
        self.assertEqual(str(FileFormat.PARQUET), "parquet")

        # Test enum membership
        self.assertIn(FileFormat.CSV, FileFormat)
        self.assertIn(FileFormat.JSON, FileFormat)

    def test_enum_creation_from_string(self):
        """Test creating enums from string values."""
        # Test DataType creation from string
        self.assertEqual(DataType("numeric"), DataType.NUMERIC)
        self.assertEqual(DataType("price"), DataType.PRICE)

        # Test ScalerType creation from string
        self.assertEqual(ScalerType("standard"), ScalerType.STANDARD)
        self.assertEqual(ScalerType("robust"), ScalerType.ROBUST)

        # Test FileFormat creation from string
        self.assertEqual(FileFormat("csv"), FileFormat.CSV)
        self.assertEqual(FileFormat("json"), FileFormat.JSON)

    def test_enum_invalid_values(self):
        """Test that invalid enum values raise appropriate errors."""
        with self.assertRaises(ValueError):
            DataType("invalid_type")

        with self.assertRaises(ValueError):
            ScalerType("invalid_scaler")

        with self.assertRaises(ValueError):
            FileFormat("invalid_format")

    def test_enum_comparison(self):
        """Test enum comparison operations."""
        # Test equality
        self.assertEqual(DataType.NUMERIC, DataType.NUMERIC)
        self.assertNotEqual(DataType.NUMERIC, DataType.STRING)

        # Test that enums are not equal to their string values
        self.assertNotEqual(DataType.NUMERIC, "numeric")
        self.assertNotEqual(ScalerType.STANDARD, "standard")

    def test_enum_hashing(self):
        """Test that enums can be used as dictionary keys."""
        # Test with DataType
        data_type_dict = {DataType.NUMERIC: "numeric_handler", DataType.STRING: "string_handler"}
        self.assertEqual(data_type_dict[DataType.NUMERIC], "numeric_handler")

        # Test with ScalerType
        scaler_dict = {ScalerType.STANDARD: "standard_scaler", ScalerType.ROBUST: "robust_scaler"}
        self.assertEqual(scaler_dict[ScalerType.STANDARD], "standard_scaler")

    def test_enum_iteration(self):
        """Test iterating over enum values."""
        # Test DataType iteration
        data_types = list(DataType)
        self.assertIn(DataType.NUMERIC, data_types)
        self.assertIn(DataType.STRING, data_types)
        self.assertEqual(len(data_types), 11)  # Should have 11 data types

        # Test ScalerType iteration
        scaler_types = list(ScalerType)
        self.assertIn(ScalerType.STANDARD, scaler_types)
        self.assertIn(ScalerType.NONE, scaler_types)
        self.assertEqual(len(scaler_types), 4)  # Should have 4 scaler types

        # Test FileFormat iteration
        file_formats = list(FileFormat)
        self.assertIn(FileFormat.CSV, file_formats)
        self.assertIn(FileFormat.PARQUET, file_formats)
        self.assertEqual(len(file_formats), 10)  # Should have 10 file formats


if __name__ == "__main__":
    unittest.main()
