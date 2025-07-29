"""
Command-line interface for the prepo package.

This module provides a CLI tool supporting 8+ file formats with optional
Polars/PyArrow optimizations for high-performance data preprocessing.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

from .io import FileReader, FileWriter
from .preprocessor import FeaturePreProcessor
from .types import FileFormat, ScalerType


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Preprocess data with automated type detection, KNN imputation, and scaling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  prepo input.csv output.csv                    # Basic preprocessing with defaults
  prepo input.xlsx output.csv --scaler robust  # Use robust scaler
  prepo input.json output.parquet --no-outliers --keep-na  # Keep outliers and NA values
  prepo input.csv output.feather --polars      # Use Polars for high performance
  prepo input.tsv output.xlsx --pyarrow        # Use PyArrow optimizations

Supported formats:
  Input/Output: CSV, JSON, Excel (.xlsx/.xls), Parquet, Feather, TSV, Pickle, ORC
        """,
    )

    # Input/Output arguments
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")

    # Processing options
    parser.add_argument(
        "--scaler",
        choices=["standard", "robust", "minmax", "none"],
        default="standard",
        help="Scaling method to use (default: standard)",
    )

    parser.add_argument("--keep-na", action="store_true", help="Keep NA values and impute them instead of dropping rows")

    parser.add_argument("--no-outliers", action="store_true", help="Skip outlier removal")

    # Performance optimizations
    parser.add_argument("--polars", action="store_true", help="Use Polars for high-performance operations (if available)")

    parser.add_argument("--pyarrow", action="store_true", help="Use PyArrow for optimized I/O operations (if available)")

    # File format options
    parser.add_argument(
        "--input-format",
        choices=["csv", "json", "excel", "xlsx", "xls", "parquet", "feather", "pickle", "tsv", "orc"],
        help="Explicitly specify input file format (auto-detected if not provided)",
    )

    parser.add_argument(
        "--output-format",
        choices=["csv", "json", "excel", "xlsx", "xls", "parquet", "feather", "pickle", "tsv", "orc"],
        help="Explicitly specify output file format (auto-detected if not provided)",
    )

    # Additional options
    parser.add_argument(
        "--info", action="store_true", help="Display information about detected data types and processing steps"
    )

    parser.add_argument("--version", action="version", version="prepo 0.2.0")

    return parser


def validate_args(args) -> None:
    """Validate command line arguments."""
    # Check input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Check output directory exists
    output_path = Path(args.output)
    if not output_path.parent.exists():
        print(f"Error: Output directory '{output_path.parent}' does not exist", file=sys.stderr)
        sys.exit(1)


def process_file(args) -> None:
    """Process the file according to command line arguments."""
    # Initialize components
    processor = FeaturePreProcessor(use_polars=args.polars, use_pyarrow=args.pyarrow)

    reader = FileReader(use_polars=args.polars, use_pyarrow=args.pyarrow)

    writer = FileWriter(use_polars=args.polars, use_pyarrow=args.pyarrow)

    # Read input file
    try:
        input_format = FileFormat(args.input_format) if args.input_format else None
        print(f"Reading {args.input}...")
        df = reader.read_file(args.input, file_format=input_format)
        print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Display data type information if requested
    if args.info:
        datatypes = processor.determine_datatypes(df)
        print("\nDetected data types:")
        for col, dtype in datatypes.items():
            print(f"  {col}: {dtype}")
        print()

    # Process the data
    try:
        print("Processing data...")

        scaler_type = ScalerType(args.scaler)
        drop_na = not args.keep_na
        remove_outliers = not args.no_outliers

        if args.info:
            print(f"  Scaler: {scaler_type}")
            print(f"  Drop NA: {drop_na}")
            print(f"  Remove outliers: {remove_outliers}")

        processed_df = processor.process(df=df, drop_na=drop_na, scaler_type=scaler_type, remove_outlier=remove_outliers)

        print(f"Processed data: {len(processed_df)} rows, {len(processed_df.columns)} columns")

    except Exception as e:
        print(f"Error processing data: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output file
    try:
        output_format = FileFormat(args.output_format) if args.output_format else None
        print(f"Writing {args.output}...")
        writer.write_file(processed_df, args.output, file_format=output_format)
        print("Processing complete!")

    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    validate_args(args)
    process_file(args)


if __name__ == "__main__":
    main()
