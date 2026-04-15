"""Visualization module for Crime Data Analysis.

This module contains all visualization functions for the 8 objectives:
1. visualize_top_crimes - Bar plot for top 10 crime categories
2. visualize_crime_trends_by_month - Bar plot for monthly crime trends
3. visualize_crime_hotspots - Heatmap for crime hotspots
4. visualize_victim_age_by_crime_and_gender - Stripplot for victim age distribution
5. visualize_top_weapons - Pie chart for top 5 weapons
6. visualize_victim_age_distribution - Histogram for victim age distribution
7. visualize_crime_status_distribution - Bar plot for crime status
8. visualize_monthly_crime_by_area_2020 - Line plot for monthly trends by area
"""

from typing import Optional, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

import config


def setup_plotting_style() -> None:
    """Initialize seaborn and matplotlib plotting styles."""
    sns.set_style(config.SEABORN_STYLE)
    sns.set_palette(config.SEABORN_PALETTE)
    plt.rcParams.update(config.MATPLOTLIB_RCPARAMS)


def visualize_top_crimes(top_crimes: pd.Series) -> None:
    """Visualize top 10 crime categories as horizontal bar plot.

    Args:
        top_crimes: Series with crime counts, indexed by crime description.
    """
    plt.figure(figsize=config.FIGURE_SIZE_DEFAULT)
    sns.barplot(
        x=top_crimes.values,
        y=top_crimes.index,
        hue=top_crimes.index,
        palette=config.PALETTE_TOP_CRIMES,
        width=0.5,
        legend=False
    )
    plt.title("Top 10 Crime Categories", fontsize=config.FONT_SIZE_TITLE, weight='bold')
    plt.xlabel("Number of Crimes", fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel("Crime Type", fontsize=config.FONT_SIZE_LABEL)
    plt.xticks(fontsize=config.FONT_SIZE_TICK)
    plt.yticks(fontsize=config.FONT_SIZE_TICK_BOLD, fontweight='bold')
    plt.tight_layout()
    plt.grid(
        True,
        axis='x',
        linestyle=config.GRID_LINE_STYLE,
        alpha=config.GRID_ALPHA
    )
    plt.show()


def visualize_crime_trends_by_month(crime_trends: pd.Series) -> None:
    """Visualize crime trends by month as bar plot.

    Args:
        crime_trends: Series with crime counts grouped by month.
    """
    plt.figure(figsize=config.FIGURE_SIZE_DEFAULT)
    sns.barplot(
        x=crime_trends.index,
        y=crime_trends.values,
        hue=crime_trends.index,
        palette=config.PALETTE_MONTHLY_TRENDS,
        width=0.7,
        legend=False
    )
    plt.title(
        "Average Crime Trends by Month",
        fontsize=config.FONT_SIZE_TITLE,
        weight='bold'
    )
    plt.xlabel("Month", fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel("Number of Crimes", fontsize=config.FONT_SIZE_LABEL)
    plt.xticks(
        ticks=np.arange(12),
        labels=config.MONTH_ORDER,
        fontsize=config.FONT_SIZE_TICK
    )
    plt.yticks(fontsize=config.FONT_SIZE_TICK_BOLD, fontweight='bold')
    plt.tight_layout()
    plt.grid(
        True,
        axis='y',
        linestyle=config.GRID_LINE_STYLE,
        alpha=config.GRID_ALPHA
    )
    plt.show()


def visualize_crime_hotspots(
    crime_density: np.ndarray,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float
) -> None:
    """Visualize crime hotspots as heatmap.

    Args:
        crime_density: 2D array of crime density values.
        lat_min: Minimum latitude value.
        lat_max: Maximum latitude value.
        lon_min: Minimum longitude value.
        lon_max: Maximum longitude value.
    """
    plt.figure(figsize=config.FIGURE_SIZE_DEFAULT)
    plt.imshow(
        crime_density.T,
        cmap=config.PALETTE_HEATMAP,
        origin='lower',
        aspect='auto',
        extent=[lon_min, lon_max, lat_min, lat_max]
    )
    plt.colorbar(label='Crime Density')
    plt.title(
        "Crime Hotspots (Enhanced Heatmap)",
        fontsize=config.FONT_SIZE_TITLE,
        weight='bold'
    )
    plt.xlabel("Longitude", fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel("Latitude", fontsize=config.FONT_SIZE_LABEL)
    plt.tight_layout()
    plt.grid(
        True,
        linestyle=config.HEATMAP_GRID_LINESTYLE,
        color=config.HEATMAP_GRID_COLOR,
        alpha=config.HEATMAP_GRID_ALPHA
    )
    plt.show()


def visualize_victim_age_by_crime_and_gender(df: pd.DataFrame) -> None:
    """Visualize victim age distribution by crime type and gender as stripplot.

    Args:
        df: DataFrame filtered for top crimes with victim age and gender data.
    """
    plt.figure(figsize=(12, 6))
    sns.stripplot(
        data=df,
        x='Crm Cd Desc',
        y='Vict Age',
        hue='Vict Sex',
        jitter=True,
        dodge=True,
        alpha=0.7,
        palette=config.PALETTE_STRIPPLOT
    )
    plt.title(
        "Victim Age Distribution by Crime Type and Gender",
        fontsize=config.FONT_SIZE_TITLE,
        weight='bold'
    )
    plt.xlabel("Crime Type", fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel("Victim Age", fontsize=config.FONT_SIZE_LABEL)
    plt.xticks(rotation=25, fontsize=config.FONT_SIZE_TICK)
    plt.legend(title='Victim Sex', fontsize=config.FONT_SIZE_LEGEND)
    plt.tight_layout()
    plt.show()


def visualize_top_weapons(weapon_counts: pd.Series) -> None:
    """Visualize top 5 weapons used in crimes as pie chart.

    Args:
        weapon_counts: Series with weapon counts.
    """
    plt.figure(figsize=config.FIGURE_SIZE_PIE)

    explode = tuple([config.PIE_EXPLODE_VALUE] * len(weapon_counts))
    colors = sns.color_palette(
        config.PALETTE_PIE,
        n_colors=len(weapon_counts)
    )

    plt.pie(
        weapon_counts,
        autopct='%1.1f%%',
        startangle=120,
        colors=colors,
        textprops={
            'fontsize': config.FONT_SIZE_PIE,
            'fontweight': 'bold'
        },
        explode=explode,
        labels=None,
        pctdistance=0.85
    )

    plt.title(
        "Top 5 Weapons Used in Crimes",
        fontsize=18,
        weight='bold'
    )
    plt.axis('equal')

    # Create color-coded legend
    labels = weapon_counts.index.tolist()
    legend_handles = [
        Line2D(
            [0], [0],
            marker='o',
            color='w',
            markerfacecolor=color,
            markersize=10
        )
        for color in colors
    ]
    plt.legend(
        handles=legend_handles,
        labels=labels,
        title="Weapon Descriptions",
        loc='center left',
        bbox_to_anchor=(1.05, 0.5),
        fontsize=config.FONT_SIZE_LEGEND
    )

    plt.tight_layout()
    plt.show()


def visualize_victim_age_distribution(df: pd.DataFrame) -> None:
    """Visualize victim age distribution as histogram with KDE.

    Args:
        df: DataFrame with valid victim ages.
    """
    plt.figure(figsize=config.FIGURE_SIZE_DEFAULT)
    sns.histplot(
        df['Vict Age'],
        bins=config.HISTOGRAM_BINS,
        kde=True,
        color=config.PALETTE_HISTOGRAM
    )
    plt.title(
        "Victim Age Distribution",
        fontsize=config.FONT_SIZE_TITLE,
        weight='bold'
    )
    plt.xlabel("Age", fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel("Frequency", fontsize=config.FONT_SIZE_LABEL)
    plt.tight_layout()
    plt.show()


def visualize_crime_status_distribution(status_counts: pd.Series) -> None:
    """Visualize crime distribution by status description as bar plot.

    Args:
        status_counts: Series with crime counts by status.
    """
    plt.figure(figsize=config.FIGURE_SIZE_DEFAULT)
    status_counts.plot(
        kind='bar',
        stacked=True,
        color=sns.color_palette(config.PALETTE_STATUS_BAR)
    )
    plt.title(
        "Distribution of Crimes by Status Description",
        fontsize=config.FONT_SIZE_TITLE,
        weight='bold'
    )
    plt.xlabel("Status", fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel("Number of Crimes", fontsize=config.FONT_SIZE_LABEL)
    plt.xticks(rotation=0, fontsize=config.FONT_SIZE_TICK)
    plt.tight_layout()
    plt.show()


def visualize_monthly_crime_by_area_2020(monthly_crimes: pd.DataFrame) -> None:
    """Visualize monthly crime trends by area for 2020 as horizontal line plot.

    Args:
        monthly_crimes: DataFrame with months as index and areas as columns.
    """
    plt.figure(figsize=config.FIGURE_SIZE_LARGE)

    for area in monthly_crimes.columns:
        sns.lineplot(
            y=monthly_crimes.index,
            x=monthly_crimes[area],
            label=area,
            marker='o'
        )

    plt.title(
        "Monthly Crime Trends by Area (2020, Horizontal View)",
        fontsize=config.FONT_SIZE_TITLE,
        weight='bold'
    )
    plt.xlabel("Number of Crimes", fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel("Month", fontsize=config.FONT_SIZE_LABEL)
    plt.legend(
        title="Area",
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        fontsize=config.FONT_SIZE_LEGEND
    )
    plt.tight_layout()
    plt.show()
