"""Objective 4: Victim Age Distribution by Crime Type and Gender (matches pyproject.py)."""

import pandas as pd
import os
from src.crime_analysis.plotting import plot_victim_age_distribution_by_crime_gender

def run_analysis(df: pd.DataFrame, output_dir: str) -> dict:
    """
    Run Objective 4: Victim Age Distribution by Crime Type and Gender.
    
    Args:
        df: Preprocessed DataFrame with crime data
        output_dir: Directory to save output files
        
    Returns:
        Dictionary containing analysis results and statistics
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot - 1 plot per objective
    plot_victim_age_distribution_by_crime_gender(df, output_dir, "objective_04_victim_age.png")
    
    # Calculate statistics
    df_valid = df[(df['Vict Age'] > 0) & (df['Vict Age'] <= 100)]
    top5_crimes = df_valid['Crm Cd Desc'].value_counts().head(5)
    
    # Summary statistics by crime type
    crime_stats = []
    for crime_type in top5_crimes.index:
        crime_data = df_valid[df_valid['Crm Cd Desc'] == crime_type]
        crime_stats.append({
            "Crime Type": crime_type[:30],
            "Total Victims": len(crime_data),
            "Avg Age": round(crime_data['Vict Age'].mean(), 2),
            "Min Age": crime_data['Vict Age'].min(),
            "Max Age": crime_data['Vict Age'].max()
        })
    
    stats_df = pd.DataFrame(crime_stats)
    stats_df.to_csv(os.path.join(output_dir, "objective_04_statistics.csv"), index=False)
    
    return {
        "objective": "04",
        "description": "Victim Age Distribution by Crime Type and Gender",
        "top_5_crime_types": top5_crimes.to_dict(),
        "total_valid_victims": len(df_valid),
        "overall_avg_victim_age": round(df_valid['Vict Age'].mean(), 2),
        "plots_generated": ["objective_04_victim_age.png"],
        "statistics_file": "objective_04_statistics.csv"
    }
