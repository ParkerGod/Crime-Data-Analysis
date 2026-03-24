"""Objective 1: Analyze and Visualize Top 10 Crime Categories (matches pyproject.py)."""

import pandas as pd
import os
from src.crime_analysis.plotting import plot_top_10_crime_categories

def run_analysis(df: pd.DataFrame, output_dir: str) -> dict:
    """
    Run Objective 1: Top 10 Crime Categories.
    
    Args:
        df: Preprocessed DataFrame with crime data
        output_dir: Directory to save output files
        
    Returns:
        Dictionary containing analysis results and statistics
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot - 1 plot per objective
    plot_top_10_crime_categories(df, output_dir, "objective_01_top_crimes.png")
    
    # Calculate statistics
    crime_counts = df['Crm Cd Desc'].value_counts()
    top_crimes = crime_counts.head(10)
    
    short_labels = {
        'VEHICLE - STOLEN': 'Stolen Vehicle',
        'BATTERY - SIMPLE ASSAULT': 'Battery Assault',
        'BURGLARY FROM VEHICLE': 'Burglary (Vehicle)',
        'VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)': 'Felony Vandalism',
        'ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT': 'Aggr. Assault w/ Weapon',
        'INTIMATE PARTNER - SIMPLE ASSAULT': 'IP Assault',
        'BURGLARY': 'Burglary',
        'THEFT PLAIN - PETTY ($950 & UNDER)': 'Petty Theft',
        'THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)': 'Theft from Vehicle',
        'VANDALISM - MISDEMEANOR ($399 OR UNDER)': 'Misdemeanor Vandalism'
    }
    
    # Save statistics to CSV
    stats_data = []
    for crime_type, count in top_crimes.items():
        display_name = short_labels.get(crime_type, crime_type[:30])
        stats_data.append({
            "Rank": len(stats_data) + 1,
            "Crime Type": display_name,
            "Count": count
        })
    
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(os.path.join(output_dir, "objective_01_statistics.csv"), index=False)
    
    return {
        "objective": "01",
        "description": "Top 10 Crime Categories",
        "total_crime_types": len(crime_counts),
        "top_10_crimes": top_crimes.to_dict(),
        "plots_generated": ["objective_01_top_crimes.png"],
        "statistics_file": "objective_01_statistics.csv"
    }
