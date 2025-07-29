# Prepo

A Python package for preprocessing pandas DataFrames, with a focus on automatic data type detection, cleaning, and scaling.

## Installation

```bash
pip install prepo
```

## Usage

```python
import pandas as pd
from prepo import FeaturePreProcessor

# Create a processor instance
processor = FeaturePreProcessor()

# Load your data
df = pd.read_csv('data/raw/your_data.csv')

# Process the data
processed_df = processor.process(
    df, 
    drop_na=True,           # Drop rows with missing values
    scaler_type='standard', # Scale numeric features using standard scaling
    remove_outlier=True     # Remove outliers
)

# Save the processed data
processed_df.to_csv('data/processed/processed_data.csv', index=False)
```

## Data Type Detection

The package automatically detects the following data types:

- **temporal**: Date and time columns
- **binary**: Columns with only two unique values
- **percentage**: Columns with values between 0 and 1, or columns with names containing "perc", "rating", etc.
- **price**: Columns with names containing "price", "cost", "revenue", etc.
- **id**: Columns with names ending or starting with "id"
- **numeric**: General numeric columns
- **string**: Short text columns
- **text**: Long text columns

## Project Structure

```
prepo/
├── data/               # Data directory
│   ├── raw/            # Raw data files
│   ├── processed/      # Processed data files
│   └── test/           # Test data files
├── src/                # Source code
│   └── prepo/          # Main package
│       ├── __init__.py        # Package initialization
│       └── preprocessor.py    # Core preprocessing functionality
├── tests/              # Test directory
│   ├── __init__.py     # Test package initialization
│   └── test_preprocessor.py  # Tests for preprocessor
├── examples/           # Example scripts
│   └── basic_usage.py  # Basic usage example
├── README.md           # Project documentation
├── LICENSE             # License information
└── setup.py            # Package installation script
```

## Demo
[preposc.streamlit.app](https://preposc.streamlit.app/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
