# Prepo Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Data Types](#data-types)
5. [API Reference](#api-reference)
6. [Advanced Usage](#advanced-usage)
7. [Performance Tips](#performance-tips)
8. [Contributing](#contributing)

## Introduction

Prepo is a modern Python package for intelligent preprocessing of pandas DataFrames. It automatically detects data types, handles missing values, removes outliers, and scales features - all with a simple, type-safe API.

### Key Features
- **Automatic Data Type Detection**: Intelligently identifies temporal, numeric, percentage, price, binary, ID, and text columns
- **Smart Data Cleaning**: Handles various null representations and missing values
- **Multiple Scaling Options**: Standard, Robust, and MinMax scaling
- **Outlier Detection**: IQR-based outlier removal with configurable options
- **Multiple File Formats**: Support for CSV, Parquet, Excel, JSON, and more
- **Performance Optimized**: Optional Polars integration and memory optimization utilities
- **Type-Safe**: Full type hints and Enum-based configuration
-  **CLI Support**: Process files directly from the command line

## Installation

### Basic Installation
```bash
pip install prepo
```

### With Optional Dependencies
```bash
# For Parquet support
pip install prepo[parquet]

# For performance features (Polars, Dask)
pip install prepo[performance]

# For development
pip install prepo[dev]

# All extras
pip install prepo[parquet,performance,dev]
```

## Quick Start

### Basic Usage
```python
import pandas as pd
from prepo import FeaturePreProcessor, ScalerType

# Create processor
processor = FeaturePreProcessor()

# Load and process data
df = pd.read_csv('data.csv')
processed_df = processor.process(
    df,
    drop_na=True,
    scaler_type=ScalerType.STANDARD,
    remove_outlier=True
)

# Save processed data
processor.save_file(processed_df, 'processed_data.parquet')
```

### Command Line Usage
```bash
# Basic processing
prepo input.csv -o output.csv

# With options
prepo data.csv -o clean.parquet --scaler robust --keep-na --verbose
```

## Data Types

Prepo automatically detects the following data types:

### DataType Enum Values

| Type | Description | Detection Criteria |
|------|-------------|-------------------|
| `TEMPORAL` | Date/time data | Column names with date/time keywords or parseable dates |
| `NUMERIC` | General numbers | Numeric values without special meaning |
| `PERCENTAGE` | Percentages | Values in [0,1] range or percentage keywords |
| `PRICE` | Currency/money | Price/cost keywords or currency symbols |
| `BINARY` | Two-value columns | Exactly 2 unique values |
| `ID` | Identifiers | ID/key/tag keywords in column name |
| `STRING` | Short text | Text with average length < 100 chars |
| `TEXT` | Long text | Text with average length ≥ 100 chars |
| `UNKNOWN` | Unidentified | Cannot determine type |

## API Reference

### FeaturePreProcessor

The main class for data preprocessing.

#### Methods

##### `process(df, drop_na=True, scaler_type=ScalerType.STANDARD, remove_outlier=True)`
Process a DataFrame through the complete pipeline.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `drop_na` (bool): Drop rows with missing values if True, impute if False
- `scaler_type` (ScalerType): Type of scaling to apply
- `remove_outlier` (bool): Remove outliers using IQR method

**Returns:** Processed DataFrame

##### `determine_datatypes(df)`
Automatically detect data types for all columns.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame

**Returns:** Dict[str, DataType] mapping column names to types

##### `clean_data(df, drop_na=True)`
Clean data by handling missing values and null representations.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `drop_na` (bool): Drop or impute missing values

**Returns:** Tuple of (cleaned DataFrame, datatypes dict)

##### `scale_features(df, scaler_type, datatypes=None)`
Scale numeric features using specified method.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `scaler_type` (ScalerType): Scaling method
- `datatypes` (Dict[str, DataType]): Pre-computed datatypes (optional)

**Returns:** Scaled DataFrame

##### `read_file(filepath, file_format=None, **kwargs)`
Read data from various file formats.

**Parameters:**
- `filepath` (str/Path): Path to file
- `file_format` (str): Format override (auto-detected if None)
- `**kwargs`: Additional arguments for pandas read functions

**Returns:** DataFrame

##### `save_file(df, filepath, file_format=None, **kwargs)`
Save DataFrame to various formats.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to save
- `filepath` (str/Path): Output path
- `file_format` (str): Format override (auto-detected if None)
- `**kwargs`: Additional arguments for pandas write functions

### Utility Functions

#### Memory Optimization
```python
from prepo.utils import optimize_dtypes

# Reduce memory usage
optimized_df = optimize_dtypes(df)
```

#### Data Profiling
```python
from prepo.utils import DataProfiler

# Generate comprehensive profile
profile = DataProfiler.profile(df)
print(f"Memory usage: {profile['memory_usage']} MB")
```

#### Performance Benchmarking
```python
from prepo.utils import benchmark_read_performance

# Compare read speeds
results = benchmark_read_performance('large_file.csv')
print(results)  # {'pandas': 1.23, 'polars': 0.45}
```

## Advanced Usage

### Working with Parquet Files
```python
# Convert CSV to Parquet for better performance
from prepo.utils import convert_to_parquet

parquet_path = convert_to_parquet('large_data.csv')

# Process Parquet file
df = processor.read_file(parquet_path)
processed = processor.process(df)
```

### Using Polars for Large Files
```python
from prepo.utils import read_with_polars

# Read with Polars (faster for large files)
df = read_with_polars('huge_file.csv', to_pandas=True)
processed = processor.process(df)
```

### Custom Null Values
```python
# Add custom null representations
processor._null_values.extend(['Missing', 'N.A.', '--'])

# Process will now recognize these as null
processed = processor.process(df)
```

### Pipeline with Multiple Steps
```python
# Step 1: Clean without scaling
clean_df, datatypes = processor.clean_data(df, drop_na=False)

# Step 2: Custom outlier handling
if datatypes['revenue'] == DataType.PRICE:
    # Custom logic for price columns
    clean_df = clean_df[clean_df['revenue'] < 1000000]

# Step 3: Scale with specific method
final_df = processor.scale_features(clean_df, ScalerType.ROBUST, datatypes)
```

## License

MIT License - see LICENSE file for details.