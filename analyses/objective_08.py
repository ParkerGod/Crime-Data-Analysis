"""Objective 8: Monthly Crime Trends by Area in 2020 (matches pyproject.py)."""

import pandas as pd
import os
from src.crime_analysis.plotting import plot_monthly_crime_by_area_2020

def run_analysis(df: pd.DataFrame, output_dir: str) -> dict:
    """
    Run Objective 8: Monthly Crime Trends by Area in 2020.
    
    Args:
        df: Preprocessed DataFrame with crime data
        output_dir: Directory to save output files
        
    Returns:
        Dictionary containing analysis results and statistics
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot - 1 plot per objective
    plot_monthly_crime_by_area_2020(df, output_dir, "objective_08_area_trends.png")
    
    # Calculate statistics (focus on 2020 data)
    df_2020 = df[df['Year'] == 2020].copy()
    
    area_counts = df_2020['AREA NAME'].value_counts().head(5) if 'AREA NAME' in df.columns else pd.Series()
    
    # Save statistics to CSV
    stats_data = []
    stats_data.append({
        "Metric": "Total Crimes in 2020",
        "Value": len(df_2020)
    })
    stats_data.append({
        "Metric": "Number of Areas",
        "Value": df_2020['AREA NAME'].nunique() if 'AREA NAME' in df.columns else 0
    })
    
    for area, count in area_counts.items():
        stats_data.append({
            "Metric": f"Top Area: {area}",
            "Value": count
        })
    
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(os.path.join(output_dir, "objective_08_statistics.csv"), index=False)
    
    return {
        "objective": "08",
        "description": "Monthly Crime Trends by Area in 2020",
        "total_crimes_2020": len(df_2020),
        "number_of_areas": df_2020['AREA NAME'].nunique() if 'AREA NAME' in df.columns else 0,
        "top_areas_2020": area_counts.to_dict(),
        "plots_generated": ["objective_08_area_trends.png"],
        "statistics_file": "objective_08_statistics.csv"
    }
