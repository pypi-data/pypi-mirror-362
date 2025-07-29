"""
File I/O operations supporting multiple formats.

This module provides functionality to read and write data from various file formats
including CSV, JSON, Excel, Parquet, and more with optional Polars/PyArrow optimizations.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np
import pandas as pd

from .types import FileFormat

# Optional high-performance libraries
try:
    import polars as pl

    HAS_POLARS = True
except ImportError:
    pl = None
    HAS_POLARS = False

try:
    import pyarrow as pa
    import pyarrow.parquet as pq

    HAS_PYARROW = True
except ImportError:
    pa = None
    pq = None
    HAS_PYARROW = False


class FileReader:
    """
    Universal file reader supporting 8+ file formats with optional optimizations.
    """

    def __init__(self, use_polars: bool = False, use_pyarrow: bool = False):
        """
        Initialize the FileReader.

        Args:
            use_polars: Use Polars for high-performance operations if available
            use_pyarrow: Use PyArrow for optimized I/O operations if available
        """
        self.use_polars = use_polars and HAS_POLARS
        self.use_pyarrow = use_pyarrow and HAS_PYARROW

    def _detect_format(self, filepath: Union[str, Path]) -> FileFormat:
        """
        Detect file format from file extension.

        Args:
            filepath: Path to the file

        Returns:
            Detected file format
        """
        path = Path(filepath)
        extension = path.suffix.lower()

        format_mapping = {
            ".csv": FileFormat.CSV,
            ".json": FileFormat.JSON,
            ".xlsx": FileFormat.XLSX,
            ".xls": FileFormat.XLS,
            ".parquet": FileFormat.PARQUET,
            ".feather": FileFormat.FEATHER,
            ".pkl": FileFormat.PICKLE,
            ".pickle": FileFormat.PICKLE,
            ".tsv": FileFormat.TSV,
            ".orc": FileFormat.ORC,
        }

        return format_mapping.get(extension, FileFormat.CSV)

    def read_file(self, filepath: Union[str, Path], file_format: Optional[FileFormat] = None, **kwargs) -> pd.DataFrame:
        """
        Read data from various file formats.

        Args:
            filepath: Path to the file
            file_format: Explicit file format (auto-detected if None)
            **kwargs: Additional arguments for specific readers

        Returns:
            DataFrame containing the data
        """
        if file_format is None:
            file_format = self._detect_format(filepath)

        if self.use_polars and file_format in [FileFormat.CSV, FileFormat.PARQUET]:
            return self._read_with_polars(filepath, file_format, **kwargs)
        elif self.use_pyarrow and file_format == FileFormat.PARQUET:
            return self._read_with_pyarrow(filepath, **kwargs)
        else:
            return self._read_with_pandas(filepath, file_format, **kwargs)

    def _read_with_polars(self, filepath: Union[str, Path], file_format: FileFormat, **kwargs) -> pd.DataFrame:
        """Read file using Polars for high performance."""
        if file_format == FileFormat.CSV:
            df_pl = pl.read_csv(filepath, **kwargs)
        elif file_format == FileFormat.PARQUET:
            df_pl = pl.read_parquet(filepath, **kwargs)
        else:
            raise ValueError(f"Polars doesn't support {file_format}")

        return df_pl.to_pandas()

    def _read_with_pyarrow(self, filepath: Union[str, Path], **kwargs) -> pd.DataFrame:
        """Read Parquet file using PyArrow for optimized I/O."""
        table = pq.read_table(filepath, **kwargs)
        return table.to_pandas()

    def _read_with_pandas(self, filepath: Union[str, Path], file_format: FileFormat, **kwargs) -> pd.DataFrame:
        """Read file using pandas."""
        if file_format == FileFormat.CSV:
            return pd.read_csv(filepath, **kwargs)
        elif file_format == FileFormat.JSON:
            return pd.read_json(filepath, **kwargs)
        elif file_format in [FileFormat.XLSX, FileFormat.XLS, FileFormat.EXCEL]:
            return pd.read_excel(filepath, **kwargs)
        elif file_format == FileFormat.PARQUET:
            return pd.read_parquet(filepath, **kwargs)
        elif file_format == FileFormat.FEATHER:
            return pd.read_feather(filepath, **kwargs)
        elif file_format == FileFormat.PICKLE:
            return pd.read_pickle(filepath, **kwargs)
        elif file_format == FileFormat.TSV:
            return pd.read_csv(filepath, sep="\t", **kwargs)
        elif file_format == FileFormat.ORC:
            return pd.read_orc(filepath, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")


class FileWriter:
    """
    Universal file writer supporting multiple formats.
    """

    def __init__(self, use_polars: bool = False, use_pyarrow: bool = False):
        """
        Initialize the FileWriter.

        Args:
            use_polars: Use Polars for high-performance operations if available
            use_pyarrow: Use PyArrow for optimized I/O operations if available
        """
        self.use_polars = use_polars and HAS_POLARS
        self.use_pyarrow = use_pyarrow and HAS_PYARROW

    def _detect_format(self, filepath: Union[str, Path]) -> FileFormat:
        """Detect file format from file extension."""
        path = Path(filepath)
        extension = path.suffix.lower()

        format_mapping = {
            ".csv": FileFormat.CSV,
            ".json": FileFormat.JSON,
            ".xlsx": FileFormat.XLSX,
            ".xls": FileFormat.XLS,
            ".parquet": FileFormat.PARQUET,
            ".feather": FileFormat.FEATHER,
            ".pkl": FileFormat.PICKLE,
            ".pickle": FileFormat.PICKLE,
            ".tsv": FileFormat.TSV,
            ".orc": FileFormat.ORC,
        }

        return format_mapping.get(extension, FileFormat.CSV)

    def write_file(
        self, df: pd.DataFrame, filepath: Union[str, Path], file_format: Optional[FileFormat] = None, **kwargs
    ) -> None:
        """
        Write DataFrame to various file formats.

        Args:
            df: DataFrame to write
            filepath: Output file path
            file_format: Explicit file format (auto-detected if None)
            **kwargs: Additional arguments for specific writers
        """
        if file_format is None:
            file_format = self._detect_format(filepath)

        if self.use_polars and file_format in [FileFormat.CSV, FileFormat.PARQUET]:
            self._write_with_polars(df, filepath, file_format, **kwargs)
        elif self.use_pyarrow and file_format == FileFormat.PARQUET:
            self._write_with_pyarrow(df, filepath, **kwargs)
        else:
            self._write_with_pandas(df, filepath, file_format, **kwargs)

    def _write_with_polars(self, df: pd.DataFrame, filepath: Union[str, Path], file_format: FileFormat, **kwargs) -> None:
        """Write file using Polars for high performance."""
        df_pl = pl.from_pandas(df)

        if file_format == FileFormat.CSV:
            df_pl.write_csv(filepath, **kwargs)
        elif file_format == FileFormat.PARQUET:
            df_pl.write_parquet(filepath, **kwargs)
        else:
            raise ValueError(f"Polars doesn't support {file_format}")

    def _write_with_pyarrow(self, df: pd.DataFrame, filepath: Union[str, Path], **kwargs) -> None:
        """Write Parquet file using PyArrow for optimized I/O."""
        table = pa.Table.from_pandas(df)
        pq.write_table(table, filepath, **kwargs)

    def _write_with_pandas(self, df: pd.DataFrame, filepath: Union[str, Path], file_format: FileFormat, **kwargs) -> None:
        """Write file using pandas."""
        if file_format == FileFormat.CSV:
            # Use proper quoting to handle special characters and newlines
            df.to_csv(filepath, index=False, quoting=1, **kwargs)  # quoting=1 is csv.QUOTE_ALL
        elif file_format == FileFormat.JSON:
            df.to_json(filepath, **kwargs)
        elif file_format in [FileFormat.XLSX, FileFormat.XLS, FileFormat.EXCEL]:
            df.to_excel(filepath, index=False, **kwargs)
        elif file_format == FileFormat.PARQUET:
            df.to_parquet(filepath, **kwargs)
        elif file_format == FileFormat.FEATHER:
            df.to_feather(filepath, **kwargs)
        elif file_format == FileFormat.PICKLE:
            df.to_pickle(filepath, **kwargs)
        elif file_format == FileFormat.TSV:
            # Use proper quoting for TSV as well
            df.to_csv(filepath, sep="\t", index=False, quoting=1, **kwargs)
        elif file_format == FileFormat.ORC:
            df.to_orc(filepath, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
