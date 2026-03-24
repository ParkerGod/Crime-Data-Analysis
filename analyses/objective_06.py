"""Objective 6: Victim Age Distribution (Histogram) (matches pyproject.py)."""

import pandas as pd
import os
from src.crime_analysis.plotting import plot_victim_age_histogram

def run_analysis(df: pd.DataFrame, output_dir: str) -> dict:
    """
    Run Objective 6: Victim Age Distribution (Histogram).
    
    Args:
        df: Preprocessed DataFrame with crime data
        output_dir: Directory to save output files
        
    Returns:
        Dictionary containing analysis results and statistics
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot - 1 plot per objective
    plot_victim_age_histogram(df, output_dir, "objective_06_age_histogram.png")
    
    # Calculate statistics
    df_valid = df[(df['Vict Age'] > 0) & (df['Vict Age'] <= 100)]
    
    # Age group analysis
    age_bins = [0, 18, 30, 45, 60, 100]
    age_labels = ['0-17', '18-29', '30-44', '45-59', '60+']
    df_valid['Age Group'] = pd.cut(df_valid['Vict Age'], bins=age_bins, labels=age_labels)
    age_group_counts = df_valid['Age Group'].value_counts().sort_index()
    
    # Save statistics to CSV
    stats_data = [{
        "Statistic": "Total Valid Victim Age Records",
        "Value": len(df_valid)
    }, {
        "Statistic": "Average Victim Age",
        "Value": round(df_valid['Vict Age'].mean(), 2)
    }, {
        "Statistic": "Median Victim Age",
        "Value": df_valid['Vict Age'].median()
    }, {
        "Statistic": "Most Common Age Group",
        "Value": age_group_counts.idxmax() if not age_group_counts.empty else "N/A"
    }]
    
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(os.path.join(output_dir, "objective_06_statistics.csv"), index=False)
    
    return {
        "objective": "06",
        "description": "Victim Age Distribution (Histogram)",
        "total_valid_age_records": len(df_valid),
        "average_victim_age": round(df_valid['Vict Age'].mean(), 2),
        "median_victim_age": df_valid['Vict Age'].median(),
        "age_group_distribution": age_group_counts.to_dict(),
        "plots_generated": ["objective_06_age_histogram.png"],
        "statistics_file": "objective_06_statistics.csv"
    }
