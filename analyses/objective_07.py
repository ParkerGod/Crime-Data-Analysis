"""Objective 7: Analyze Crime Distribution by Status Description (matches pyproject.py)."""

import pandas as pd
import os
from src.crime_analysis.plotting import plot_crime_by_status

def run_analysis(df: pd.DataFrame, output_dir: str) -> dict:
    """
    Run Objective 7: Crime Distribution by Status Description.
    
    Args:
        df: Preprocessed DataFrame with crime data
        output_dir: Directory to save output files
        
    Returns:
        Dictionary containing analysis results and statistics
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot - 1 plot per objective
    plot_crime_by_status(df, output_dir, "objective_07_status.png")
    
    # Calculate statistics
    status_desc_counts = df['Status Desc'].value_counts()
    
    # Save statistics to CSV
    stats_data = []
    for status, count in status_desc_counts.items():
        percentage = round((count / len(df)) * 100, 2) if len(df) > 0 else 0
        stats_data.append({
            "Status Description": status,
            "Count": count,
            "Percentage (%)": percentage
        })
    
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(os.path.join(output_dir, "objective_07_statistics.csv"), index=False)
    
    return {
        "objective": "07",
        "description": "Crime Distribution by Status Description",
        "total_status_types": df['Status Desc'].nunique(),
        "status_distribution": status_desc_counts.to_dict(),
        "plots_generated": ["objective_07_status.png"],
        "statistics_file": "objective_07_statistics.csv"
    }
