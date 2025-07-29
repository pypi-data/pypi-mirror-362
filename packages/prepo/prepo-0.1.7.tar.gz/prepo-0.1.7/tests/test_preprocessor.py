"""
Comprehensive tests for the prepo package.
"""

import unittest
from pathlib import Path
import tempfile
import warnings

import pandas as pd
import numpy as np
import pytest

from src.prepo import FeaturePreProcessor, DataType, ScalerType
from src.prepo.utils import optimize_dtypes, DataProfiler


class TestFeaturePreProcessor(unittest.TestCase):
    """Test cases for the FeaturePreProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = FeaturePreProcessor()

        # Create a comprehensive test dataframe
        self.test_data = {
            'date_column': ['2023-01-01', '2023-01-02', np.nan, '2023-01-04', '2023-01-05'],
            'price_USD': [100.50, np.nan, 200.75, 150.25, 300.00],
            'percentage_score': [0.85, 0.92, np.nan, 0.78, 0.95],
            'rating_100': [85, 92, np.nan, 78, 95],
            'is_active': [True, False, np.nan, True, False],
            'category': ['A', 'B', np.nan, 'A', 'C'],
            'revenue': [1000.50, 2000.75, np.nan, 1500.25, 3000.00],
            'count': [10, 15, np.nan, 12, 20],
            'description': ['Product A', np.nan, 'Product C', 'Product D', 'Product E'],
            'user_id': ['USR001', 'USR002', 'USR003', 'USR004', 'USR005'],
            'long_text': ['A' * 150, 'B' * 150, 'C' * 150, 'D' * 150, 'E' * 150]
        }
        self.df = pd.DataFrame(self.test_data)

    def test_enum_usage(self):
        """Test that ENUMs are properly used throughout the code."""
        # Test DataType enum
        self.assertEqual(DataType.NUMERIC.value, "numeric")
        self.assertEqual(DataType.TEMPORAL.value, "temporal")
        
        # Test ScalerType enum
        self.assertEqual(ScalerType.STANDARD.value, "standard")
        self.assertEqual(ScalerType.ROBUST.value, "robust")
    def test_determine_datatypes(self):
        """Test the determine_datatypes method."""
        datatypes = self.processor.determine_datatypes(self.df)

        # Check that the method correctly identifies column types
        self.assertEqual(datatypes['date_column'], DataType.TEMPORAL)
        self.assertEqual(datatypes['price_USD'], DataType.PRICE)
        self.assertEqual(datatypes['percentage_score'], DataType.PERCENTAGE)
        self.assertEqual(datatypes['rating_100'], DataType.NUMERIC)
        self.assertEqual(datatypes['is_active'], DataType.BINARY)
        self.assertEqual(datatypes['category'], DataType.STRING)
        self.assertEqual(datatypes['revenue'], DataType.PRICE)
        self.assertEqual(datatypes['count'], DataType.NUMERIC)
        self.assertEqual(datatypes['description'], DataType.STRING)
        self.assertEqual(datatypes['user_id'], DataType.ID)
        self.assertEqual(datatypes['long_text'], DataType.TEXT)

    def test_clean_data_drop_na(self):
        """Test the clean_data method with drop_na=True."""
        clean_df, datatypes = self.processor.clean_data(self.df, drop_na=True)
        
        # Check no NaN values remain
        self.assertFalse(clean_df.isnull().any().any())
        
        # Check shape is reduced (we had NaN values)
        self.assertLess(len(clean_df), len(self.df))

    def test_clean_data_impute(self):
        """Test the clean_data method with drop_na=False."""
        clean_df, datatypes = self.processor.clean_data(self.df, drop_na=False)
        
        # Check numeric columns have no NaN values (should be imputed)
        numeric_cols = ['price_USD', 'percentage_score', 'rating_100', 'revenue', 'count']
        for col in numeric_cols:
            if col in clean_df.columns:
                self.assertFalse(clean_df[col].isnull().any())

    def test_scalers(self):
        """Test all scaler types."""
        clean_df, _ = self.processor.clean_data(self.df, drop_na=True)
        
        # Test standard scaler
        scaled_standard = self.processor.scale_features(clean_df, ScalerType.STANDARD)
        self.assertIsInstance(scaled_standard, pd.DataFrame)
        # Test robust scaler
        scaled_robust = self.processor.scale_features(clean_df, ScalerType.ROBUST)
        self.assertIsInstance(scaled_robust, pd.DataFrame)
        
        # Test minmax scaler
        scaled_minmax = self.processor.scale_features(clean_df, ScalerType.MINMAX)
        self.assertIsInstance(scaled_minmax, pd.DataFrame)
        
        # Test no scaling
        scaled_none = self.processor.scale_features(clean_df, ScalerType.NONE)
        pd.testing.assert_frame_equal(scaled_none, clean_df)

    def test_process_method(self):
        """Test the main process method."""
        # Test with default parameters
        processed_df = self.processor.process(self.df)
        self.assertIsInstance(processed_df, pd.DataFrame)
        self.assertFalse(processed_df.isnull().any().any())
        
        # Test with different scalers
        for scaler in [ScalerType.STANDARD, ScalerType.ROBUST, ScalerType.MINMAX]:
            processed = self.processor.process(self.df, scaler_type=scaler)
            self.assertIsInstance(processed, pd.DataFrame)

    def test_outlier_removal(self):
        """Test outlier removal functionality."""
        # Create data with outliers
        outlier_data = self.df.copy()
        outlier_data.loc[0, 'price_USD'] = 10000  # Extreme outlier
        
        # Process with outlier removal
        with_outliers = self.processor.process(outlier_data, remove_outlier=False)
        without_outliers = self.processor.process(outlier_data, remove_outlier=True)
        
        # Should have fewer rows when outliers are removed
        self.assertLess(len(without_outliers), len(with_outliers))

    def test_file_io(self):
        """Test file reading and saving functionality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Test CSV
            csv_path = tmpdir / "test.csv"
            self.processor.save_file(self.df, csv_path)            loaded_csv = self.processor.read_file(csv_path)
            self.assertEqual(len(loaded_csv), len(self.df))
            
            # Test Parquet (if available)
            try:
                parquet_path = tmpdir / "test.parquet"
                self.processor.save_file(self.df, parquet_path)
                loaded_parquet = self.processor.read_file(parquet_path)
                self.assertEqual(len(loaded_parquet), len(self.df))
            except ImportError:
                warnings.warn("Parquet support not available")

    def test_error_handling(self):
        """Test error handling."""
        # Test invalid scaler type
        with self.assertRaises(ValueError):
            self.processor.process(self.df, scaler_type='invalid_scaler')
        
        # Test invalid file format
        with self.assertRaises(ValueError):
            self.processor.read_file('test.invalid_format')


