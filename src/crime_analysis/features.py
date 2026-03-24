"""Feature engineering module."""

import pandas as pd
from datetime import datetime
from src.crime_analysis.config import DATE_FORMATS

def parse_date(date_str: str) -> datetime:
    """Parse date string with multiple possible formats."""
    if pd.isna(date_str):
        return None
    
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(str(date_str).strip(), fmt)
        except (ValueError, TypeError):
            continue
    return None

def extract_date_features(df: pd.DataFrame, date_column: str = "DATE OCC") -> pd.DataFrame:
    """Extract year, month, day, and other date features from date column."""
    df = df.copy()
    
    # Parse dates
    df["parsed_date"] = df[date_column].apply(parse_date)
    
    # Extract features
    df["Year"] = df["parsed_date"].dt.year
    df["Month"] = df["parsed_date"].dt.month
    df["Day"] = df["parsed_date"].dt.day
    df["DayOfWeek"] = df["parsed_date"].dt.dayofweek  # 0 = Monday, 6 = Sunday
    df["Hour"] = df["parsed_date"].dt.hour
    df["Quarter"] = df["parsed_date"].dt.quarter
    df["IsWeekend"] = df["DayOfWeek"].isin([5, 6]).astype(int)
    
    # Drop temporary parsed_date column
    df = df.drop("parsed_date", axis=1)
    
    return df

def extract_time_features(df: pd.DataFrame, time_column: str = "TIME OCC") -> pd.DataFrame:
    """Extract time-based features from time column."""
    df = df.copy()
    
    # Convert time to string with leading zeros if needed
    df["time_str"] = df[time_column].astype(str).str.zfill(4)
    
    # Extract hour and minute
    df["TimeHour"] = df["time_str"].str[:2].astype(int)
    df["TimeMinute"] = df["time_str"].str[2:].astype(int)
    
    # Create time of day categories
    df["TimeOfDay"] = pd.cut(
        df["TimeHour"],
        bins=[-1, 6, 12, 18, 24],
        labels=["Night", "Morning", "Afternoon", "Evening"]
    )
    
    df = df.drop("time_str", axis=1)
    return df

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create all features from the dataset."""
    df = df.copy()
    df = extract_date_features(df)
    df = extract_time_features(df)
    return df
