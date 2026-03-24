"""Objective 5: Analyze Top 5 Weapons Used in Crimes (matches pyproject.py)."""

import pandas as pd
import os
from src.crime_analysis.plotting import plot_top_5_weapons

def run_analysis(df: pd.DataFrame, output_dir: str) -> dict:
    """
    Run Objective 5: Top 5 Weapons Used in Crimes.
    
    Args:
        df: Preprocessed DataFrame with crime data
        output_dir: Directory to save output files
        
    Returns:
        Dictionary containing analysis results and statistics
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot - 1 plot per objective
    plot_top_5_weapons(df, output_dir, "objective_05_weapons.png")
    
    # Calculate statistics
    weapon_counts = df['Weapon Desc'].value_counts().head(5)
    
    # Save statistics to CSV
    stats_data = []
    for weapon, count in weapon_counts.items():
        percentage = round((count / len(df)) * 100, 2) if len(df) > 0 else 0
        stats_data.append({
            "Rank": len(stats_data) + 1,
            "Weapon Description": weapon[:40],
            "Count": count,
            "Percentage (%)": percentage
        })
    
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(os.path.join(output_dir, "objective_05_statistics.csv"), index=False)
    
    return {
        "objective": "05",
        "description": "Top 5 Weapons Used in Crimes",
        "total_weapon_types": df['Weapon Desc'].nunique(),
        "top_5_weapons": weapon_counts.to_dict(),
        "plots_generated": ["objective_05_weapons.png"],
        "statistics_file": "objective_05_statistics.csv"
    }
