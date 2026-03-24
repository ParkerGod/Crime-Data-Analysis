"""Objective 2: Time-Series Analysis of Crime Trends by Month (matches pyproject.py)."""

import pandas as pd
import os
from src.crime_analysis.plotting import plot_crime_trends_by_month

def run_analysis(df: pd.DataFrame, output_dir: str) -> dict:
    """
    Run Objective 2: Crime Trends by Month.
    
    Args:
        df: Preprocessed DataFrame with crime data
        output_dir: Directory to save output files
        
    Returns:
        Dictionary containing analysis results and statistics
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot - 1 plot per objective
    plot_crime_trends_by_month(df, output_dir, "objective_02_monthly_trends.png")
    
    # Calculate statistics
    crime_trends_by_month = df.groupby('Month').size()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Save statistics to CSV
    stats_data = []
    for month_num, count in crime_trends_by_month.items():
        stats_data.append({
            "Month": month_names[int(month_num) - 1] if month_num <= 12 else str(month_num),
            "Month Number": int(month_num),
            "Number of Crimes": count
        })
    
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(os.path.join(output_dir, "objective_02_statistics.csv"), index=False)
    
    return {
        "objective": "02",
        "description": "Time-Series Analysis of Crime Trends by Month",
        "peak_month": crime_trends_by_month.idxmax() if not crime_trends_by_month.empty else None,
        "lowest_month": crime_trends_by_month.idxmin() if not crime_trends_by_month.empty else None,
        "monthly_crime_counts": crime_trends_by_month.to_dict(),
        "plots_generated": ["objective_02_monthly_trends.png"],
        "statistics_file": "objective_02_statistics.csv"
    }
