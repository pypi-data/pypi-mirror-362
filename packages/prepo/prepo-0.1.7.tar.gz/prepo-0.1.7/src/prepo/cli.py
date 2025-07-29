"""Command line interface for prepo."""

import argparse
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

from .preprocessor import FeaturePreProcessor, ScalerType


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Preprocess CSV/Parquet files with automatic type detection and scaling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  prepo input.csv -o output.csv
  prepo input.csv -o output.parquet --format parquet
  prepo data.csv --scaler robust --keep-na
  prepo data.csv --no-outliers --scaler minmax
        """
    )
    
    parser.add_argument(
        "input",
        type=str,
        help="Input file path (CSV, Parquet, Excel, etc.)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="Output file path"
    )
    
    parser.add_argument(
        "-f", "--format",
        type=str,
        default=None,
        choices=["csv", "parquet", "excel", "json", "feather"],
        help="Output format (auto-detected from extension if not specified)"
    )
    
    parser.add_argument(
        "-s", "--scaler",
        type=str,
        default="standard",
        choices=["standard", "robust", "minmax", "none"],
        help="Scaler type to use (default: standard)"
    )
    
    parser.add_argument(
        "--keep-na",
        action="store_true",
        help="Keep rows with missing values (impute instead of dropping)"
    )
    
    parser.add_argument(
        "--no-outliers",
        action="store_false",
        dest="remove_outliers",
        help="Don't remove outliers"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed processing information"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize processor
        processor = FeaturePreProcessor()
        
        # Read input file
        if args.verbose:
            print(f"Reading {args.input}...")
        df = processor.read_file(args.input)
        
        if args.verbose:
            print(f"Original shape: {df.shape}")
            print(f"Columns: {', '.join(df.columns)}")
        
        # Process data
        if args.verbose:
            print(f"\nProcessing with scaler='{args.scaler}', "
                  f"drop_na={not args.keep_na}, "
                  f"remove_outliers={args.remove_outliers}")
        
        processed_df = processor.process(
            df,
            drop_na=not args.keep_na,
            scaler_type=args.scaler,
            remove_outlier=args.remove_outliers
        )
        
        if args.verbose:
            print(f"Processed shape: {processed_df.shape}")
        
        # Save output
        if args.verbose:
            print(f"\nSaving to {args.output}...")
        processor.save_file(processed_df, args.output, file_format=args.format)
        
        if args.verbose:
            print("Done!")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()