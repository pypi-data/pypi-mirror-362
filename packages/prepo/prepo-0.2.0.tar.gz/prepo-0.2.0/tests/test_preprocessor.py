"""
Comprehensive tests for the prepo package.
"""

import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from src.prepo import DataType, FeaturePreProcessor, ScalerType


class TestFeaturePreProcessor(unittest.TestCase):
    """Test cases for the FeaturePreProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = FeaturePreProcessor()

        # Create a comprehensive test dataframe
        self.test_data = {
            "date_column": ["2023-01-01", "2023-01-02", np.nan, "2023-01-04", "2023-01-05"],
            "price_USD": [100.50, np.nan, 200.75, 150.25, 300.00],
            "percentage_score": [0.85, 0.92, np.nan, 0.78, 0.95],
            "rating_100": [85, 92, np.nan, 78, 95],
            "is_active": [True, False, np.nan, True, False],
            "category": ["A", "B", np.nan, "A", "C"],
            "revenue": [1000.50, 2000.75, np.nan, 1500.25, 3000.00],
            "count": [10, 15, np.nan, 12, 20],
            "description": ["Product A", np.nan, "Product C", "Product D", "Product E"],
            "id_column": [1001, 1002, 1003, 1004, 1005],
            "long_text": [
                "This is a very long description that exceeds 100 characters and should be classified as text type rather than string type."
            ]
            * 5,
        }
        self.df = pd.DataFrame(self.test_data)

    def test_determine_datatypes_comprehensive(self):
        """Test the determine_datatypes method with comprehensive data types."""
        datatypes = self.processor.determine_datatypes(self.df)

        # Check that the method correctly identifies all column types
        self.assertEqual(datatypes["date_column"], DataType.TEMPORAL)
        self.assertEqual(datatypes["price_USD"], DataType.PRICE)
        self.assertEqual(datatypes["percentage_score"], DataType.PERCENTAGE)
        self.assertEqual(datatypes["rating_100"], DataType.INTEGER)
        self.assertEqual(datatypes["is_active"], DataType.BINARY)
        self.assertEqual(datatypes["category"], DataType.CATEGORICAL)
        self.assertEqual(datatypes["revenue"], DataType.PRICE)
        self.assertEqual(datatypes["count"], DataType.INTEGER)
        self.assertEqual(datatypes["description"], DataType.STRING)
        self.assertEqual(datatypes["id_column"], DataType.ID)
        self.assertEqual(datatypes["long_text"], DataType.TEXT)

    def test_determine_datatypes_edge_cases(self):
        """Test edge cases in data type determination."""
        # Test with empty dataframe
        empty_df = pd.DataFrame()
        datatypes_empty = self.processor.determine_datatypes(empty_df)
        self.assertEqual(datatypes_empty, {})

        # Test with single row
        single_row_df = pd.DataFrame({"col1": [1], "col2": ["text"]})
        datatypes_single = self.processor.determine_datatypes(single_row_df)
        self.assertIn("col1", datatypes_single)
        self.assertIn("col2", datatypes_single)

    def test_clean_data_drop_na(self):
        """Test the clean_data method with drop_na=True."""
        clean_df, datatypes = self.processor.clean_data(self.df, drop_na=True)

        # Check that rows with NaN values are dropped
        self.assertEqual(len(clean_df), 3)  # Only 3 rows have no NaN values (rows 0, 3, 4)
        self.assertFalse(clean_df.isnull().any().any())

    def test_clean_data_impute(self):
        """Test the clean_data method with drop_na=False (KNN imputation)."""
        clean_df, datatypes = self.processor.clean_data(self.df, drop_na=False)

        # Check that NaN values are imputed in numeric columns
        self.assertFalse(clean_df["price_USD"].isna().any())
        self.assertFalse(clean_df["percentage_score"].isna().any())

        # Check that the dataframe has the expected structure
        self.assertGreater(len(clean_df), 2)

    def test_clean_outliers(self):
        """Test the clean_outliers method."""
        # Create data with obvious outliers
        outlier_data = {"normal_values": [1, 2, 3, 4, 5], "with_outliers": [1, 2, 3, 4, 1000]}  # 1000 is an outlier
        outlier_df = pd.DataFrame(outlier_data)

        datatypes = {"normal_values": DataType.NUMERIC, "with_outliers": DataType.NUMERIC}

        clean_df = self.processor.clean_outliers(outlier_df, datatypes)

        # Should have fewer rows after removing outliers
        self.assertLess(len(clean_df), len(outlier_df))

    def test_scaling_methods(self):
        """Test all scaling methods."""
        clean_df, datatypes = self.processor.clean_data(self.df, drop_na=True)

        # Test standard scaling
        test_df_std = clean_df.copy()
        self.processor.scaler(test_df_std, ScalerType.STANDARD, datatypes)

        # Check that numeric columns are scaled (mean should be close to 0)
        numeric_cols = [
            col
            for col, dtype in datatypes.items()
            if dtype in [DataType.NUMERIC, DataType.PRICE, DataType.PERCENTAGE, DataType.INTEGER]
        ]

        for col in numeric_cols:
            if col in test_df_std.columns:
                self.assertAlmostEqual(test_df_std[col].mean(), 0, delta=1e-10)

        # Test robust scaling
        test_df_robust = clean_df.copy()
        self.processor.scaler(test_df_robust, ScalerType.ROBUST, datatypes)

        # Test minmax scaling
        test_df_minmax = clean_df.copy()
        self.processor.scaler(test_df_minmax, ScalerType.MINMAX, datatypes)

        # Test no scaling
        test_df_none = clean_df.copy()
        original_values = test_df_none.copy()
        self.processor.scaler(test_df_none, ScalerType.NONE, datatypes)
        pd.testing.assert_frame_equal(test_df_none, original_values)

    def test_process_comprehensive(self):
        """Test the complete process method with different configurations."""
        # Test with different scaler types
        for scaler in [ScalerType.STANDARD, ScalerType.ROBUST, ScalerType.MINMAX, ScalerType.NONE]:
            processed_df = self.processor.process(self.df, drop_na=True, scaler_type=scaler, remove_outlier=True)

            self.assertIsInstance(processed_df, pd.DataFrame)
            self.assertGreater(len(processed_df.columns), 0)

        # Test with string scaler type (backward compatibility)
        processed_df = self.processor.process(self.df, scaler_type="standard")
        self.assertIsInstance(processed_df, pd.DataFrame)

        # Test with keep NA and no outlier removal
        processed_df = self.processor.process(self.df, drop_na=False, scaler_type=ScalerType.ROBUST, remove_outlier=False)
        self.assertIsInstance(processed_df, pd.DataFrame)

    def test_polars_optimization(self):
        """Test Polars optimization initialization."""
        try:
            import polars as pl

            processor_polars = FeaturePreProcessor(use_polars=True)
            self.assertTrue(processor_polars.use_polars)
        except ImportError:
            processor_polars = FeaturePreProcessor(use_polars=True)
            self.assertFalse(processor_polars.use_polars)

    def test_pyarrow_optimization(self):
        """Test PyArrow optimization initialization."""
        try:
            import pyarrow as pa

            processor_pyarrow = FeaturePreProcessor(use_pyarrow=True)
            self.assertTrue(processor_pyarrow.use_pyarrow)
        except ImportError:
            processor_pyarrow = FeaturePreProcessor(use_pyarrow=True)
            self.assertFalse(processor_pyarrow.use_pyarrow)

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test invalid scaler type
        with self.assertRaises(ValueError):
            self.processor.process(self.df, scaler_type="invalid_scaler")

        # Test with enum
        with self.assertRaises(ValueError):
            # Create a mock invalid enum value
            invalid_scaler = "invalid"
            self.processor.process(self.df, scaler_type=invalid_scaler)

    def test_helper_methods(self):
        """Test private helper methods."""
        # Test _is_numeric
        numeric_series = pd.Series([1, 2, 3, 4, 5])
        self.assertTrue(self.processor._is_numeric(numeric_series))

        string_series = pd.Series(["a", "b", "c"])
        self.assertFalse(self.processor._is_numeric(string_series))

        # Test _is_percentage_range
        percentage_series = pd.Series([0.1, 0.5, 0.9])
        self.assertTrue(self.processor._is_percentage_range(percentage_series))

        non_percentage_series = pd.Series([10, 50, 90])
        self.assertFalse(self.processor._is_percentage_range(non_percentage_series))

        # Test _is_date
        self.assertTrue(self.processor._is_date("2023-01-01"))
        self.assertFalse(self.processor._is_date("not_a_date"))
        self.assertFalse(self.processor._is_date(np.nan))

    def test_scalers_dict(self):
        """Test that all scalers are properly initialized."""
        expected_scalers = {ScalerType.STANDARD, ScalerType.ROBUST, ScalerType.MINMAX, ScalerType.NONE}

        actual_scalers = set(self.processor.scalers.keys())
        self.assertEqual(expected_scalers, actual_scalers)


if __name__ == "__main__":
    unittest.main()
