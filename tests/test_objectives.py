"""Unit tests for analysis objectives."""

import pytest
import pandas as pd
import tempfile
import os
from analyses.objective_01 import run_analysis as run_analysis_01
from analyses.objective_02 import run_analysis as run_analysis_02

class TestObjectives:
    """Test cases for analysis objectives."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            "DATE OCC": [
                "01/15/2023 12:00:00 AM",
                "02/20/2023 03:30:00 PM",
                "03/10/2023 09:15:00 AM",
                "04/05/2023 06:45:00 PM",
                "05/22/2023 11:30:00 PM"
            ],
            "TIME OCC": ["0000", "1530", "0915", "1845", "2330"],
            "AREA NAME": ["Central", "West LA", "Hollywood", "Central", "West LA"],
            "Crm Cd Desc": ["Theft", "Assault", "Burglary", "Theft", "Assault"],
            "Vict Age": [30, 25, 45, 35, 28],
            "Vict Sex": ["M", "F", "M", "F", "M"],
            "LOCATION": ["Main St", "Broadway", "Sunset Blvd", "Figueroa", "Santa Monica Blvd"],
            "LAT": [34.05, 34.1, 34.08, 34.06, 34.09],
            "LON": [-118.25, -118.3, -118.32, -118.28, -118.35],
            "Year": [2023, 2023, 2023, 2023, 2023],
            "Month": [1, 2, 3, 4, 5],
            "TimeOfDay": ["Night", "Afternoon", "Morning", "Evening", "Night"]
        })
    
    def test_objective_01_basic(self, sample_data):
        """Test basic functionality of objective 01."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_analysis_01(sample_data, tmpdir)
            
            # Check result structure
            assert "objective" in result
            assert result["objective"] == "01"
            
            # Check statistics
            assert "total_incidents" in result
            assert result["total_incidents"] == 5
            
            # Check crime by year
            assert "crime_by_year" in result
            assert 2023 in result["crime_by_year"]
            assert result["crime_by_year"][2023] == 5
            
            # Check crime by area
            assert "crime_by_area" in result
            assert "Central" in result["crime_by_area"]
            assert "West LA" in result["crime_by_area"]
            
            # Check top crime types
            assert "top_crime_types" in result
            assert "Theft" in result["top_crime_types"]
    
    def test_objective_01_output_files(self, sample_data):
        """Test that objective 01 generates output files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_analysis_01(sample_data, tmpdir)
            
            # Check that output directory was created
            obj_dir = os.path.join(tmpdir)
            assert os.path.exists(obj_dir)
            
            # Check that plots were generated
            assert "plots_generated" in result
            for plot_file in result["plots_generated"]:
                assert os.path.exists(os.path.join(tmpdir, plot_file))
            
            # Check that statistics file was generated
            assert "statistics_file" in result
            stats_file = os.path.join(tmpdir, result["statistics_file"])
            assert os.path.exists(stats_file)
            
            # Verify statistics file content
            stats_df = pd.read_csv(stats_file)
            assert len(stats_df) > 0
            assert "Metric" in stats_df.columns
            assert "Value" in stats_df.columns
    
    def test_objective_02_basic(self, sample_data):
        """Test basic functionality of objective 02."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_analysis_02(sample_data, tmpdir)
            
            # Check result structure
            assert "objective" in result
            assert result["objective"] == "02"
            
            # Check victim gender distribution
            assert "victim_gender_distribution" in result
            gender_dist = result["victim_gender_distribution"]
            assert "M" in gender_dist
            assert "F" in gender_dist
            assert gender_dist["M"] == 3
            assert gender_dist["F"] == 2
            
            # Check average victim age
            assert "average_victim_age" in result
            avg_age = result["average_victim_age"]
            expected_avg = (30 + 25 + 45 + 35 + 28) / 5
            assert abs(avg_age - expected_avg) < 0.01
            
            # Check top hotspots
            assert "top_hotspots" in result
            assert len(result["top_hotspots"]) == 5  # All 5 locations
    
    def test_objective_02_output_files(self, sample_data):
        """Test that objective 02 generates output files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_analysis_02(sample_data, tmpdir)
            
            # Check that plots were generated
            assert "plots_generated" in result
            for plot_file in result["plots_generated"]:
                assert os.path.exists(os.path.join(tmpdir, plot_file))
            
            # Check that statistics file was generated
            assert "statistics_file" in result
            stats_file = os.path.join(tmpdir, result["statistics_file"])
            assert os.path.exists(stats_file)
    
    def test_objective_01_edge_cases(self):
        """Test objective 01 with edge cases (empty data, missing columns)."""
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_analysis_01(empty_df, tmpdir)
            assert result["total_incidents"] == 0
            
        # Test with minimal required columns
        minimal_df = pd.DataFrame({
            "DATE OCC": ["01/15/2023"],
            "AREA NAME": ["Central"],
            "Crm Cd Desc": ["Theft"],
            "Year": [2023],
            "Month": [1],
            "TimeOfDay": ["Morning"]
        })
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_analysis_01(minimal_df, tmpdir)
            assert result["total_incidents"] == 1
            assert "plots_generated" in result
