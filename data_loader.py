import pandas as pd
from typing import Optional
from config import DATA_PATH


def load_and_clean_data(file_path: Optional[str] = None) -> pd.DataFrame:
    if file_path is None:
        file_path = DATA_PATH

    df = pd.read_csv(file_path)

    df["Mocodes"].fillna("Null", inplace=True)
    df["Vict Sex"].fillna("Unknown", inplace=True)
    df["Vict Descent"].fillna("Unknown", inplace=True)
    df["Premis Desc"].fillna("Unknown", inplace=True)
    df["Weapon Desc"].fillna("Unknown", inplace=True)
    df["Weapon Used Cd"].fillna("N/A", inplace=True)
    df["Crm Cd 1"].fillna("N/A", inplace=True)
    df["Crm Cd 2"].fillna("N/A", inplace=True)
    df["Crm Cd 3"].fillna("N/A", inplace=True)

    df.drop_duplicates(inplace=True)

    df["DATE OCC"] = pd.to_datetime(df["DATE OCC"], errors="coerce")
    df["Year"] = df["DATE OCC"].dt.year
    df["Month"] = df["DATE OCC"].dt.month
    df["Day"] = df["DATE OCC"].dt.day

    return df
