"""Plotting utilities for crime analysis - based on pyproject.py functionality."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from typing import Optional, Tuple
from src.crime_analysis.config import DEFAULT_SHOW_PLOTS

def setup_plot_style():
    """Set up consistent plot styling based on pyproject.py."""
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    plt.rcParams.update({'font.size': 12, 'axes.titlesize': 16, 'axes.labelsize': 12})

def save_plot(filename: str, output_dir: str, show_plot: bool = DEFAULT_SHOW_PLOTS):
    """Save plot to file and optionally display it."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    if show_plot:
        plt.show()
    plt.close()

# =============================================================================
# OBJECTIVE 1: Top 10 Crime Categories Bar Plot
# =============================================================================
def plot_top_10_crime_categories(df: pd.DataFrame,
                                 output_dir: str,
                                 filename: str = "objective_01_top_crimes.png") -> Tuple[plt.Figure, plt.Axes]:
    """Plot top 10 crime categories - based on pyproject.py Objective 1."""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
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
    top_crimes.index = top_crimes.index.map(lambda x: short_labels.get(x, x[:20]))
    
    sns.barplot(x=top_crimes.values, y=top_crimes.index, palette="cubehelix", width=0.5, ax=ax)
    ax.set_title("Top 10 Crime Categories", fontsize=20, weight='bold')
    ax.set_xlabel("Number of Crimes", fontsize=16)
    ax.set_ylabel("Crime Type", fontsize=16)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    save_plot(filename, output_dir)
    return fig, ax

# =============================================================================
# OBJECTIVE 2: Time-Series Analysis of Crime Trends by Month
# =============================================================================
def plot_crime_trends_by_month(df: pd.DataFrame,
                               output_dir: str,
                               filename: str = "objective_02_monthly_trends.png") -> Tuple[plt.Figure, plt.Axes]:
    """Plot crime trends by month - based on pyproject.py Objective 2."""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    crime_trends_by_month = df.groupby('Month').size()
    
    sns.barplot(x=crime_trends_by_month.index, y=crime_trends_by_month.values, palette="crest", width=0.7, ax=ax)
    ax.set_title("Average Crime Trends by Month", fontsize=20, weight='bold')
    ax.set_xlabel("Month", fontsize=16)
    ax.set_ylabel("Number of Crimes", fontsize=16)
    ax.set_xticks(ticks=np.arange(12))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    save_plot(filename, output_dir)
    return fig, ax

# =============================================================================
# OBJECTIVE 3: Crime Hotspot Detection Using Grid-Based Heatmap
# =============================================================================
def plot_crime_hotspots_heatmap(df: pd.DataFrame,
                                output_dir: str,
                                filename: str = "objective_03_hotspots.png") -> Tuple[plt.Figure, plt.Axes]:
    """Plot crime hotspots using grid-based heatmap - based on pyproject.py Objective 3."""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    lat_bins = np.linspace(df["LAT"].min(), df["LAT"].max(), 4)
    lon_bins = np.linspace(df["LON"].min(), df["LON"].max(), 4)
    
    crime_density, _, _ = np.histogram2d(df["LAT"], df["LON"], bins=[lat_bins, lon_bins])
    
    im = ax.imshow(crime_density.T, cmap='Blues', origin='lower', aspect='auto',
                   extent=[df["LON"].min(), df["LON"].max(), df["LAT"].min(), df["LAT"].max()])
    
    plt.colorbar(im, label='Crime Density')
    ax.set_title("Crime Hotspots (Enhanced Heatmap)", fontsize=20, weight='bold')
    ax.set_xlabel("Longitude", fontsize=16)
    ax.set_ylabel("Latitude", fontsize=16)
    ax.grid(True, linestyle='-', color='black', alpha=0.3)
    
    plt.tight_layout()
    save_plot(filename, output_dir)
    return fig, ax

# =============================================================================
# OBJECTIVE 4: Victim Age Distribution by Crime Type and Gender
# =============================================================================
def plot_victim_age_distribution_by_crime_gender(df: pd.DataFrame,
                                                 output_dir: str,
                                                 filename: str = "objective_04_victim_age.png") -> Tuple[plt.Figure, plt.Axes]:
    """Plot victim age distribution by crime type and gender - based on pyproject.py Objective 4."""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    df_valid = df[(df['Vict Age'] > 0) & (df['Vict Age'] <= 100)]
    top5_crimes = df_valid['Crm Cd Desc'].value_counts().head(5).index
    df_top5 = df_valid[df_valid['Crm Cd Desc'].isin(top5_crimes)]
    
    sns.stripplot(data=df_top5, x='Crm Cd Desc', y='Vict Age', hue='Vict Sex', 
                  jitter=True, dodge=True, alpha=0.7, palette='coolwarm', ax=ax)
    
    ax.set_title("Victim Age Distribution by Crime Type and Gender", fontsize=20, weight='bold')
    ax.set_xlabel("Crime Type", fontsize=16)
    ax.set_ylabel("Victim Age", fontsize=16)
    ax.tick_params(axis='x', rotation=25, labelsize=14)
    ax.legend(title='Victim Sex', fontsize=14)
    
    plt.tight_layout()
    save_plot(filename, output_dir)
    return fig, ax

