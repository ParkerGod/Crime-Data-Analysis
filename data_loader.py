"""Data loading and cleaning module for Crime Data Analysis.

This module handles loading the crime dataset, cleaning missing values,
and preparing the data for analysis.
"""

from typing import Optional
import pandas as pd
import numpy as np
from datetime import datetime

import config


def load_crime_data(file_path: str) -> pd.DataFrame:
    """Load crime data from CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame containing the raw crime data.
    """
    df = pd.read_csv(file_path)
    return df


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values according to configuration.

    Args:
        df: Raw DataFrame with potential missing values.

    Returns:
        DataFrame with missing values filled.
    """
    df = df.copy()
    for column, fill_value in config.FILLNA_VALUES.items():
        if column in df.columns:
            df[column] = df[column].fillna(fill_value)
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from the DataFrame.

    Args:
        df: DataFrame potentially containing duplicates.

    Returns:
        DataFrame with duplicates removed.
    """
    return df.drop_duplicates()


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse date columns and extract year, month, day.

    Args:
        df: DataFrame with date columns.

    Returns:
        DataFrame with parsed dates and extracted components.
    """
    df = df.copy()
    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], errors='coerce')
    df['Year'] = df['DATE OCC'].dt.year
    df['Month'] = df['DATE OCC'].dt.month
    df['Day'] = df['DATE OCC'].dt.day
    return df


def filter_by_year(df: pd.DataFrame, min_year: int, max_year: int) -> pd.DataFrame:
    """Filter DataFrame by year range.

    Args:
        df: DataFrame with 'Year' column.
        min_year: Minimum year to include.
        max_year: Maximum year to include.

    Returns:
        Filtered DataFrame.
    """
    return df[(df['Year'] >= min_year) & (df['Year'] <= max_year)]


def get_valid_age_data(df: pd.DataFrame, min_age: int, max_age: int) -> pd.DataFrame:
    """Filter DataFrame for valid age ranges.

    Args:
        df: DataFrame with 'Vict Age' column.
        min_age: Minimum valid age.
        max_age: Maximum valid age.

    Returns:
        Filtered DataFrame with valid ages.
    """
    return df[(df['Vict Age'] > min_age) & (df['Vict Age'] <= max_age)]


def load_and_clean_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """Complete data loading and cleaning pipeline.

    Args:
        file_path: Optional path to CSV file. Uses config default if not provided.

    Returns:
        Cleaned and processed DataFrame ready for analysis.
    """
    if file_path is None:
        file_path = config.DATA_PATH

    # Load data
    df = load_crime_data(file_path)

    # Clean missing values
    df = clean_missing_values(df)

    # Remove duplicates
    df = remove_duplicates(df)

    # Parse dates
    df = parse_dates(df)

    return df


def save_cleaned_data(df: pd.DataFrame, output_path: Optional[str] = None) -> None:
    """Save cleaned data to CSV file.

    Args:
        df: Cleaned DataFrame to save.
        output_path: Optional output path. Uses config default if not provided.
    """
    if output_path is None:
        output_path = config.OUTPUT_CSV_PATH
    df.to_csv(output_path, index=False)
