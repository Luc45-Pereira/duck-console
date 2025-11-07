"""
File reading utilities for various formats
"""
from pathlib import Path
from typing import Optional, Union

import pandas as pd


def read_csv(
    file_path: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """Read a CSV file with smart defaults
    
    Args:
        file_path: Path to CSV file
        **kwargs: Additional arguments passed to pd.read_csv
        
    Returns:
        Pandas DataFrame with the CSV contents
    """
    return pd.read_csv(file_path, **kwargs)


def read_parquet(
    file_path: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """Read a Parquet file
    
    Args:
        file_path: Path to Parquet file
        **kwargs: Additional arguments passed to pd.read_parquet
        
    Returns:
        Pandas DataFrame with the Parquet contents
    """
    return pd.read_parquet(file_path, **kwargs)


def detect_encoding(file_path: Union[str, Path]) -> str:
    """Try to detect file encoding
    
    Args:
        file_path: Path to text file
        
    Returns:
        Detected encoding name (defaults to utf-8)
    """
    # TODO: Implement proper encoding detection
    return "utf-8"