# =============================================================================
# OBJECTIVE 5: Top 5 Weapons Used in Crimes
# =============================================================================
def plot_top_5_weapons(df: pd.DataFrame,
                       output_dir: str,
                       filename: str = "objective_05_weapons.png") -> Tuple[plt.Figure, plt.Axes]:
    """Plot top 5 weapons used in crimes - based on pyproject.py Objective 5."""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(8, 8))
    
    weapon_counts = df['Weapon Desc'].value_counts().head(5)
    explode = (0.1, 0.1, 0.1, 0.1, 0.1)
    colors = sns.color_palette("Spectral", n_colors=len(weapon_counts))
    
    ax.pie(weapon_counts, autopct='%1.1f%%', startangle=120, colors=colors, 
           textprops={'fontsize': 12, 'fontweight': 'bold'}, explode=explode, labels=None, pctdistance=0.85)
    
    ax.set_title("Top 5 Weapons Used in Crimes", fontsize=18, weight='bold')
    ax.axis('equal')
    
    # Create legend
    labels = weapon_counts.index.tolist()
    ax.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) 
                      for color in colors], labels=labels, title="Weapon Descriptions", 
              loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize=12)
    
    plt.tight_layout()
    save_plot(filename, output_dir)
    return fig, ax

# =============================================================================
# OBJECTIVE 6: Victim Age Distribution (Histogram)
# =============================================================================
def plot_victim_age_histogram(df: pd.DataFrame,
                              output_dir: str,
                              filename: str = "objective_06_age_histogram.png") -> Tuple[plt.Figure, plt.Axes]:
    """Plot victim age distribution histogram - based on pyproject.py Objective 6."""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    df_valid = df[(df['Vict Age'] > 0) & (df['Vict Age'] <= 100)]
    
    sns.histplot(df_valid['Vict Age'], bins=20, kde=True, color="green", ax=ax)
    ax.set_title("Victim Age Distribution", fontsize=20, weight='bold')
    ax.set_xlabel("Age", fontsize=16)
    ax.set_ylabel("Frequency", fontsize=16)
    
    plt.tight_layout()
    save_plot(filename, output_dir)
    return fig, ax

# =============================================================================
# OBJECTIVE 7: Crime Distribution by Status Description
# =============================================================================
def plot_crime_by_status(df: pd.DataFrame,
                         output_dir: str,
                         filename: str = "objective_07_status.png") -> Tuple[plt.Figure, plt.Axes]:
    """Plot crime distribution by status description - based on pyproject.py Objective 7."""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    status_desc_counts = df['Status Desc'].value_counts()
    
    status_desc_counts.plot(kind='bar', stacked=True, color=sns.color_palette("Set2"), ax=ax)
    ax.set_title("Distribution of Crimes by Status Description", fontsize=20, weight='bold')
    ax.set_xlabel("Status", fontsize=16)
    ax.set_ylabel("Number of Crimes", fontsize=16)
    ax.tick_params(axis='x', rotation=0, labelsize=14)
    
    plt.tight_layout()
    save_plot(filename, output_dir)
    return fig, ax

# =============================================================================
# OBJECTIVE 8: Monthly Crime Trends by Area in 2020
# =============================================================================
def plot_monthly_crime_by_area_2020(df: pd.DataFrame,
                                    output_dir: str,
                                    filename: str = "objective_08_area_trends.png") -> Tuple[plt.Figure, plt.Axes]:
    """Plot monthly crime trends by area in 2020 - based on pyproject.py Objective 8."""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Get month in short format
    df['Month_Str'] = df['Month'].map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                                       7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
    
    df_2020 = df[df['Year'] == 2020].copy()
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_2020['Month_Str'] = pd.Categorical(df_2020['Month_Str'], categories=month_order, ordered=True)
    
    monthly_crimes = df_2020.groupby(['Month_Str', 'AREA NAME']).size().unstack(fill_value=0)
    
    for area in monthly_crimes.columns:
        sns.lineplot(y=monthly_crimes.index, x=monthly_crimes[area], label=area, marker='o', ax=ax)
    
    ax.set_title("Monthly Crime Trends by Area (2020, Horizontal View)", fontsize=20, weight='bold')
    ax.set_xlabel("Number of Crimes", fontsize=16)
    ax.set_ylabel("Month", fontsize=16)
    ax.legend(title="Area", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14)
    
    plt.tight_layout()
    save_plot(filename, output_dir)
    return fig, ax
