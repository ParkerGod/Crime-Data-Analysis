"""Analysis module for Crime Data Analysis.

This module contains all data analysis functions for the 8 objectives:
1. Top 10 Crime Categories
2. Time-Series Analysis of Crime Trends by Month
3. Crime Hotspot Detection (Grid-Based Heatmap data)
4. Victim Age Distribution by Crime Type and Gender
5. Top 5 Weapons Used in Crimes
6. Victim Age Distribution (Histogram data)
7. Crime Distribution by Status Description
8. Monthly Crime Trends by Area in 2020
"""

from typing import Tuple, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime

import config


def analyze_top_crimes(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """Analyze top N crime categories.

    Args:
        df: Cleaned crime DataFrame.
        top_n: Number of top crimes to return.

    Returns:
        Series with crime counts, indexed by crime description.
    """
    crime_counts = df['Crm Cd Desc'].value_counts()
    top_crimes = crime_counts.head(top_n)

    # Apply short labels mapping
    top_crimes = top_crimes.copy()
    top_crimes.index = top_crimes.index.map(
        lambda x: config.CRIME_SHORT_LABELS.get(x, x)
    )

    return top_crimes


def analyze_crime_trends_by_month(df: pd.DataFrame) -> pd.Series:
    """Analyze crime trends aggregated by month across all years.

    Args:
        df: Cleaned crime DataFrame with 'Month' column.

    Returns:
        Series with crime counts grouped by month.
    """
    return df.groupby('Month').size()


def analyze_crime_hotspots(
    df: pd.DataFrame,
    bins: int = 4
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Analyze crime density for hotspot detection.

    Args:
        df: Cleaned crime DataFrame with 'LAT' and 'LON' columns.
        bins: Number of bins for latitude and longitude.

    Returns:
        Tuple of (crime_density, lat_bins, lon_bins).
    """
    lat_bins = np.linspace(df["LAT"].min(), df["LAT"].max(), bins)
    lon_bins = np.linspace(df["LON"].min(), df["LON"].max(), bins)

    crime_density, _, _ = np.histogram2d(
        df["LAT"],
        df["LON"],
        bins=[lat_bins, lon_bins]
    )

    return crime_density, lat_bins, lon_bins


def analyze_victim_age_by_crime_and_gender(
    df: pd.DataFrame,
    top_n_crimes: int = 5
) -> pd.DataFrame:
    """Analyze victim age distribution by top crime types and gender.

    Args:
        df: Cleaned crime DataFrame.
        top_n_crimes: Number of top crimes to include.

    Returns:
        Filtered DataFrame for top crimes with valid ages.
    """
    # Filter valid ages
    df_valid = df[
        (df['Vict Age'] > config.MIN_VALID_AGE) &
        (df['Vict Age'] <= config.MAX_VALID_AGE)
    ]

    # Get top N crimes
    top5_crimes = df_valid['Crm Cd Desc'].value_counts().head(top_n_crimes).index

    # Filter for top crimes
    df_top5 = df_valid[df_valid['Crm Cd Desc'].isin(top5_crimes)]

    return df_top5


def analyze_top_weapons(df: pd.DataFrame, top_n: int = 5) -> pd.Series:
    """Analyze top N weapons used in crimes.

    Args:
        df: Cleaned crime DataFrame.
        top_n: Number of top weapons to return.

    Returns:
        Series with weapon counts.
    """
    return df['Weapon Desc'].value_counts().head(top_n)


def analyze_victim_age_distribution(
    df: pd.DataFrame
) -> pd.DataFrame:
    """Get victim age distribution data for histogram.

    Args:
        df: Cleaned crime DataFrame.

    Returns:
        Filtered DataFrame with valid victim ages.
    """
    return df[
        (df['Vict Age'] > config.MIN_VALID_AGE) &
        (df['Vict Age'] <= config.MAX_VALID_AGE)
    ]


def analyze_crime_status_distribution(df: pd.DataFrame) -> pd.Series:
    """Analyze crime distribution by status description.

    Args:
        df: Cleaned crime DataFrame.

    Returns:
        Series with crime counts by status.
    """
    return df['Status Desc'].value_counts()


def analyze_monthly_crime_by_area_2020(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze monthly crime trends by area for year 2020.

    Args:
        df: Cleaned crime DataFrame with 'Year', 'Month', and 'AREA NAME' columns.

    Returns:
        DataFrame with months as index and areas as columns.
    """
    # Create month abbreviation
    df = df.copy()
    df['Month_Abbr'] = df['DATE OCC'].dt.strftime('%b')

    # Filter for 2020
    df_2020 = df[df['Year'] == 2020].copy()

    # Set categorical month order
    df_2020['Month_Abbr'] = pd.Categorical(
        df_2020['Month_Abbr'],
        categories=config.MONTH_ORDER,
        ordered=True
    )

    # Group by month and area
    monthly_crimes = df_2020.groupby(
        ['Month_Abbr', 'AREA NAME'],
        observed=False
    ).size().unstack(fill_value=0)

    return monthly_crimes


def get_latitude_longitude_bounds(df: pd.DataFrame) -> Tuple[float, float, float, float]:
    """Get the min/max latitude and longitude values.

    Args:
        df: Cleaned crime DataFrame with 'LAT' and 'LON' columns.

    Returns:
        Tuple of (lat_min, lat_max, lon_min, lon_max).
    """
    return (
        df["LAT"].min(),
        df["LAT"].max(),
        df["LON"].min(),
        df["LON"].max()
    )
