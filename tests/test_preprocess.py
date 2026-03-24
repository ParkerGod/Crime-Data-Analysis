"""Unit tests for preprocessing module."""

import pytest
import pandas as pd
import numpy as np
from src.crime_analysis.preprocess import (
    handle_missing_values,
    remove_duplicates,
    filter_coordinates,
    clean_data
)

class TestPreprocess:
    """Test cases for preprocessing functions."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            "DATE OCC": ["01/15/2023 12:00:00 AM", "02/20/2023 03:30:00 PM", None],
            "TIME OCC": ["1200", "1530", "0900"],
            "AREA NAME": ["Central", None, "West LA"],
            "Crm Cd Desc": ["Theft", "Assault", "Burglary"],
            "Vict Age": [30, -5, None],
            "Vict Sex": ["M", "F", None],
            "LOCATION": ["Main St", "Broadway", "Sunset Blvd"],
            "LAT": [34.05, 34.1, 100.0],  # Invalid latitude in third row
            "LON": [-118.25, -118.3, -200.0]  # Invalid longitude in third row
        })
    
    def test_handle_missing_values(self, sample_data):
        """Test handling of missing values."""
        result = handle_missing_values(sample_data)
        
        # Check that critical missing rows are dropped (DATE OCC is None)
        assert len(result) == 2
        
        # Check categorical columns are filled with "Unknown"
        assert result["AREA NAME"].isna().sum() == 0
        assert result["Vict Sex"].isna().sum() == 0
        
        # Check negative ages are converted to 0
        assert result["Vict Age"].iloc[1] == 0
        
        # Check numerical columns are filled
        assert result["Vict Age"].isna().sum() == 0
    
    def test_remove_duplicates(self):
        """Test duplicate removal."""
        df = pd.DataFrame({
            "A": [1, 2, 2, 3],
            "B": ["x", "y", "y", "z"]
        })
        
        result = remove_duplicates(df)
        assert len(result) == 3
    
    def test_filter_coordinates(self, sample_data):
        """Test coordinate filtering."""
        result = filter_coordinates(sample_data)
        
        # Third row has invalid coordinates
        assert len(result) == 2
        
        # Check valid coordinate ranges
        assert all(result["LAT"].between(33.0, 35.0))
        assert all(result["LON"].between(-119.0, -117.0))
    
    def test_clean_data(self, sample_data):
        """Test complete data cleaning pipeline."""
        result = clean_data(sample_data)
        
        # After all cleaning steps, we should have 2 valid rows
        # Row 0: valid
        # Row 1: valid (negative age fixed)
        # Row 2: dropped (invalid coordinates)
        assert len(result) == 2
        
        # Check no missing values in critical columns
        critical_columns = ["DATE OCC", "Crm Cd Desc", "LAT", "LON"]
        for col in critical_columns:
            assert result[col].isna().sum() == 0
