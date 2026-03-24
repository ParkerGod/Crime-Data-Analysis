import pandas as pd
from pathlib import Path
from typing import List, Optional
from .config import Config


class DataLoader:
    def __init__(self, config: Config):
        self.config = config

    def load_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        path = Path(file_path) if file_path else self.config.input_path
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")
        df = pd.read_csv(path)
        return df

    def validate_columns(self, df: pd.DataFrame) -> List[str]:
        missing_columns = []
        for col in self.config.required_columns:
            if col not in df.columns:
                missing_columns.append(col)
        return missing_columns

    def check_data_quality(self, df: pd.DataFrame) -> dict:
        quality_report = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_columns": self.validate_columns(df),
            "null_counts": df.isnull().sum().to_dict(),
            "duplicate_rows": df.duplicated().sum()
        }
        return quality_report

    def load_and_validate(self, file_path: Optional[str] = None) -> pd.DataFrame:
        df = self.load_data(file_path)
        missing = self.validate_columns(df)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        return df


def load_crime_data(config: Config) -> pd.DataFrame:
    loader = DataLoader(config)
    return loader.load_and_validate()
