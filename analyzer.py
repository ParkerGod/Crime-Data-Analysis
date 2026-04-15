import pandas as pd
import numpy as np
from typing import Tuple
import config


def analyze_top_crimes(df: pd.DataFrame) -> pd.Series:
    crime_counts = df['Crm Cd Desc'].value_counts()
    top_crimes = crime_counts.head(config.TOP_CRIMES_COUNT)
    top_crimes.index = top_crimes.index.map(
        lambda x: config.CRIME_SHORT_LABELS.get(x, x)
    )
    return top_crimes


def analyze_monthly_trends(df: pd.DataFrame) -> pd.Series:
    crime_trends_by_month = df.groupby('Month').size()
    return crime_trends_by_month


def analyze_crime_hotspots(
    df: pd.DataFrame
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    lat_bins = np.linspace(df["LAT"].min(), df["LAT"].max(), config.GRID_BINS)
    lon_bins = np.linspace(df["LON"].min(), df["LON"].max(), config.GRID_BINS)
    
    crime_density, lat_edges, lon_edges = np.histogram2d(
        df["LAT"], df["LON"], bins=[lat_bins, lon_bins]
    )
    
    return crime_density, lat_edges, lon_edges


def analyze_age_by_crime_gender(
    df: pd.DataFrame
) -> Tuple[pd.DataFrame, list]:
    df_valid = df[
        (df['Vict Age'] > config.VALID_AGE_MIN) &
        (df['Vict Age'] <= config.VALID_AGE_MAX)
    ]
    
    top5_crimes = df_valid['Crm Cd Desc'].value_counts().head(
        config.TOP5_CRIMES_COUNT
    ).index
    
    df_top5 = df_valid[df_valid['Crm Cd Desc'].isin(top5_crimes)]
    
    return df_top5, top5_crimes.tolist()


def analyze_top_weapons(df: pd.DataFrame) -> pd.Series:
    weapon_counts = df['Weapon Desc'].value_counts().head(config.TOP_WEAPONS_COUNT)
    return weapon_counts


def analyze_age_distribution(df: pd.DataFrame) -> pd.Series:
    df_valid = df[
        (df['Vict Age'] > config.VALID_AGE_MIN) &
        (df['Vict Age'] <= config.VALID_AGE_MAX)
    ]
    return df_valid['Vict Age']


def analyze_status_distribution(df: pd.DataFrame) -> pd.Series:
    status_desc_counts = df['Status Desc'].value_counts()
    return status_desc_counts


def analyze_area_monthly_trends(
    df: pd.DataFrame,
    year: int = config.TARGET_YEAR
) -> pd.DataFrame:
    df_year = df[df['Year'] == year].copy()
    df_year['Month'] = df_year['DATE OCC'].dt.strftime('%b')
    df_year['Month'] = pd.Categorical(
        df_year['Month'],
        categories=config.MONTH_ORDER,
        ordered=True
    )
    
    monthly_crimes = df_year.groupby(['Month', 'AREA NAME'], observed=False).size().unstack(
        fill_value=0
    )
    
    return monthly_crimes
