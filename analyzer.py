import pandas as pd
import numpy as np
from typing import Tuple, List
from config import CRIME_LABEL_MAPPING, MONTH_LABELS


def analyze_top_crime_categories(df: pd.DataFrame) -> pd.Series:
    crime_counts = df["Crm Cd Desc"].value_counts()
    top_crimes = crime_counts.head(10)
    top_crimes.index = top_crimes.index.map(CRIME_LABEL_MAPPING)
    return top_crimes


def analyze_crime_trends_by_month(df: pd.DataFrame) -> pd.Series:
    crime_trends_by_month = df.groupby("Month").size()
    return crime_trends_by_month


def analyze_crime_hotspots(df: pd.DataFrame) -> Tuple[np.ndarray, float, float, float, float]:
    lat_bins = np.linspace(df["LAT"].min(), df["LAT"].max(), 4)
    lon_bins = np.linspace(df["LON"].min(), df["LON"].max(), 4)
    crime_density, _, _ = np.histogram2d(df["LAT"], df["LON"], bins=[lat_bins, lon_bins])
    lon_min = df["LON"].min()
    lon_max = df["LON"].max()
    lat_min = df["LAT"].min()
    lat_max = df["LAT"].max()
    return crime_density, lon_min, lon_max, lat_min, lat_max


def analyze_victim_age_distribution(df: pd.DataFrame) -> pd.DataFrame:
    df_valid = df[(df["Vict Age"] > 0) & (df["Vict Age"] <= 100)]
    top5_crimes = df_valid["Crm Cd Desc"].value_counts().head(5).index
    df_top5 = df_valid[df_valid["Crm Cd Desc"].isin(top5_crimes)]
    return df_top5


def analyze_top_weapons(df: pd.DataFrame) -> pd.Series:
    weapon_counts = df["Weapon Desc"].value_counts().head(5)
    return weapon_counts


def analyze_victim_age_histogram(df: pd.DataFrame) -> pd.DataFrame:
    df_valid = df[(df["Vict Age"] > 0) & (df["Vict Age"] <= 100)]
    return df_valid


def analyze_crime_by_status(df: pd.DataFrame) -> pd.Series:
    status_desc_counts = df["Status Desc"].value_counts()
    return status_desc_counts


def analyze_monthly_crimes_by_area_2020(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy["MonthStr"] = df_copy["DATE OCC"].dt.strftime("%b")
    df_2020 = df_copy[df_copy["Year"] == 2020].copy()
    df_2020["MonthStr"] = pd.Categorical(
        df_2020["MonthStr"], categories=MONTH_LABELS, ordered=True
    )
    monthly_crimes = df_2020.groupby(["MonthStr", "AREA NAME"], observed=False).size().unstack(fill_value=0)
    return monthly_crimes
