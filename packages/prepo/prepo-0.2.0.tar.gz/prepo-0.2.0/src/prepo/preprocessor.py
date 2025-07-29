"""
Core functionality for the prepo package.

This module contains the main FeaturePreProcessor class that provides
methods for cleaning, scaling, and processing pandas DataFrames.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from dateutil.parser import parse
from scipy.stats import iqr
from sklearn.impute import KNNImputer

from .types import DataType, DataTypeDict, ScalerType

# Optional high-performance libraries
try:
    import polars as pl

    HAS_POLARS = True
except ImportError:
    pl = None
    HAS_POLARS = False

try:
    import pyarrow as pa

    HAS_PYARROW = True
except ImportError:
    pa = None
    HAS_PYARROW = False


class FeaturePreProcessor:
    """
    A class for preprocessing pandas DataFrames with automated data type detection,
    KNN imputation, outlier removal, and multiple scaling methods.

    Features:
    - Automated data type detection using type-safe enums
    - KNN imputation for missing values
    - Multiple scaling methods (standard, robust, minmax)
    - Outlier removal using IQR method
    - Optional Polars/PyArrow optimizations
    """

    def __init__(self, use_polars: bool = False, use_pyarrow: bool = False):
        """
        Initialize the FeaturePreProcessor.

        Args:
            use_polars: Use Polars for high-performance operations if available
            use_pyarrow: Use PyArrow for optimized I/O operations if available
        """
        self.use_polars = use_polars and HAS_POLARS
        self.use_pyarrow = use_pyarrow and HAS_PYARROW
        self.ENUM = DataType  # Add the ENUM attribute

        self.scalers = {
            ScalerType.STANDARD: self._standard_scaler,
            ScalerType.ROBUST: self._robust_scaler,
            ScalerType.MINMAX: self._minmax_scaler,
            ScalerType.NONE: None,
        }

    def _robust_scaler(self, series: pd.Series) -> pd.Series:
        """Apply robust scaling using IQR."""
        median = series.median()
        iqr_value = iqr(series)
        if iqr_value == 0:
            return series - median
        return (series - median) / iqr_value

    def _minmax_scaler(self, series: pd.Series) -> pd.Series:
        """Apply min-max scaling."""
        min_val, max_val = series.min(), series.max()
        if min_val == max_val:
            return series - min_val
        return (series - min_val) / (max_val - min_val)

    def _standard_scaler(self, series: pd.Series) -> pd.Series:
        """Apply standard scaling (z-score normalization)."""
        mean_val, std_val = series.mean(), series.std()
        if std_val == 0:
            return series - mean_val
        return (series - mean_val) / std_val

    def _is_numeric(self, series):
        """Check if a series contains mostly numeric data."""
        if pd.api.types.is_numeric_dtype(series):
            return True

        sample = series.dropna().astype(str)
        if len(sample) > 1000:
            sample = sample.sample(1000)

        if len(sample) == 0:
            return False

        converted = pd.to_numeric(sample, errors="coerce")

        success_rate = converted.notna().sum() / len(sample)

        return success_rate > 0.6

    def _is_percentage_range(self, series):
        """checks if a numeric series is a percentage"""
        try:
            numeric_data = pd.to_numeric(series, errors="coerce")
            clean_numeric = numeric_data.dropna()

            if len(clean_numeric) == 0:
                return False

            in_range = clean_numeric.between(0, 1)
            percentage_in_range = in_range.mean()

            return percentage_in_range > 0.9

        except Exception:
            return False

    def _is_date(self, value) -> bool:
        """Check if a value can be parsed as a date."""
        if pd.isna(value) or not isinstance(value, str):
            return False
        try:
            parse(value, fuzzy=False)
            return True
        except (ValueError, TypeError):
            return False

    def _is_string(self, value) -> bool:
        """Check if a value is a string."""
        return isinstance(value, str)

    def clean_outliers(self, df: pd.DataFrame, dt: DataTypeDict) -> pd.DataFrame:
        """
        Remove outliers from numeric columns in the dataframe using IQR method.

        Args:
            df: DataFrame to clean
            dt: Dictionary mapping column names to their data types

        Returns:
            DataFrame with outliers removed
        """
        newdf = df.copy()

        for col in df.columns:
            if any(word in col.lower() for word in ["id", "tag", "identification", "item"]):
                continue
            if dt[col] in [DataType.PRICE, DataType.NUMERIC, DataType.PERCENTAGE, DataType.INTEGER]:
                iqrv = iqr(newdf[col])
                q1 = newdf[col].quantile(0.25)
                q3 = newdf[col].quantile(0.75)
                newdf = newdf[newdf[col].between(q1 - 1.5 * iqrv, q3 + 1.5 * iqrv)]

        return newdf

    def determine_datatypes(self, df: pd.DataFrame) -> DataTypeDict:
        """
        Determine the data type of each column in the dataframe using automated detection.

        Args:
            df: DataFrame to find data types

        Returns:
            Dictionary mapping column names to their inferred data types
        """
        datatypes = {}
        sample_size = min(1000, len(df.index))
        sample_df = df.sample(sample_size, random_state=42) if sample_size > 100 else df

        # Precompute column properties
        column_properties = {}
        for col in sample_df.columns:
            series = sample_df[col]
            column_properties[col] = {
                "is_numeric": self._is_numeric(series),
                "nunique": series.nunique(),
                "nunique_ratio": series.value_counts(normalize=True),
                "col_lower": col.lower(),
                "na_count": series.isna().sum(),
            }

        for col in sample_df.columns:
            props = column_properties[col]
            series = sample_df[col]
            col_lower = props["col_lower"]

            # temporal
            if any(word in col_lower for word in ["date", "time", "year", "month", "day"]):
                datatypes[col] = DataType.TEMPORAL
            elif series.dropna().apply(self._is_date).all() and not series.dropna().empty:
                datatypes[col] = DataType.TEMPORAL

            # binary
            elif props["nunique"] == 2:
                datatypes[col] = DataType.BINARY

            # ID columns (check before numeric to catch numeric IDs)
            elif any(word in col_lower for word in ["id", "identification", "serial", "key"]):
                datatypes[col] = DataType.ID

            # percentage - check both value range and keywords (but prioritize actual value range)
            elif props["is_numeric"] and self._is_percentage_range(series):
                datatypes[col] = DataType.PERCENTAGE
            elif (
                any(word in col_lower for word in ["perc", "percentage", "percent", "%", "score", "ratio"])
                and props["is_numeric"]
                and self._is_percentage_range(series)
            ):
                datatypes[col] = DataType.PERCENTAGE

            # price/currency
            elif props["is_numeric"] and any(
                word in col_lower
                for word in [
                    "price",
                    "cost",
                    "revenue",
                    "sales",
                    "income",
                    "expense",
                    "$",
                    "€",
                    "£",
                    "¥",
                    "₹",
                    "₽",
                    "₩",
                    "₪",
                    "₦",
                    "₡",
                    "¢",
                    "₨",
                    "₱",
                ]
            ):
                datatypes[col] = DataType.PRICE

            # Check for integer vs float numeric
            elif props["is_numeric"]:
                if series.dropna().apply(lambda x: float(x).is_integer()).all():
                    datatypes[col] = DataType.INTEGER
                else:
                    datatypes[col] = DataType.NUMERIC

            # categorical (before string to catch categorical data)
            elif (props["nunique_ratio"].max() < 0.2 and pd.api.types.is_object_dtype(series)) or any(
                word in col_lower for word in ["category", "categories", "type", "group"]
            ):
                datatypes[col] = DataType.CATEGORICAL

            # string/text
            elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
                if series.dropna().str.len().mean() > 100:
                    datatypes[col] = DataType.TEXT
                else:
                    datatypes[col] = DataType.STRING

            # unknown
            else:
                datatypes[col] = DataType.UNKNOWN

        return datatypes

    def clean_data(self, df: pd.DataFrame, drop_na: bool = True) -> Tuple[pd.DataFrame, DataTypeDict]:
        """
        Clean the dataframe by handling missing values and standardizing null representations.

        Args:
            df: DataFrame to clean
            drop_na: If True, drop rows with NA values; if False, impute them using KNN

        Returns:
            Tuple of (cleaned_dataframe, datatypes_dict)
        """
        datatypes = self.determine_datatypes(df)
        clean_df = df.copy()

        null_values = ["?", "Error", "na", "NA", "ERROR", "error", "err", "ERR", "NAType", "natype", "UNKNOWN", "unknown", ""]
        clean_df = clean_df.replace(null_values, np.nan)

        # Convert numeric columns to proper numeric types
        for col in clean_df.columns:
            if datatypes[col] in [DataType.NUMERIC, DataType.PRICE, DataType.PERCENTAGE, DataType.INTEGER]:
                clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")

        if drop_na:
            clean_df = clean_df.dropna(how="any")
        else:
            for col in clean_df.columns:
                if not clean_df[col].isnull().any():
                    continue

                if datatypes[col] in [DataType.NUMERIC, DataType.PRICE, DataType.PERCENTAGE, DataType.INTEGER]:
                    if clean_df[col].notna().sum() >= 3:  # Need at least 3 values for KNN
                        imputer = KNNImputer(n_neighbors=min(3, clean_df[col].notna().sum()))
                        clean_df[col] = imputer.fit_transform(clean_df[[col]]).flatten()
                    else:
                        clean_df[col] = clean_df[col].fillna(clean_df[col].mean())

                elif datatypes[col] == DataType.CATEGORICAL:
                    mode_value = clean_df[col].mode()
                    if not mode_value.empty:
                        clean_df[col] = clean_df[col].fillna(mode_value[0])

                else:
                    clean_df = clean_df.dropna(subset=[col])

        clean_df = clean_df.reset_index(drop=True)
        return clean_df, datatypes

    def scaler(
        self,
        df: pd.DataFrame,
        scaler_type: Union[ScalerType, str] = "standard",
        datatypes: Optional[Dict[str, Union[DataType, str]]] = None,
    ):
        """
        Scales the features using the specified scaler type.

        Args:
            df: Cleaned dataframe to scale
            scaler_type: Type of scaler to use (standard, robust, minmax) - can be string or ScalerType enum
            datatypes: Datatypes of dataframe - can contain DataType enums or strings

        Returns:
            None (scales the dataframe in-place)
        """
        # Convert string to enum if needed
        if isinstance(scaler_type, str):
            scaler_type = ScalerType(scaler_type)

        scaler_func = self.scalers[scaler_type]

        if scaler_func is None:
            return

        if datatypes is None:
            return

        for col in df.columns:
            # Skip ID columns
            if any(word in col.lower() for word in ["id", "identification", "item"]):
                continue

            # Handle both enum and string datatypes
            col_datatype = datatypes[col]
            if hasattr(col_datatype, "value"):  # It's an enum object
                col_datatype_value = col_datatype.value
            else:  # It's already a string
                col_datatype_value = col_datatype

            # Check if column should be scaled
            scalable_types = ["price", "numeric", "percentage", "integer"]
            if col_datatype_value in scalable_types:
                df[col] = scaler_func(df[col])

    def process(
        self,
        df: pd.DataFrame,
        drop_na: bool = True,
        scaler_type: Union[ScalerType, str] = ScalerType.STANDARD,
        remove_outlier: bool = True,
    ) -> pd.DataFrame:
        """
        Clean and scale numeric features in the dataframe.

        Args:
            df: DataFrame to process
            drop_na: Whether to drop NA values during cleaning
            scaler_type: Type of scaler to use (standard, robust, minmax, none)
            remove_outlier: Choose to remove outliers or not

        Returns:
            Processed DataFrame
        """
        # Convert string to enum if needed
        if isinstance(scaler_type, str):
            scaler_type = ScalerType(scaler_type)

        if scaler_type not in self.scalers:
            raise ValueError(f"Unknown scaler type: {scaler_type}. Available: {list(self.scalers.keys())}")

        # Get cleaned data set
        clean_df, datatypes = self.clean_data(df, drop_na=drop_na)

        # Remove outliers if wanted
        if remove_outlier:
            clean_df = self.clean_outliers(clean_df, datatypes)

        # Scale numeric columns
        datatypes_str = {k: v.value for k, v in datatypes.items()}
        self.scaler(clean_df, scaler_type.value, datatypes_str)

        clean_df.index = range(len(clean_df))
        return clean_df
