"""Utilities for efficient data processing with Parquet and alternative engines."""

from typing import Optional, Union, Dict, Any
from pathlib import Path
import warnings

import pandas as pd
import numpy as np

# Optional imports for performance
try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False
    pl = None

try:
    import pyarrow.parquet as pq
    import pyarrow as pa
    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False
    pa = None
    pq = None


def convert_to_parquet(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    compression: str = 'snappy',
    **kwargs
) -> Path:
    """
    Convert CSV or other formats to Parquet for better performance.
    
    Args:
        input_path: Path to input file
        output_path: Path for output Parquet file (auto-generated if None)
        compression: Compression algorithm ('snappy', 'gzip', 'brotli', etc.)
        **kwargs: Additional arguments for read function
        
    Returns:
        Path to the created Parquet file
    """
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.with_suffix('.parquet')
    else:
        output_path = Path(output_path)
    
    # Read the file
    if input_path.suffix.lower() == '.csv':
        df = pd.read_csv(input_path, **kwargs)
    else:
        df = pd.read_table(input_path, **kwargs)
    
    # Save as Parquet
    df.to_parquet(output_path, compression=compression, engine='auto')
    
    return output_path


def read_with_polars(
    filepath: Union[str, Path],
    to_pandas: bool = True
) -> Union[pd.DataFrame, 'pl.DataFrame']:
    """
    Read files using Polars for better performance.
    
    Args:
        filepath: Path to the file
        to_pandas: Convert to pandas DataFrame (default: True)
        
    Returns:
        DataFrame (pandas or Polars based on to_pandas parameter)
    """
    if not HAS_POLARS:
        raise ImportError(
            "Polars is not installed. Install with: pip install prepo[performance]"
        )
    
    filepath = Path(filepath)
    
    # Read based on file type
    if filepath.suffix.lower() == '.csv':
        df = pl.read_csv(filepath)
    elif filepath.suffix.lower() in ['.parquet', '.pq']:
        df = pl.read_parquet(filepath)
    elif filepath.suffix.lower() in ['.xlsx', '.xls']:
        df = pl.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")
    
    if to_pandas:
        return df.to_pandas()
    return df


def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize DataFrame dtypes to reduce memory usage.
    
    Args:
        df: DataFrame to optimize
        
    Returns:
        DataFrame with optimized dtypes
    """
    optimized_df = df.copy()
    
    for col in optimized_df.columns:
        col_type = optimized_df[col].dtype
        
        if col_type != 'object':
            c_min = optimized_df[col].min()
            c_max = optimized_df[col].max()
            
            # Integer optimization
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    optimized_df[col] = optimized_df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    optimized_df[col] = optimized_df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    optimized_df[col] = optimized_df[col].astype(np.int32)
                    
            # Float optimization
            elif str(col_type)[:5] == 'float':
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    optimized_df[col] = optimized_df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    optimized_df[col] = optimized_df[col].astype(np.float32)
        
        # Category optimization for low cardinality strings
        elif col_type == 'object':
            num_unique_values = len(optimized_df[col].unique())
            num_total_values = len(optimized_df[col])
            if num_unique_values / num_total_values < 0.5:
                optimized_df[col] = optimized_df[col].astype('category')
    
    return optimized_df


def benchmark_read_performance(
    filepath: Union[str, Path],
    engines: list = ['pandas', 'polars', 'pyarrow']
) -> Dict[str, float]:
    """
    Benchmark file reading performance with different engines.
    
    Args:
        filepath: Path to the file to benchmark
        engines: List of engines to test
        
    Returns:
        Dictionary with engine names as keys and read times as values
    """
    import time
    
    filepath = Path(filepath)
    results = {}
    
    # Pandas benchmark
    if 'pandas' in engines:
        start = time.time()
        _ = pd.read_csv(filepath) if filepath.suffix == '.csv' else pd.read_parquet(filepath)
        results['pandas'] = time.time() - start
    
    # Polars benchmark
    if 'polars' in engines and HAS_POLARS:
        start = time.time()
        _ = read_with_polars(filepath, to_pandas=True)
        results['polars'] = time.time() - start
    
    # PyArrow benchmark for Parquet
    if 'pyarrow' in engines and HAS_PYARROW and filepath.suffix in ['.parquet', '.pq']:
        start = time.time()
        _ = pq.read_table(filepath).to_pandas()
        results['pyarrow'] = time.time() - start
    
    return results


class DataProfiler:
    """Generate detailed profiling reports for DataFrames."""
    
    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a comprehensive profile of the DataFrame.
        
        Args:
            df: DataFrame to profile
            
        Returns:
            Dictionary containing profiling information
        """
        profile = {
            'shape': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
            'dtypes': df.dtypes.value_counts().to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'columns': {}
        }
        
        for col in df.columns:
            col_profile = {
                'dtype': str(df[col].dtype),
                'null_count': df[col].isnull().sum(),
                'null_percentage': df[col].isnull().sum() / len(df) * 100,
                'unique_count': df[col].nunique(),
                'unique_percentage': df[col].nunique() / len(df) * 100,
            }
            
            # Numeric column statistics
            if pd.api.types.is_numeric_dtype(df[col]):
                col_profile.update({
                    'mean': df[col].mean(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'quantiles': df[col].quantile([0.25, 0.5, 0.75]).to_dict()
                })
            
            # String column statistics
            elif pd.api.types.is_string_dtype(df[col]) or df[col].dtype == 'object':
                col_profile.update({
                    'avg_length': df[col].astype(str).str.len().mean(),
                    'max_length': df[col].astype(str).str.len().max(),
                    'most_common': df[col].value_counts().head(5).to_dict()
                })
            
            profile['columns'][col] = col_profile
        
        return profile