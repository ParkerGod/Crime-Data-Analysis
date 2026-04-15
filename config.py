"""Configuration module for Crime Data Analysis.

This module contains all configuration settings including paths,
visualization styles, labels, and color palettes.
"""

from typing import Dict, List, Tuple

# =============================================================================
# Data Paths
# =============================================================================
DATA_PATH: str = "Crime_Data.csv"
OUTPUT_CSV_PATH: str = "crime_data_cleaned.csv"

# =============================================================================
# Plotting Configuration
# =============================================================================
FIGURE_SIZE_DEFAULT: Tuple[int, int] = (10, 6)
FIGURE_SIZE_LARGE: Tuple[int, int] = (10, 8)
FIGURE_SIZE_PIE: Tuple[int, int] = (8, 8)

# Font sizes
FONT_SIZE_DEFAULT: int = 12
FONT_SIZE_TITLE: int = 20
FONT_SIZE_LABEL: int = 16
FONT_SIZE_TICK: int = 14
FONT_SIZE_TICK_BOLD: int = 14
FONT_SIZE_LEGEND: int = 12
FONT_SIZE_PIE: int = 12
FONT_SIZE_PIE_BOLD: int = 12

# Seaborn style
SEABORN_STYLE: str = "whitegrid"
SEABORN_PALETTE: str = "husl"

# Matplotlib RC parameters
MATPLOTLIB_RCPARAMS: Dict[str, int] = {
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 12
}

# =============================================================================
# Color Palettes
# =============================================================================
PALETTE_TOP_CRIMES: str = "cubehelix"
PALETTE_MONTHLY_TRENDS: str = "crest"
PALETTE_HEATMAP: str = "Blues"
PALETTE_STRIPPLOT: str = "coolwarm"
PALETTE_PIE: str = "Spectral"
PALETTE_HISTOGRAM: str = "green"
PALETTE_STATUS_BAR: str = "Set2"

# =============================================================================
# Crime Labels Mapping
# =============================================================================
CRIME_SHORT_LABELS: Dict[str, str] = {
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

# =============================================================================
# Month Labels
# =============================================================================
MONTH_ORDER: List[str] = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

# =============================================================================
# Data Cleaning Configuration
# =============================================================================
FILLNA_VALUES: Dict[str, str] = {
    "Mocodes": "Null",
    "Vict Sex": "Unknown",
    "Vict Descent": "Unknown",
    "Premis Desc": "Unknown",
    "Weapon Desc": "Unknown",
    "Weapon Used Cd": "N/A",
    "Crm Cd 1": "N/A",
    "Crm Cd 2": "N/A",
    "Crm Cd 3": "N/A"
}

# Age filtering
MIN_VALID_AGE: int = 0
MAX_VALID_AGE: int = 100

# Year filtering
MIN_YEAR: int = 2000

# =============================================================================
# Analysis Configuration
# =============================================================================
TOP_CRIMES_COUNT: int = 10
TOP_WEAPONS_COUNT: int = 5
TOP_CRIMES_FOR_AGE_ANALYSIS: int = 5
HEATMAP_BINS: int = 4
HISTOGRAM_BINS: int = 20
PIE_EXPLODE_VALUE: float = 0.1

# =============================================================================
# Grid and Line Styles
# =============================================================================
GRID_LINE_STYLE: str = "--"
GRID_ALPHA: float = 0.7
HEATMAP_GRID_ALPHA: float = 0.3
HEATMAP_GRID_COLOR: str = "black"
HEATMAP_GRID_LINESTYLE: str = "-"

# =============================================================================
# Output Messages
# =============================================================================
ANALYSIS_COMPLETE_MSG: str = "-----Analysis Done!-------"
