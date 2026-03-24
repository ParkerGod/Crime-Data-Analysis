import pandas as pd
from typing import Optional, List


class FeatureEngineer:
    def __init__(self, date_column: str = "DATE OCC"):
        self.date_column = date_column

    def parse_date_column(
        self,
        df: pd.DataFrame,
        date_column: Optional[str] = None,
        errors: str = "coerce"
    ) -> pd.DataFrame:
        col = date_column or self.date_column
        if col not in df.columns:
            raise ValueError(f"Date column '{col}' not found in DataFrame")
        df = df.copy()
        df[col] = pd.to_datetime(df[col], errors=errors)
        return df

    def extract_date_features(
        self,
        df: pd.DataFrame,
        date_column: Optional[str] = None
    ) -> pd.DataFrame:
        col = date_column or self.date_column
        if col not in df.columns:
            raise ValueError(f"Date column '{col}' not found in DataFrame")
        df = df.copy()
        df["Year"] = df[col].dt.year
        df["Month"] = df[col].dt.month
        df["Day"] = df[col].dt.day
        df["MonthName"] = df[col].dt.strftime("%b")
        return df

    def add_all_date_features(
        self,
        df: pd.DataFrame,
        date_column: Optional[str] = None
    ) -> pd.DataFrame:
        df = self.parse_date_column(df, date_column)
        df = self.extract_date_features(df, date_column)
        return df

    def create_month_categorical(
        self,
        df: pd.DataFrame,
        month_column: str = "MonthName"
    ) -> pd.DataFrame:
        month_order = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]
        df = df.copy()
        if month_column in df.columns:
            df[month_column] = pd.Categorical(
                df[month_column],
                categories=month_order,
                ordered=True
            )
        return df


def extract_date_features(df: pd.DataFrame, date_column: str = "DATE OCC") -> pd.DataFrame:
    engineer = FeatureEngineer(date_column)
    return engineer.add_all_date_features(df)
