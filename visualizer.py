import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from config import (
    FIGSIZE_STANDARD,
    FIGSIZE_LARGE,
    FIGSIZE_PIE,
    FIGSIZE_TRENDS,
    PALETTE_TOP_CRIMES,
    PALETTE_MONTH_TRENDS,
    PALETTE_VICTIM_DIST,
    PALETTE_WEAPONS,
    PALETTE_STATUS,
    CMAP_HOTSPOTS,
    COLOR_HIST_AGE,
    MONTH_LABELS,
)


def plot_top_crime_categories(top_crimes: pd.Series) -> None:
    plt.figure(figsize=FIGSIZE_STANDARD)
    sns.barplot(x=top_crimes.values, y=top_crimes.index, palette=PALETTE_TOP_CRIMES, width=0.5)
    plt.title("Top 10 Crime Categories", fontsize=20, weight="bold")
    plt.xlabel("Number of Crimes", fontsize=16)
    plt.ylabel("Crime Type", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.grid(True, axis="x", linestyle="--", alpha=0.7)
    plt.show()


def plot_crime_trends_by_month(crime_trends_by_month: pd.Series) -> None:
    plt.figure(figsize=FIGSIZE_STANDARD)
    sns.barplot(
        x=crime_trends_by_month.index, y=crime_trends_by_month.values, palette=PALETTE_MONTH_TRENDS, width=0.7
    )
    plt.title("Average Crime Trends by Month", fontsize=20, weight="bold")
    plt.xlabel("Month", fontsize=16)
    plt.ylabel("Number of Crimes", fontsize=16)
    plt.xticks(ticks=np.arange(12), labels=MONTH_LABELS, fontsize=14)
    plt.yticks(fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.show()


def plot_crime_hotspots(
    crime_density: np.ndarray, lon_min: float, lon_max: float, lat_min: float, lat_max: float
) -> None:
    plt.figure(figsize=FIGSIZE_STANDARD)
    plt.imshow(
        crime_density.T,
        cmap=CMAP_HOTSPOTS,
        origin="lower",
        aspect="auto",
        extent=[lon_min, lon_max, lat_min, lat_max],
    )
    plt.colorbar(label="Crime Density")
    plt.title("Crime Hotspots (Enhanced Heatmap)", fontsize=20, weight="bold")
    plt.xlabel("Longitude", fontsize=16)
    plt.ylabel("Latitude", fontsize=16)
    plt.tight_layout()
    plt.grid(True, linestyle="-", color="black", alpha=0.3)
    plt.show()


def plot_victim_age_distribution(df_top5: pd.DataFrame) -> None:
    plt.figure(figsize=FIGSIZE_LARGE)
    sns.stripplot(
        data=df_top5,
        x="Crm Cd Desc",
        y="Vict Age",
        hue="Vict Sex",
        jitter=True,
        dodge=True,
        alpha=0.7,
        palette=PALETTE_VICTIM_DIST,
    )
    plt.title("Victim Age Distribution by Crime Type and Gender", fontsize=20, weight="bold")
    plt.xlabel("Crime Type", fontsize=16)
    plt.ylabel("Victim Age", fontsize=16)
    plt.xticks(rotation=25, fontsize=14)
    plt.legend(title="Victim Sex", fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_top_weapons(weapon_counts: pd.Series) -> None:
    plt.figure(figsize=FIGSIZE_PIE)
    explode = (0.1, 0.1, 0.1, 0.1, 0.1)
    colors = sns.color_palette(PALETTE_WEAPONS, n_colors=len(weapon_counts))
    plt.pie(
        weapon_counts,
        autopct="%1.1f%%",
        startangle=120,
        colors=colors,
        textprops={"fontsize": 12, "fontweight": "bold"},
        explode=explode,
        labels=None,
        pctdistance=0.85,
    )
    plt.title("Top 5 Weapons Used in Crimes", fontsize=18, weight="bold")
    plt.axis("equal")
    labels = weapon_counts.index.tolist()
    plt.legend(
        handles=[
            plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=10)
            for color in colors
        ],
        labels=labels,
        title="Weapon Descriptions",
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        fontsize=12,
    )
    plt.tight_layout()
    plt.show()


def plot_victim_age_histogram(df_valid: pd.DataFrame) -> None:
    plt.figure(figsize=FIGSIZE_STANDARD)
    sns.histplot(df_valid["Vict Age"], bins=20, kde=True, color=COLOR_HIST_AGE)
    plt.title("Victim Age Distribution", fontsize=20, weight="bold")
    plt.xlabel("Age", fontsize=16)
    plt.ylabel("Frequency", fontsize=16)
    plt.tight_layout()
    plt.show()


def plot_crime_by_status(status_desc_counts: pd.Series) -> None:
    plt.figure(figsize=FIGSIZE_STANDARD)
    status_desc_counts.plot(kind="bar", stacked=True, color=sns.color_palette(PALETTE_STATUS))
    plt.title("Distribution of Crimes by Status Description", fontsize=20, weight="bold")
    plt.xlabel("Status", fontsize=16)
    plt.ylabel("Number of Crimes", fontsize=16)
    plt.xticks(rotation=0, fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_monthly_crimes_by_area_2020(monthly_crimes: pd.DataFrame) -> None:
    plt.figure(figsize=FIGSIZE_TRENDS)
    for area in monthly_crimes.columns:
        sns.lineplot(y=monthly_crimes.index, x=monthly_crimes[area], label=area, marker="o")
    plt.title("Monthly Crime Trends by Area (2020, Horizontal View)", fontsize=20, weight="bold")
    plt.xlabel("Number of Crimes", fontsize=16)
    plt.ylabel("Month", fontsize=16)
    plt.legend(title="Area", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=14)
    plt.tight_layout()
    plt.show()
