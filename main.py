"""Main entry point for Crime Data Analysis.

This module orchestrates the complete analysis pipeline:
1. Data loading and cleaning
2. Analysis execution for 8 objectives
3. Visualization generation
4. Results export
"""

from datetime import datetime

import config
import data_loader
import analyzer
import visualizer


def main() -> None:
    """Execute the complete crime data analysis pipeline."""
    # Initialize plotting style
    visualizer.setup_plotting_style()

    # =============================================================================
    # Data Loading and Cleaning
    # =============================================================================
    df = data_loader.load_and_clean_data()

    # =============================================================================
    # OBJECTIVE 1: Analyze and Visualize Top 10 Crime Categories
    # =============================================================================
    top_crimes = analyzer.analyze_top_crimes(df, top_n=config.TOP_CRIMES_COUNT)
    visualizer.visualize_top_crimes(top_crimes)

    # =============================================================================
    # OBJECTIVE 2: Time-Series Analysis of Crime Trends by Month and Year
    # =============================================================================
    current_year = datetime.now().year
    df_filtered = data_loader.filter_by_year(df, config.MIN_YEAR, current_year)
    crime_trends_by_month = analyzer.analyze_crime_trends_by_month(df_filtered)
    visualizer.visualize_crime_trends_by_month(crime_trends_by_month)

    # =============================================================================
    # OBJECTIVE 3: Crime Hotspot Detection Using Grid-Based Heatmap
    # =============================================================================
    crime_density, lat_bins, lon_bins = analyzer.analyze_crime_hotspots(
        df, bins=config.HEATMAP_BINS
    )
    lat_min, lat_max, lon_min, lon_max = analyzer.get_latitude_longitude_bounds(df)
    visualizer.visualize_crime_hotspots(
        crime_density, lat_min, lat_max, lon_min, lon_max
    )

    # =============================================================================
    # OBJECTIVE 4: Victim Age Distribution by Crime Type and Gender
    # =============================================================================
    df_top5_crimes = analyzer.analyze_victim_age_by_crime_and_gender(
        df, top_n_crimes=config.TOP_CRIMES_FOR_AGE_ANALYSIS
    )
    visualizer.visualize_victim_age_by_crime_and_gender(df_top5_crimes)

    # =============================================================================
    # OBJECTIVE 5: Analyze Top 5 Weapons Used in Crimes
    # =============================================================================
    weapon_counts = analyzer.analyze_top_weapons(df, top_n=config.TOP_WEAPONS_COUNT)
    visualizer.visualize_top_weapons(weapon_counts)

    # =============================================================================
    # OBJECTIVE 6: Victim Age Distribution (Histogram)
    # =============================================================================
    df_valid_ages = analyzer.analyze_victim_age_distribution(df)
    visualizer.visualize_victim_age_distribution(df_valid_ages)

    # =============================================================================
    # OBJECTIVE 7: Analyze Crime Distribution by Status Description
    # =============================================================================
    status_desc_counts = analyzer.analyze_crime_status_distribution(df)
    visualizer.visualize_crime_status_distribution(status_desc_counts)

    # =============================================================================
    # OBJECTIVE 8: Monthly Crime Trends by Area in 2020
    # =============================================================================
    monthly_crimes = analyzer.analyze_monthly_crime_by_area_2020(df)
    visualizer.visualize_monthly_crime_by_area_2020(monthly_crimes)

    # =============================================================================
    # Save Results
    # =============================================================================
    data_loader.save_cleaned_data(df)
    print(config.ANALYSIS_COMPLETE_MSG)


if __name__ == "__main__":
    main()
