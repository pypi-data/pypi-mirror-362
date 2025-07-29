"""
Core functionality for the prepo package.

This module contains the main FeaturePreProcessor class that provides
methods for cleaning, scaling, and processing pandas DataFrames.
"""

from __future__ import annotations

import warnings
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Tuple, Optional, Union, Literal, List, Any, Protocol

import pandas as pd
import numpy as np
from dateutil.parser import parse
from scipy.stats import iqr
from sklearn.impute import KNNImputer


class DataType(Enum):
    """Enumeration for supported data types."""
    STRING = "string"
    NUMERIC = "numeric"
    PERCENTAGE = "percentage"
    PRICE = "price"
    BINARY = "binary"
    TEMPORAL = "temporal"
    ID = "id"
    TEXT = "text"
    UNKNOWN = "unknown"


class ScalerType(Enum):
    """Enumeration for supported scaler types."""
    STANDARD = "standard"
    ROBUST = "robust"
    MINMAX = "minmax"
    NONE = "none"


class ScalerProtocol(Protocol):
    """Protocol for scaler functions."""
    def __call__(self, series: pd.Series) -> pd.Series: ...


class FeaturePreProcessor:
    """
    A class for preprocessing pandas DataFrames with automatic data type detection,
    cleaning, and feature scaling.
    
    This preprocessor handles:
    - Automatic data type detection
    - Missing value imputation
    - Outlier removal
    - Feature scaling
    - Support for multiple file formats (CSV, Parquet)
    
    Examples:
        >>> processor = FeaturePreProcessor()
        >>> df = pd.read_csv('data.csv')
        >>> processed_df = processor.process(df, drop_na=True, scaler_type='standard')
    """

    def __init__(self) -> None:
        """Initialize the FeaturePreProcessor with available scalers."""
        self.scalers: Dict[str, Optional[ScalerProtocol]] = {
            ScalerType.STANDARD.value: self._standard_scaler,
            ScalerType.ROBUST.value: self._robust_scaler,
            ScalerType.MINMAX.value: self._minmax_scaler,
            ScalerType.NONE.value: None
        }
        self._null_values: List[str] = [
            "?", "Error", "na", "NA", "ERROR", "error", "err", "ERR",
            "NAType", "natype", "UNKNOWN", "unknown", "", "N/A", "n/a",
            "None", "none", "NULL", "null", "NaN", "nan"
        ]

    def _robust_scaler(self, series: pd.Series) -> pd.Series:
        """
        Apply robust scaling using IQR.
        
        Args:
            series: Pandas Series to scale
            
        Returns:
            Scaled Series
        """
        median = series.median()
        iqr_value = iqr(series)
        if iqr_value == 0:
            return series - median
        return (series - median) / iqr_value

    def _minmax_scaler(self, series: pd.Series) -> pd.Series:
        """
        Apply min-max scaling.
        
        Args:
            series: Pandas Series to scale
            
        Returns:
            Scaled Series between 0 and 1
        """
        min_val, max_val = series.min(), series.max()
        if min_val == max_val:
            return series - min_val
        return (series - min_val) / (max_val - min_val)

    def _standard_scaler(self, series: pd.Series) -> pd.Series:
        """
        Apply standard scaling (z-score normalization).
        
        Args:
            series: Pandas Series to scale
            
        Returns:
            Scaled Series with mean=0 and std=1
        """
        mean_val, std_val = series.mean(), series.std()
        if std_val == 0:
            return series - mean_val
        return (series - mean_val) / std_val

    def _is_numeric(self, series: pd.Series, threshold: float = 0.6) -> bool:
        """
        Check if a series contains mostly numeric data.
        
        Args:
            series: Pandas Series to check
            threshold: Minimum success rate for numeric conversion (default: 0.6)
            
        Returns:
            True if series is mostly numeric, False otherwise
        """
        if pd.api.types.is_numeric_dtype(series):
            return True

        sample = series.dropna().astype(str)
        if len(sample) > 1000:
            sample = sample.sample(1000, random_state=42)

        if len(sample) == 0:
            return False

        converted = pd.to_numeric(sample, errors='coerce')
        success_rate = converted.notna().sum() / len(sample)

        return success_rate > threshold

    def _is_percentage_range(self, series: pd.Series, threshold: float = 0.9) -> bool:
        """
        Check if a numeric series represents percentages.
        
        Args:
            series: Pandas Series to check
            threshold: Minimum ratio of values in [0,1] range (default: 0.9)
            
        Returns:
            True if series contains percentage values, False otherwise
        """
        try:
            numeric_data = pd.to_numeric(series, errors='coerce')
            clean_numeric = numeric_data.dropna()

            if len(clean_numeric) == 0:
                return False

            in_range = clean_numeric.between(0, 1)
            percentage_in_range = in_range.mean()

            return percentage_in_range > threshold

        except Exception:
            return False

    def _is_date(self, value: Any) -> bool:
        """
        Check if a value can be parsed as a date.
        
        Args:
            value: Value to check
            
        Returns:
            True if value can be parsed as date, False otherwise
        """
        if pd.isna(value) or not isinstance(value, str):
            return False
        try:
            parse(value, fuzzy=False)
            return True
        except (ValueError, TypeError):
            return False

    def _is_string(self, value: Any) -> bool:
        """
        Check if a value is a string.
        
        Args:
            value: Value to check
            
        Returns:
            True if value is a string, False otherwise
        """
        return isinstance(value, str)

    def clean_outliers(
        self, 
        df: pd.DataFrame, 
        datatypes: Dict[str, DataType]
    ) -> pd.DataFrame:
        """
        Remove outliers from numeric columns using IQR method.
        
        Args:
            df: DataFrame to clean
            datatypes: Dictionary mapping column names to their data types
            
        Returns:
            DataFrame with outliers removed
        """
        newdf = df.copy()
        id_keywords = ["id", "tag", "identification", "item", "key", "code"]

        for col in df.columns:
            if any(word in col.lower() for word in id_keywords):
                continue
                
            if datatypes[col] in [DataType.PRICE, DataType.NUMERIC, DataType.PERCENTAGE]:
                iqrv = iqr(newdf[col])
                q1 = newdf[col].quantile(0.25)
                q3 = newdf[col].quantile(0.75)
                newdf = newdf[newdf[col].between(q1 - 1.5 * iqrv, q3 + 1.5 * iqrv)]

        return newdf

    def determine_datatypes(self, df: pd.DataFrame) -> Dict[str, DataType]:
        """
        Automatically determine the data type of each column.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary mapping column names to their inferred DataType
        """
        datatypes: Dict[str, DataType] = {}
        sample_size = min(1000, len(df.index))
        sample_df = df.sample(sample_size, random_state=42) if sample_size > 100 else df

        # Keywords for data type detection
        temporal_keywords = ["date", "time", "year", "month", "day", "timestamp", "datetime"]
        percentage_keywords = ["perc", "rating", "percentage", "percent", "%", "score", "ratio", "rate"]
        price_keywords = [
            "price", "cost", "revenue", "sales", "income", "expense", "amount", "fee",
            '$', '€', '£', '¥', '₹', '₽', '₩', '₪', '₦', '₡', '¢', '₨', '₱'
        ]
        id_keywords = ["id", "tag", "identification", "serial", "key", "code", "uuid", "guid"]

        # Precompute column properties for efficiency
        column_properties = {}
        for col in sample_df.columns:
            series = sample_df[col]
            column_properties[col] = {
                'is_numeric': self._is_numeric(series),
                'nunique': series.nunique(),
                'nunique_ratio': series.nunique() / len(series) if len(series) > 0 else 0,
                'col_lower': col.lower(),
                'na_count': series.isna().sum(),
                'dtype': series.dtype
            }

        for col in sample_df.columns:
            props = column_properties[col]
            series = sample_df[col]
            col_lower = props['col_lower']

            # Temporal data
            if any(word in col_lower for word in temporal_keywords):
                datatypes[col] = DataType.TEMPORAL
            elif series.dropna().apply(self._is_date).all() and not series.dropna().empty:
                datatypes[col] = DataType.TEMPORAL

            # Binary data
            elif props['nunique'] == 2:
                datatypes[col] = DataType.BINARY

            # Percentage data
            elif (any(word in col_lower for word in percentage_keywords) or
                  (props['is_numeric'] and self._is_percentage_range(series))):
                datatypes[col] = DataType.PERCENTAGE

            # Price/currency data
            elif props['is_numeric'] and any(word in col_lower for word in price_keywords):
                datatypes[col] = DataType.PRICE

            # ID columns
            elif any(word in col_lower for word in id_keywords):
                datatypes[col] = DataType.ID

            # Numeric data
            elif props['is_numeric']:
                datatypes[col] = DataType.NUMERIC

            # Text data (long strings)
            elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
                if series.dropna().str.len().mean() > 100:
                    datatypes[col] = DataType.TEXT
                else:
                    datatypes[col] = DataType.STRING

            # Unknown data type
            else:
                datatypes[col] = DataType.UNKNOWN
                warnings.warn(f"Could not determine data type for column '{col}'")

        return datatypes

    def clean_data(
        self, 
        df: pd.DataFrame, 
        drop_na: bool = True
    ) -> Tuple[pd.DataFrame, Dict[str, DataType]]:
        """
        Clean the dataframe by handling missing values and standardizing null representations.
        
        Args:
            df: DataFrame to clean
            drop_na: If True, drop rows with NA values; if False, impute them
            
        Returns:
            Tuple of (cleaned_dataframe, datatypes_dict)
        """
        datatypes = self.determine_datatypes(df)
        clean_df = df.copy()

        # Replace various null representations with NaN
        clean_df = clean_df.replace(self._null_values, np.nan)

        # Convert numeric columns
        numeric_types = [DataType.NUMERIC, DataType.PRICE, DataType.PERCENTAGE]
        for col in clean_df.columns:
            if datatypes[col] in numeric_types:
                clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce')

        # Handle missing values
        if drop_na:
            clean_df = clean_df.dropna(how='any')
        else:
            for col in clean_df.columns:
                if not clean_df[col].isnull().any():
                    continue

                if datatypes[col] in numeric_types:
                    # Use KNN imputation for numeric columns with enough data
                    if clean_df[col].notna().sum() >= 3:
                        imputer = KNNImputer(n_neighbors=min(3, clean_df[col].notna().sum()))
                        clean_df[col] = imputer.fit_transform(clean_df[[col]]).flatten()
                    else:
                        # Fall back to mean imputation
                        clean_df[col] = clean_df[col].fillna(clean_df[col].mean())
                else:
                    # For non-numeric columns, drop rows with missing values
                    clean_df = clean_df.dropna(subset=[col])

        clean_df = clean_df.reset_index(drop=True)
        return clean_df, datatypes

    def scale_features(
        self, 
        df: pd.DataFrame, 
        scaler_type: Union[str, ScalerType] = ScalerType.STANDARD,
        datatypes: Optional[Dict[str, DataType]] = None
    ) -> pd.DataFrame:
        """
        Scale numeric features using the specified scaler type.
        
        Args:
            df: DataFrame to scale
            scaler_type: Type of scaler to use
            datatypes: Pre-computed data types (optional)
            
        Returns:
            DataFrame with scaled features
        """
        # Convert ScalerType enum to string if needed
        if isinstance(scaler_type, ScalerType):
            scaler_type = scaler_type.value
            
        scaler_func = self.scalers.get(scaler_type)
        
        if scaler_func is None and scaler_type != ScalerType.NONE.value:
            raise ValueError(
                f"Unknown scaler type: {scaler_type}. "
                f"Available: {list(self.scalers.keys())}"
            )

        if scaler_type == ScalerType.NONE.value:
            return df

        if datatypes is None:
            datatypes = self.determine_datatypes(df)

        scaled_df = df.copy()
        id_keywords = ["id", "tag", "identification", "item", "key", "code"]
        numeric_types = [DataType.PRICE, DataType.NUMERIC, DataType.PERCENTAGE]

        for col in scaled_df.columns:
            # Skip ID columns
            if any(word in col.lower() for word in id_keywords):
                continue
                
            # Scale numeric columns
            if datatypes[col] in numeric_types and scaler_func is not None:
                scaled_df[col] = scaler_func(scaled_df[col])

        return scaled_df

    def process(
        self,
        df: pd.DataFrame,
        drop_na: bool = True,
        scaler_type: Union[str, ScalerType] = ScalerType.STANDARD,
        remove_outlier: bool = True
    ) -> pd.DataFrame:
        """
        Process a DataFrame through cleaning, outlier removal, and scaling.
        
        Args:
            df: DataFrame to process
            drop_na: Whether to drop NA values during cleaning
            scaler_type: Type of scaler to use
            remove_outlier: Whether to remove outliers
            
        Returns:
            Processed DataFrame
        """        # Validate scaler type
        if isinstance(scaler_type, str):
            if scaler_type not in self.scalers:
                raise ValueError(
                    f"Unknown scaler type: {scaler_type}. "
                    f"Available: {list(self.scalers.keys())}"
                )

        # Clean data
        clean_df, datatypes = self.clean_data(df, drop_na=drop_na)

        # Remove outliers if requested
        if remove_outlier:
            clean_df = self.clean_outliers(clean_df, datatypes)

        # Scale numeric features
        processed_df = self.scale_features(clean_df, scaler_type, datatypes)

        # Reset index
        processed_df.index = range(len(processed_df))
        
        return processed_df

    def read_file(
        self,
        filepath: Union[str, Path],
        file_format: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Read data from various file formats with automatic format detection.
        
        Args:            filepath: Path to the file
            file_format: File format ('csv', 'parquet', 'excel', etc.)
            **kwargs: Additional arguments for the reader function
            
        Returns:
            DataFrame containing the file data
        """
        filepath = Path(filepath)
        
        if file_format is None:
            # Auto-detect format from extension
            file_format = filepath.suffix.lower().lstrip('.')
        
        readers = {
            'csv': pd.read_csv,
            'parquet': pd.read_parquet,
            'pq': pd.read_parquet,
            'xlsx': pd.read_excel,
            'xls': pd.read_excel,
            'json': pd.read_json,
            'feather': pd.read_feather,
            'hdf': pd.read_hdf,
            'h5': pd.read_hdf,
        }
        
        if file_format not in readers:
            raise ValueError(f"Unsupported file format: {file_format}")
            
        return readers[file_format](filepath, **kwargs)

    def save_file(
        self,
        df: pd.DataFrame,        filepath: Union[str, Path],
        file_format: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Save DataFrame to various file formats.
        
        Args:
            df: DataFrame to save
            filepath: Path where to save the file
            file_format: File format ('csv', 'parquet', 'excel', etc.)
            **kwargs: Additional arguments for the writer function
        """
        filepath = Path(filepath)
        
        if file_format is None:
            # Auto-detect format from extension
            file_format = filepath.suffix.lower().lstrip('.')
        
        writers = {
            'csv': lambda df, path, **kw: df.to_csv(path, index=False, **kw),
            'parquet': df.to_parquet,
            'pq': df.to_parquet,
            'xlsx': lambda df, path, **kw: df.to_excel(path, index=False, **kw),
            'xls': lambda df, path, **kw: df.to_excel(path, index=False, **kw),
            'json': df.to_json,
            'feather': df.to_feather,
            'hdf': df.to_hdf,
            'h5': df.to_hdf,
        }
        
        if file_format not in writers:
            raise ValueError(f"Unsupported file format: {file_format}")
            
        writers[file_format](df, filepath, **kwargs)