import matplotlib.pyplot as plt
import seaborn as sns
from config import (
    SEABORN_STYLE,
    SEABORN_PALETTE,
    FONT_PARAMS,
    CLEANED_DATA_PATH,
    COMPLETION_MESSAGE,
)
from data_loader import load_and_clean_data
from analyzer import (
    analyze_top_crime_categories,
    analyze_crime_trends_by_month,
    analyze_crime_hotspots,
    analyze_victim_age_distribution,
    analyze_top_weapons,
    analyze_victim_age_histogram,
    analyze_crime_by_status,
    analyze_monthly_crimes_by_area_2020,
)
from visualizer import (
    plot_top_crime_categories,
    plot_crime_trends_by_month,
    plot_crime_hotspots,
    plot_victim_age_distribution,
    plot_top_weapons,
    plot_victim_age_histogram,
    plot_crime_by_status,
    plot_monthly_crimes_by_area_2020,
)


def main() -> None:
    sns.set_style(SEABORN_STYLE)
    sns.set_palette(SEABORN_PALETTE)
    plt.rcParams.update(FONT_PARAMS)

    df = load_and_clean_data()

    top_crimes = analyze_top_crime_categories(df)
    plot_top_crime_categories(top_crimes)

    crime_trends_by_month = analyze_crime_trends_by_month(df)
    plot_crime_trends_by_month(crime_trends_by_month)

    crime_density, lon_min, lon_max, lat_min, lat_max = analyze_crime_hotspots(df)
    plot_crime_hotspots(crime_density, lon_min, lon_max, lat_min, lat_max)

    df_top5 = analyze_victim_age_distribution(df)
    plot_victim_age_distribution(df_top5)

    weapon_counts = analyze_top_weapons(df)
    plot_top_weapons(weapon_counts)

    df_valid = analyze_victim_age_histogram(df)
    plot_victim_age_histogram(df_valid)

    status_desc_counts = analyze_crime_by_status(df)
    plot_crime_by_status(status_desc_counts)

    monthly_crimes = analyze_monthly_crimes_by_area_2020(df)
    plot_monthly_crimes_by_area_2020(monthly_crimes)

    df.to_csv(CLEANED_DATA_PATH)
    print(COMPLETION_MESSAGE)


if __name__ == "__main__":
    main()
