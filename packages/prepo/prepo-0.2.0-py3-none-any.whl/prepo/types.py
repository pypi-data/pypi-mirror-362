"""
Type definitions and enums for the prepo package.

This module contains type-safe enumerations for data types and scaling methods.
"""

from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Union


class DataType(Enum):
    """Type-safe enumeration for data types detected in DataFrames."""

    STRING = "string"
    NUMERIC = "numeric"
    INTEGER = "integer"
    PERCENTAGE = "percentage"
    PRICE = "price"
    BINARY = "binary"
    TEMPORAL = "temporal"
    CATEGORICAL = "categorical"
    ID = "id"
    TEXT = "text"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return self.value


class ScalerType(Enum):
    """Type-safe enumeration for scaling methods."""

    STANDARD = "standard"
    ROBUST = "robust"
    MINMAX = "minmax"
    NONE = "none"

    def __str__(self) -> str:
        return self.value


class FileFormat(Enum):
    """Type-safe enumeration for supported file formats."""

    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"
    XLSX = "xlsx"
    XLS = "xls"
    PARQUET = "parquet"
    FEATHER = "feather"
    PICKLE = "pickle"
    TSV = "tsv"
    ORC = "orc"

    def __str__(self) -> str:
        return self.value


# Type aliases for better code readability
DataTypeDict = Dict[str, DataType]
ScalerFunction = Optional[Callable[[Any], Any]]
FileData = Union[Dict[str, Any], List[Dict[str, Any]]]
