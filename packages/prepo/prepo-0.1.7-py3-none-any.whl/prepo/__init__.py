"""
Prepo - A modern Python package for intelligent preprocessing of pandas DataFrames.

This package provides automatic data type detection, cleaning, and scaling capabilities
for data preprocessing workflows.
"""

from .preprocessor import FeaturePreProcessor, DataType, ScalerType

# Version handling with setuptools-scm
try:
    from ._version import __version__
except ImportError:
    # Fallback for development installs
    __version__ = "0.0.0+dev"

__all__ = ["FeaturePreProcessor", "DataType", "ScalerType", "__version__"]
