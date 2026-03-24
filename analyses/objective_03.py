"""Objective 3: Crime Hotspot Detection Using Grid-Based Heatmap (matches pyproject.py)."""

import pandas as pd
import os
from src.crime_analysis.plotting import plot_crime_hotspots_heatmap

def run_analysis(df: pd.DataFrame, output_dir: str) -> dict:
    """
    Run Objective 3: Crime Hotspot Detection.
    
    Args:
        df: Preprocessed DataFrame with crime data
        output_dir: Directory to save output files
        
    Returns:
        Dictionary containing analysis results and statistics
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate plot - 1 plot per objective
    plot_crime_hotspots_heatmap(df, output_dir, "objective_03_hotspots.png")
    
    # Calculate statistics
    import numpy as np
    lat_bins = np.linspace(df["LAT"].min(), df["LAT"].max(), 4)
    lon_bins = np.linspace(df["LON"].min(), df["LON"].max(), 4)
    
    crime_density, _, _ = np.histogram2d(df["LAT"], df["LON"], bins=[lat_bins, lon_bins])
    
    # Find hotspot coordinates
    max_density = crime_density.max()
    max_position = np.unravel_index(crime_density.argmax(), crime_density.shape)
    
    # Save statistics to CSV
    stats_data = [{
        "Grid Cell (Row, Column)": f"({max_position[0]}, {max_position[1]})",
        "Latitude Range": f"{lat_bins[max_position[0]]:.4f} to {lat_bins[max_position[0]+1]:.4f}",
        "Longitude Range": f"{lon_bins[max_position[1]]:.4f} to {lon_bins[max_position[1]+1]:.4f}",
        "Crime Density (Count)": int(max_density)
    }]
    
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(os.path.join(output_dir, "objective_03_statistics.csv"), index=False)
    
    return {
        "objective": "03",
        "description": "Crime Hotspot Detection Using Grid-Based Heatmap",
        "grid_size": "3x3 grid",
        "max_crime_density": int(max_density),
        "hotspot_grid_position": max_position,
        "plots_generated": ["objective_03_hotspots.png"],
        "statistics_file": "objective_03_statistics.csv"
    }
