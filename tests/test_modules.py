import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.crime_analysis.config import Config
from src.crime_analysis.preprocess import DataCleaner, clean_crime_data
from src.crime_analysis.features import FeatureEngineer, extract_date_features
from src.crime_analysis.data import DataLoader


class TestConfig:
    def test_default_config(self):
        config = Config()
        assert config.input_file == "Crime_Data.csv"
        assert config.output_dir == "output"
        assert config.year_start == 2000
        assert config.lat_bins == 4
        assert config.lon_bins == 4
        assert config.show_plots == False

    def test_year_end_defaults_to_current_year(self):
        config = Config()
        assert config.year_end == datetime.now().year

    def test_custom_config(self):
        config = Config(
            input_file="custom.csv",
            output_dir="custom_output",
            year_start=2010,
            year_end=2020,
            lat_bins=10,
            lon_bins=10
        )
        assert config.input_file == "custom.csv"
        assert config.output_dir == "custom_output"
        assert config.year_start == 2010
        assert config.year_end == 2020
        assert config.lat_bins == 10
        assert config.lon_bins == 10

    def test_required_columns_exist(self):
        config = Config()
        assert "DR_NO" in config.required_columns
        assert "DATE OCC" in config.required_columns
        assert "LAT" in config.required_columns
        assert "LON" in config.required_columns


class TestDataCleaner:
    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            "Mocodes": [None, "ABC", None],
            "Vict Sex": [None, "M", "F"],
            "Vict Descent": [None, "H", "W"],
            "Premis Desc": [None, "STREET", "HOUSE"],
            "Weapon Desc": [None, "GUN", None],
            "Weapon Used Cd": [None, 100, None],
            "Crm Cd 1": [None, 510, None],
            "Crm Cd 2": [None, None, None],
            "Crm Cd 3": [None, None, None]
        })

    def test_fill_missing_values(self, sample_df):
        cleaner = DataCleaner()
        result = cleaner.fill_missing_values(sample_df)
        assert result["Mocodes"].iloc[0] == "Null"
        assert result["Mocodes"].iloc[1] == "ABC"
        assert result["Vict Sex"].iloc[0] == "Unknown"
        assert result["Weapon Used Cd"].iloc[0] == "N/A"

    def test_remove_duplicates(self):
        df = pd.DataFrame({
            "DR_NO": [1, 2, 2, 3],
            "Crm Cd": [100, 200, 200, 300]
        })
        cleaner = DataCleaner()
        result = cleaner.remove_duplicates(df)
        assert len(result) == 3

    def test_clean_data(self, sample_df):
        cleaner = DataCleaner()
        result = cleaner.clean_data(sample_df)
        assert result["Mocodes"].isna().sum() == 0
        assert result["Vict Sex"].isna().sum() == 0

    def test_filter_valid_victim_ages(self):
        df = pd.DataFrame({
            "Vict Age": [0, 25, 50, 100, 150, -5]
        })
        cleaner = DataCleaner()
        result = cleaner.filter_valid_victim_ages(df)
        assert len(result) == 3
        assert result["Vict Age"].tolist() == [25, 50, 100]


class TestFeatureEngineer:
    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            "DATE OCC": ["2020-01-15", "2020-06-20", "2020-12-25"]
        })

    def test_parse_date_column(self, sample_df):
        engineer = FeatureEngineer()
        result = engineer.parse_date_column(sample_df)
        assert pd.api.types.is_datetime64_any_dtype(result["DATE OCC"])

    def test_extract_date_features(self, sample_df):
        engineer = FeatureEngineer()
        result = engineer.parse_date_column(sample_df)
        result = engineer.extract_date_features(result)
        assert "Year" in result.columns
        assert "Month" in result.columns
        assert "Day" in result.columns
        assert result["Year"].iloc[0] == 2020
        assert result["Month"].iloc[0] == 1
        assert result["Day"].iloc[0] == 15

    def test_extract_date_features_year_month_day(self, sample_df):
        engineer = FeatureEngineer()
        result = engineer.add_all_date_features(sample_df)
        assert result["Year"].iloc[0] == 2020
        assert result["Month"].iloc[1] == 6
        assert result["Day"].iloc[2] == 25

    def test_create_month_categorical(self, sample_df):
        engineer = FeatureEngineer()
        result = engineer.add_all_date_features(sample_df)
        result = engineer.create_month_categorical(result)
        assert pd.api.types.is_categorical_dtype(result["MonthName"])

    def test_invalid_date_handling(self):
        df = pd.DataFrame({
            "DATE OCC": ["2020-01-15", "invalid_date", "2020-12-25"]
        })
        engineer = FeatureEngineer()
        result = engineer.parse_date_column(df, errors="coerce")
        assert pd.isna(result["DATE OCC"].iloc[1])


class TestDataLoader:
    def test_validate_columns_all_present(self):
        config = Config()
        loader = DataLoader(config)
        df = pd.DataFrame({col: [] for col in config.required_columns})
        missing = loader.validate_columns(df)
        assert missing == []

    def test_validate_columns_some_missing(self):
        config = Config()
        loader = DataLoader(config)
        df = pd.DataFrame({"DR_NO": [], "DATE OCC": []})
        missing = loader.validate_columns(df)
        assert len(missing) > 0
        assert "LAT" in missing
        assert "LON" in missing

    def test_check_data_quality(self):
        config = Config()
        loader = DataLoader(config)
        df = pd.DataFrame({
            "DR_NO": [1, 2, 2],
            "DATE OCC": ["2020-01-01", "2020-01-02", "2020-01-02"],
            "LAT": [34.0, 34.1, 34.1],
            "LON": [-118.0, -118.1, -118.1]
        })
        quality = loader.check_data_quality(df)
        assert quality["total_rows"] == 3
        assert quality["duplicate_rows"] == 1


class TestObjectiveResults:
    def test_objective_01_result_structure(self):
        from analyses.objective_01 import analyze
        df = pd.DataFrame({
            "Crm Cd Desc": ["VEHICLE - STOLEN", "BATTERY - SIMPLE ASSAULT", "VEHICLE - STOLEN"]
        })
        config = Config()
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            result, fig_path = analyze(df, config, Path(tmpdir))
            assert "top_10_crimes" in result
            assert "total_crimes_analyzed" in result
            assert result["total_crimes_analyzed"] == 3

    def test_objective_06_result_structure(self):
        from analyses.objective_06 import analyze
        df = pd.DataFrame({
            "Vict Age": [25, 30, 35, 40, 45, 0, 150]
        })
        config = Config()
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            result, fig_path = analyze(df, config, Path(tmpdir))
            assert "total_valid_victims" in result
            assert "age_statistics" in result
            assert result["total_valid_victims"] == 5
            assert result["age_statistics"]["mean"] == 35.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
