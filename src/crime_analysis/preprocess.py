"""Data preprocessing and cleaning module."""

import pandas as pd
import numpy as np

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values in the dataset."""
    df = df.copy()
    
    # Drop rows with critical missing information
    critical_columns = ["DATE OCC", "Crm Cd Desc", "LAT", "LON"]
    df = df.dropna(subset=critical_columns)
    
    # Fill categorical missing values with "Unknown"
    categorical_columns = ["AREA NAME", "Vict Sex"]
    for col in categorical_columns:
        df[col] = df[col].fillna("Unknown")
    
    # Fill numerical missing values with median or 0
    if "Vict Age" in df.columns:
        df["Vict Age"] = df["Vict Age"].fillna(0)
        # Convert negative ages to 0
        df["Vict Age"] = np.where(df["Vict Age"] < 0, 0, df["Vict Age"])
    
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from the dataset."""
    return df.drop_duplicates()

def filter_coordinates(df: pd.DataFrame, 
                       min_lat: float = 33.0, 
                       max_lat: float = 35.0,
                       min_lon: float = -119.0, 
                       max_lon: float = -117.0) -> pd.DataFrame:
    """Filter out invalid coordinates (assuming Los Angeles area)."""
    df = df.copy()
    df = df[(df["LAT"] >= min_lat) & (df["LAT"] <= max_lat)]
    df = df[(df["LON"] >= min_lon) & (df["LON"] <= max_lon)]
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all preprocessing steps."""
    df = df.copy()
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = filter_coordinates(df)
    return df
