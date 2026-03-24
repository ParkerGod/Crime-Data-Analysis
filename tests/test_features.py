"""Unit tests for feature engineering module."""

import pytest
import pandas as pd
from datetime import datetime
from src.crime_analysis.features import (
    parse_date,
    extract_date_features,
    extract_time_features,
    create_features
)

class TestFeatures:
    """Test cases for feature engineering functions."""
    
    def test_parse_date(self):
        """Test date parsing with different formats."""
        # Test various date formats
        test_cases = [
            ("01/15/2023 12:00:00 AM", datetime(2023, 1, 15, 0, 0, 0)),
            ("02/20/2023 03:30:00 PM", datetime(2023, 2, 20, 15, 30, 0)),
            ("12/31/2022", datetime(2022, 12, 31, 0, 0, 0)),
            ("2023-06-15 14:30:00", datetime(2023, 6, 15, 14, 30, 0)),
        ]
        
        for date_str, expected in test_cases:
            result = parse_date(date_str)
            assert result is not None, f"Failed to parse: {date_str}"
            assert result == expected, f"Expected {expected}, got {result}"
    
    def test_parse_date_invalid(self):
        """Test parsing invalid date strings."""
        invalid_dates = [
            "invalid date",
            "",
            None,
            "99/99/9999"
        ]
        
        for date_str in invalid_dates:
            result = parse_date(date_str)
            assert result is None or pd.isna(result), f"Should return None for: {date_str}"
    
    def test_extract_date_features(self):
        """Test extraction of date-based features."""
        df = pd.DataFrame({
            "DATE OCC": [
                "01/15/2023 12:00:00 AM",  # Sunday (6)
                "02/20/2023 03:30:00 PM",  # Monday (0)
                "12/25/2022 10:00:00 AM"   # Sunday (6)
            ]
        })
        
        result = extract_date_features(df)
        
        # Check new columns exist
        expected_columns = ["Year", "Month", "Day", "DayOfWeek", "Hour", "Quarter", "IsWeekend"]
        for col in expected_columns:
            assert col in result.columns, f"Missing column: {col}"
        
        # Verify values
        assert result["Year"].tolist() == [2023, 2023, 2022]
        assert result["Month"].tolist() == [1, 2, 12]
        assert result["Day"].tolist() == [15, 20, 25]
        assert result["DayOfWeek"].tolist() == [6, 0, 6]  # Sunday=6, Monday=0
        assert result["IsWeekend"].tolist() == [1, 0, 1]  # Sunday=weekend, Monday=weekday
    
    def test_extract_time_features(self):
        """Test extraction of time-based features."""
        df = pd.DataFrame({
            "TIME OCC": ["0030", "0915", "1445", "2200"]
        })
        
        result = extract_time_features(df)
        
        # Check new columns exist
        expected_columns = ["TimeHour", "TimeMinute", "TimeOfDay"]
        for col in expected_columns:
            assert col in result.columns, f"Missing column: {col}"
        
        # Verify values
        assert result["TimeHour"].tolist() == [0, 9, 14, 22]
        assert result["TimeMinute"].tolist() == [30, 15, 45, 0]
        
        # Check time of day categories
        expected_time_of_day = ["Night", "Morning", "Afternoon", "Evening"]
        assert result["TimeOfDay"].tolist() == expected_time_of_day
    
    def test_create_features(self):
        """Test complete feature creation pipeline."""
        df = pd.DataFrame({
            "DATE OCC": ["01/15/2023 12:30:00 AM"],
            "TIME OCC": ["0030"]
        })
        
        result = create_features(df)
        
        # Check that both date and time features are created
        assert "Year" in result.columns
        assert "TimeHour" in result.columns
        assert "TimeOfDay" in result.columns
        
        # Verify combined results
        assert result["Year"].iloc[0] == 2023
        assert result["TimeHour"].iloc[0] == 0
        assert result["TimeOfDay"].iloc[0] == "Night"
