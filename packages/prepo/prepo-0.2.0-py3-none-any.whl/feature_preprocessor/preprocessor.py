"""
Core functionality for the FeaturePreProcessor package.

This module contains the main FeaturePreProcessor class that provides
methods for cleaning, scaling, and processing pandas DataFrames.
"""

from typing import Dict, Tuple

import numpy as np
import pandas as pd
from dateutil.parser import parse
from scipy.stats import iqr
from sklearn.impute import KNNImputer


class FeaturePreProcessor:
    """
    A class for preprocessing pandas DataFrames.

    This class provides methods for:
    - Determining data types of DataFrame columns
    - Cleaning data (handling missing values)
    - Removing outliers
    - Scaling numeric features
    """

    def __init__(self):
        self.scalers = {
            "standard": self._standard_scaler,
            "robust": self._robust_scaler,
            "minmax": self._minmax_scaler,
            "none": None,
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

    def clean_outliers(self, df: pd.DataFrame, dt: Dict[str, str]) -> pd.DataFrame:
        """
        Remove outliers from numeric columns in the dataframe.

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
            if dt[col] in ["price", "numeric", "percentage"]:
                iqrv = iqr(newdf[col])
                q1 = newdf[col].quantile(0.25)
                q3 = newdf[col].quantile(0.75)
                newdf = newdf[newdf[col].between(q1 - 1.5 * iqrv, q3 + 1.5 * iqrv)]

        return newdf

    def is_timeseries(self, df: pd.DataFrame) -> bool:
        """
        Determine if the dataframe represents a time series (has exactly one temporal column).

        Args:
            df: DataFrame to analyze

        Returns:
            True if the dataframe is a time series, False otherwise
        """
        datatypes = self.determine_datatypes(df)
        temporal_count = sum(1 for dtype in datatypes.values() if dtype == "temporal")
        return temporal_count == 1

    def determine_datatypes(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Determine the data type of each column in the dataframe.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary mapping column names to their inferred data types
        """
        datatypes = {}
        sample_size = min(1000, len(df.index))
        sample_df = df.sample(sample_size, random_state=42) if sample_size > 100 else df

        # Precompute column properties for efficiency
        column_properties = {}
        for col in sample_df.columns:
            series = sample_df[col]
            column_properties[col] = {
                "is_numeric": pd.api.types.is_numeric_dtype(series),
                "nunique": series.nunique(),
                "nunique_ratio": series.nunique() / len(sample_df) if len(sample_df) > 0 else 0,
                "col_lower": col.lower(),
                "na_count": series.isna().sum(),
            }

        for col in sample_df.columns:
            props = column_properties[col]
            series = sample_df[col]
            col_lower = props["col_lower"]

            # temporal
            if any(word in col_lower for word in ["date", "time", "year", "month", "day"]):
                datatypes[col] = "temporal"
            elif pd.api.types.is_datetime64_any_dtype(series):
                datatypes[col] = "temporal"
            elif series.dropna().apply(self._is_date).all() and not series.dropna().empty:
                datatypes[col] = "temporal"

            # binary
            elif props["nunique"] == 2:
                datatypes[col] = "binary"

            # percentage
            elif props["is_numeric"] and (
                any(word in col_lower for word in ["perc", "rating", "percentage", "percent", "%", "score", "ratio"])
                or (series.dropna().between(0, 1).mean() > 0.9 and "rate" in col_lower)
            ):
                datatypes[col] = "percentage"

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
                datatypes[col] = "price"

            # ID columns
            elif props["is_numeric"] and (col_lower.endswith("id") or col_lower.startswith("id")):
                datatypes[col] = "id"

            # numeric
            elif props["is_numeric"]:
                if series.dropna().apply(lambda x: float(x).is_integer()).all():
                    datatypes[col] = "integer"
                else:
                    datatypes[col] = "numeric"

            # categorical
            elif (props["nunique_ratio"] < 0.2 and pd.api.types.is_object_dtype(series)) or any(
                word in col_lower for word in ["category", "categories", "type", "group"]
            ):
                datatypes[col] = "categorical"

            # string
            elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
                if series.dropna().str.len().mean() > 100:
                    datatypes[col] = "text"
                else:
                    datatypes[col] = "string"

            # unknown
            else:
                datatypes[col] = "unknown"

        return datatypes

    def clean_data(self, df: pd.DataFrame, drop_na: bool = True) -> Tuple[pd.DataFrame, Dict[str, str]]:
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

        null_values = ["?", "Error", "na", "NA", "ERROR", "error", "err", "ERR", "NAType", "natype", "UNKNOWN", "unknown", ""]
        clean_df = clean_df.replace(null_values, np.nan)

        if drop_na:
            clean_df = clean_df.dropna(how="any")
        else:
            for col in clean_df.columns:
                if not clean_df[col].isnull().any():
                    continue

                if datatypes[col] in ["numeric", "price", "percentage", "integer"]:
                    if clean_df[col].notna().sum() >= 3:  # Need at least 3 values for KNN
                        imputer = KNNImputer(n_neighbors=min(3, clean_df[col].notna().sum()))
                        clean_df[col] = imputer.fit_transform(clean_df[[col]]).flatten()
                    else:
                        clean_df[col] = clean_df[col].fillna(clean_df[col].mean())

                elif datatypes[col] == "categorical":
                    mode_value = clean_df[col].mode()
                    if not mode_value.empty:
                        clean_df[col] = clean_df[col].fillna(mode_value[0])

                else:
                    clean_df = clean_df.dropna(subset=[col])

        clean_df = clean_df.reset_index(drop=True)
        return clean_df, datatypes

    def scaler(self, df: pd.DataFrame, scaler_type: str = "standard", datatypes: Dict[str, str] = None):
        """
        Scales the features using the specified scaler type.

        Args:
            df: Cleaned dataframe to scale
            scaler_type: Type of scaler to use (standard, robust, minmax)
            datatypes: Datatypes of dataframe

        Returns:
            None (scales the dataframe in-place)
        """
        scaler_func = self.scalers[scaler_type]

        if scaler_func is None:
            return

        for col in df.columns:
            if any(word in col.lower() for word in ["id", "tag", "identification", "item"]):
                continue
            if datatypes[col] in ["price", "numeric", "percentage"]:
                df[col] = scaler_func(df[col])

    def process(
        self, df: pd.DataFrame, drop_na: bool = True, scaler_type: str = "standard", remove_outlier: bool = True
    ) -> pd.DataFrame:
        """
        Clean and scale numeric features in the dataframe.

        Args:
            df: DataFrame to process
            drop_na: Whether to drop NA values during cleaning
            scaler_type: Type of scaler to use ('standard', 'robust', 'minmax')
            remove_outlier: Choose to remove outliers or not

        Returns:
            Processed DataFrame
        """
        if scaler_type not in self.scalers:
            raise ValueError(f"Unknown scaler type: {scaler_type}. Available: {list(self.scalers.keys())}")

        # Get cleaned data set
        clean_df, datatypes = self.clean_data(df, drop_na=drop_na)

        # Remove outliers if wanted
        if remove_outlier:
            clean_df = self.clean_outliers(clean_df, datatypes)

        # Scale numeric columns
        self.scaler(clean_df, scaler_type, datatypes)

        clean_df.index = range(len(clean_df))
        return clean_df
