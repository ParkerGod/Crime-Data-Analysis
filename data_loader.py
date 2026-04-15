import datetime
import pandas as pd
from typing import Tuple
import config


def load_data(file_path: str = config.DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.copy()
    
    for column, fill_value in config.FILLNA_COLUMNS.items():
        if column in df_cleaned.columns:
            if df_cleaned[column].dtype == 'float64' and fill_value == 'N/A':
                df_cleaned[column] = df_cleaned[column].astype(object)
            df_cleaned[column].fillna(fill_value, inplace=True)
    
    df_cleaned.drop_duplicates(inplace=True)
    
    return df_cleaned


def add_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_with_dates = df.copy()
    
    df_with_dates['DATE OCC'] = pd.to_datetime(
        df_with_dates['DATE OCC'], errors='coerce'
    )
    df_with_dates['Year'] = df_with_dates['DATE OCC'].dt.year
    df_with_dates['Month'] = df_with_dates['DATE OCC'].dt.month
    df_with_dates['Day'] = df_with_dates['DATE OCC'].dt.day
    
    return df_with_dates


def filter_by_year_range(
    df: pd.DataFrame,
    start_year: int = config.YEAR_FILTER_START,
    end_year: int = None
) -> pd.DataFrame:
    if end_year is None:
        end_year = datetime.datetime.now().year
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]


def filter_valid_age(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        (df['Vict Age'] > config.VALID_AGE_MIN) &
        (df['Vict Age'] <= config.VALID_AGE_MAX)
    ]


def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    return df[df['Year'] == year]


def add_month_name_column(df: pd.DataFrame) -> pd.DataFrame:
    df_result = df.copy()
    df_result['Month'] = df_result['DATE OCC'].dt.strftime('%b')
    df_result['Month'] = pd.Categorical(
        df_result['Month'],
        categories=config.MONTH_ORDER,
        ordered=True
    )
    return df_result


def save_data(df: pd.DataFrame, file_path: str = config.OUTPUT_PATH) -> None:
    df.to_csv(file_path, index=False)


def load_and_prepare_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = load_data()
    df = clean_data(df)
    df = add_date_columns(df)
    df_filtered = filter_by_year_range(df)
    return df, df_filtered
