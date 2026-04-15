import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
import config


def plot_top_crimes(top_crimes: pd.Series) -> None:
    plt.figure(figsize=config.FIG_SIZE_WIDE)
    sns.barplot(
        x=top_crimes.values,
        y=top_crimes.index,
        hue=top_crimes.index,
        palette=config.PALETTE_TOP_CRIMES,
        width=config.BAR_WIDTH_NARROW,
        legend=False
    )
    plt.title(config.TITLE_TOP_CRIMES, fontsize=config.FONT_SIZE_TITLE, weight='bold')
    plt.xlabel(config.XLABEL_CRIMES, fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel(config.YLABEL_CRIME_TYPE, fontsize=config.FONT_SIZE_LABEL)
    plt.xticks(fontsize=config.FONT_SIZE_TICKS)
    plt.yticks(fontsize=config.FONT_SIZE_TICKS, fontweight='bold')
    plt.tight_layout()
    plt.grid(True, axis='x', linestyle='--', alpha=config.GRID_ALPHA)
    plt.show()


def plot_monthly_trends(crime_trends_by_month: pd.Series) -> None:
    plt.figure(figsize=config.FIG_SIZE_WIDE)
    sns.barplot(
        x=crime_trends_by_month.index,
        y=crime_trends_by_month.values,
        hue=crime_trends_by_month.index,
        palette=config.PALETTE_MONTHLY,
        width=config.BAR_WIDTH_NORMAL,
        legend=False
    )
    plt.title(config.TITLE_MONTHLY_TRENDS, fontsize=config.FONT_SIZE_TITLE, weight='bold')
    plt.xlabel(config.XLABEL_MONTH, fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel(config.YLABEL_CRIMES, fontsize=config.FONT_SIZE_LABEL)
    plt.xticks(
        ticks=np.arange(12),
        labels=config.MONTH_LABELS,
        fontsize=config.FONT_SIZE_TICKS
    )
    plt.yticks(fontsize=config.FONT_SIZE_TICKS, fontweight='bold')
    plt.tight_layout()
    plt.grid(True, axis='y', linestyle='--', alpha=config.GRID_ALPHA)
    plt.show()


def plot_crime_hotspots(hotspot_data: Dict[str, Any]) -> None:
    crime_density = hotspot_data['density']
    lat_min = hotspot_data['lat_min']
    lat_max = hotspot_data['lat_max']
    lon_min = hotspot_data['lon_min']
    lon_max = hotspot_data['lon_max']
    
    plt.figure(figsize=config.FIG_SIZE_WIDE)
    plt.imshow(
        crime_density.T,
        cmap=config.CMAP_HOTSPOTS,
        origin='lower',
        aspect='auto',
        extent=[lon_min, lon_max, lat_min, lat_max]
    )
    plt.colorbar(label='Crime Density')
    plt.title(config.TITLE_HOTSPOTS, fontsize=config.FONT_SIZE_TITLE, weight='bold')
    plt.xlabel(config.XLABEL_LONGITUDE, fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel(config.YLABEL_LATITUDE, fontsize=config.FONT_SIZE_LABEL)
    plt.tight_layout()
    plt.grid(True, linestyle='-', color='black', alpha=config.GRID_ALPHA_LIGHT)
    plt.show()


def plot_age_by_crime_gender(age_crime_data: Dict[str, Any]) -> None:
    df_top5 = age_crime_data['data']
    
    plt.figure(figsize=config.FIG_SIZE_MEDIUM)
    sns.stripplot(
        data=df_top5,
        x='Crm Cd Desc',
        y='Vict Age',
        hue='Vict Sex',
        jitter=True,
        dodge=True,
        alpha=config.STRIP_ALPHA,
        palette=config.PALETTE_AGE_GENDER
    )
    plt.title(config.TITLE_AGE_BY_CRIME, fontsize=config.FONT_SIZE_TITLE, weight='bold')
    plt.xlabel(config.XLABEL_CRIME_TYPE, fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel(config.YLABEL_VICTIM_AGE, fontsize=config.FONT_SIZE_LABEL)
    plt.xticks(rotation=25, fontsize=config.FONT_SIZE_TICKS)
    plt.legend(title='Victim Sex', fontsize=config.FONT_SIZE_LEGEND)
    plt.tight_layout()
    plt.show()


def plot_top_weapons(weapon_counts: pd.Series) -> None:
    plt.figure(figsize=config.FIG_SIZE_SQUARE)
    
    colors = sns.color_palette(
        config.PALETTE_WEAPONS,
        n_colors=len(weapon_counts)
    )
    
    plt.pie(
        weapon_counts,
        autopct='%1.1f%%',
        startangle=config.PIE_START_ANGLE,
        colors=colors,
        textprops={'fontsize': config.FONT_SIZE_PIE_PCT, 'fontweight': 'bold'},
        explode=config.PIE_EXPLODE,
        labels=None,
        pctdistance=config.PIE_PCT_DISTANCE
    )
    
    plt.title(config.TITLE_WEAPONS, fontsize=config.FONT_SIZE_TITLE - 2, weight='bold')
    plt.axis('equal')
    
    labels = weapon_counts.index.tolist()
    legend_handles = [
        plt.Line2D(
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
        fontsize=config.FONT_SIZE_LEGEND - 2
    )
    
    plt.tight_layout()
    plt.show()


def plot_age_distribution(age_data: pd.Series) -> None:
    plt.figure(figsize=config.FIG_SIZE_WIDE)
    sns.histplot(
        age_data,
        bins=config.HISTOGRAM_BINS,
        kde=True,
        color=config.COLOR_HISTOGRAM
    )
    plt.title(config.TITLE_AGE_DIST, fontsize=config.FONT_SIZE_TITLE, weight='bold')
    plt.xlabel(config.XLABEL_AGE, fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel(config.YLABEL_FREQUENCY, fontsize=config.FONT_SIZE_LABEL)
    plt.tight_layout()
    plt.show()


def plot_status_distribution(status_counts: pd.Series) -> None:
    plt.figure(figsize=config.FIG_SIZE_WIDE)
    status_counts.plot(
        kind='bar',
        stacked=True,
        color=sns.color_palette(config.PALETTE_STATUS)
    )
    plt.title(config.TITLE_STATUS, fontsize=config.FONT_SIZE_TITLE, weight='bold')
    plt.xlabel(config.XLABEL_STATUS, fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel(config.YLABEL_CRIMES, fontsize=config.FONT_SIZE_LABEL)
    plt.xticks(rotation=0, fontsize=config.FONT_SIZE_TICKS)
    plt.tight_layout()
    plt.show()


def plot_area_monthly_trends(monthly_crimes: pd.DataFrame) -> None:
    plt.figure(figsize=config.FIG_SIZE_LARGE)
    for area in monthly_crimes.columns:
        sns.lineplot(
            y=monthly_crimes.index,
            x=monthly_crimes[area],
            label=area,
            marker=config.MARKER_STYLE
        )
    
    plt.title(config.TITLE_AREA_TRENDS, fontsize=config.FONT_SIZE_TITLE, weight='bold')
    plt.xlabel(config.XLABEL_CRIMES, fontsize=config.FONT_SIZE_LABEL)
    plt.ylabel(config.YLABEL_MONTH, fontsize=config.FONT_SIZE_LABEL)
    plt.legend(
        title="Area",
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        fontsize=config.FONT_SIZE_LEGEND
    )
    plt.tight_layout()
    plt.show()
