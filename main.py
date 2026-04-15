import config
import data_loader
import analyzer
import visualizer


def main() -> None:
    config.setup_plot_style()
    
    df, df_filtered = data_loader.load_and_prepare_data()
    
    top_crimes = analyzer.analyze_top_crimes(df)
    visualizer.plot_top_crimes(top_crimes)
    
    monthly_trends = analyzer.analyze_monthly_trends(df_filtered)
    visualizer.plot_monthly_trends(monthly_trends)
    
    crime_density, lat_edges, lon_edges = analyzer.analyze_crime_hotspots(df)
    hotspot_data = {
        'density': crime_density,
        'lat_edges': lat_edges,
        'lon_edges': lon_edges,
        'lat_min': df["LAT"].min(),
        'lat_max': df["LAT"].max(),
        'lon_min': df["LON"].min(),
        'lon_max': df["LON"].max()
    }
    visualizer.plot_crime_hotspots(hotspot_data)
    
    df_top5, top5_crimes = analyzer.analyze_age_by_crime_gender(df)
    age_crime_data = {
        'data': df_top5,
        'top5_crimes': top5_crimes
    }
    visualizer.plot_age_by_crime_gender(age_crime_data)
    
    top_weapons = analyzer.analyze_top_weapons(df)
    visualizer.plot_top_weapons(top_weapons)
    
    age_distribution = analyzer.analyze_age_distribution(df)
    visualizer.plot_age_distribution(age_distribution)
    
    status_distribution = analyzer.analyze_status_distribution(df)
    visualizer.plot_status_distribution(status_distribution)
    
    area_monthly_trends = analyzer.analyze_area_monthly_trends(df)
    visualizer.plot_area_monthly_trends(area_monthly_trends)
    
    data_loader.save_data(df)
    
    print("-----Analysis Done!-------")


if __name__ == "__main__":
    main()