class TestUtilities(unittest.TestCase):
    """Test cases for utility functions."""
    
    def setUp(self):
        """Set up test data."""
        self.df = pd.DataFrame({
            'int_col': [1, 2, 3, 4, 5],
            'float_col': [1.1, 2.2, 3.3, 4.4, 5.5],
            'string_col': ['a', 'b', 'a', 'b', 'c'],
            'large_int': [1000000, 2000000, 3000000, 4000000, 5000000]
        })

    def test_optimize_dtypes(self):
        """Test dtype optimization."""
        optimized = optimize_dtypes(self.df)
        
        # Check that int_col is downcasted
        self.assertEqual(optimized['int_col'].dtype, np.int8)
        
        # Check that string column with low cardinality becomes category
        self.assertEqual(optimized['string_col'].dtype.name, 'category')
    def test_data_profiler(self):
        """Test data profiling functionality."""
        profile = DataProfiler.profile(self.df)
        
        # Check profile structure
        self.assertIn('shape', profile)
        self.assertIn('memory_usage', profile)
        self.assertIn('dtypes', profile)
        self.assertIn('missing_values', profile)
        self.assertIn('columns', profile)
        
        # Check column profiles
        self.assertIn('int_col', profile['columns'])
        self.assertIn('mean', profile['columns']['int_col'])
        self.assertIn('std', profile['columns']['int_col'])
        
        # Check string column profile
        self.assertIn('string_col', profile['columns'])
        self.assertIn('avg_length', profile['columns']['string_col'])
        self.assertIn('most_common', profile['columns']['string_col'])


if __name__ == "__main__":
    unittest.main()