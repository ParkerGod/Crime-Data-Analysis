"""Data loading and validation module."""

import pandas as pd
from typing import Optional
from src.crime_analysis.config import REQUIRED_COLUMNS

def load_data(file_path: str) -> pd.DataFrame:
    """Load crime data from CSV file."""
    try:
        df = pd.read_csv(file_path, low_memory=False)
        return df
    except Exception as e:
        raise IOError(f"Failed to load data from {file_path}: {str(e)}")

def validate_columns(df: pd.DataFrame) -> bool:
    """Check if all required columns are present in the DataFrame."""
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    return True

def get_data(file_path: str) -> pd.DataFrame:
    """Load and validate crime data."""
    df = load_data(file_path)
    validate_columns(df)
    return df
