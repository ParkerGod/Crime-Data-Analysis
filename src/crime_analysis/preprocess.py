import pandas as pd
from typing import Optional


class DataCleaner:
    def __init__(self):
        self.fill_values = {
            "Mocodes": "Null",
            "Vict Sex": "Unknown",
            "Vict Descent": "Unknown",
            "Premis Desc": "Unknown",
            "Weapon Desc": "Unknown",
            "Weapon Used Cd": "N/A",
            "Crm Cd 1": "N/A",
            "Crm Cd 2": "N/A",
            "Crm Cd 3": "N/A"
        }

    def fill_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for column, fill_value in self.fill_values.items():
            if column in df.columns:
                df[column] = df[column].fillna(fill_value)
        return df

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates()

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.fill_missing_values(df)
        df = self.remove_duplicates(df)
        return df

    def filter_by_year_range(
        self,
        df: pd.DataFrame,
        year_column: str,
        year_start: int,
        year_end: int
    ) -> pd.DataFrame:
        if year_column not in df.columns:
            raise ValueError(f"Year column '{year_column}' not found in DataFrame")
        return df[(df[year_column] >= year_start) & (df[year_column] <= year_end)]

    def filter_valid_victim_ages(
        self,
        df: pd.DataFrame,
        age_column: str = "Vict Age",
        min_age: int = 1,
        max_age: int = 100
    ) -> pd.DataFrame:
        if age_column not in df.columns:
            raise ValueError(f"Age column '{age_column}' not found in DataFrame")
        return df[(df[age_column] > min_age) & (df[age_column] <= max_age)]


def clean_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaner = DataCleaner()
    return cleaner.clean_data(df)
