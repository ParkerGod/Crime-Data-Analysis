from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH: str = "Crime_Data.csv"
OUTPUT_PATH: str = "crime_data_cleaned.csv"

FILLNA_COLUMNS: Dict[str, str] = {
    "Mocodes": "Null",
    "Vict Sex": "Unknown",
    "Vict Descent": "Unknown",
    "Premis Desc": "Unknown",
    "Weapon Desc": "Unknown",
    "Weapon Used Cd": "N/A",
    "Crm Cd 1": "N/A",
    "Crm Cd 2": "N/A",
    "Crm Cd 3": "N/A",
}

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

MONTH_LABELS: List[str] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

MONTH_ORDER: List[str] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

YEAR_FILTER_START: int = 2000

VALID_AGE_MIN: int = 0
VALID_AGE_MAX: int = 100
TOP_CRIMES_COUNT: int = 10
TOP5_CRIMES_COUNT: int = 5
TOP_WEAPONS_COUNT: int = 5
GRID_BINS: int = 4
HISTOGRAM_BINS: int = 20
TARGET_YEAR: int = 2020

TITLE_TOP_CRIMES: str = "Top 10 Crime Categories"
TITLE_MONTHLY_TRENDS: str = "Average Crime Trends by Month"
TITLE_HOTSPOTS: str = "Crime Hotspots (Enhanced Heatmap)"
TITLE_AGE_BY_CRIME: str = "Victim Age Distribution by Crime Type and Gender"
TITLE_WEAPONS: str = "Top 5 Weapons Used in Crimes"
TITLE_AGE_DIST: str = "Victim Age Distribution"
TITLE_STATUS: str = "Distribution of Crimes by Status Description"
TITLE_AREA_TRENDS: str = "Monthly Crime Trends by Area (2020, Horizontal View)"

XLABEL_CRIMES: str = "Number of Crimes"
XLABEL_MONTH: str = "Month"
XLABEL_LONGITUDE: str = "Longitude"
XLABEL_CRIME_TYPE: str = "Crime Type"
XLABEL_AGE: str = "Age"
XLABEL_STATUS: str = "Status"
YLABEL_CRIME_TYPE: str = "Crime Type"
YLABEL_CRIMES: str = "Number of Crimes"
YLABEL_LATITUDE: str = "Latitude"
YLABEL_VICTIM_AGE: str = "Victim Age"
YLABEL_FREQUENCY: str = "Frequency"
YLABEL_MONTH: str = "Month"

PALETTE_TOP_CRIMES: str = "cubehelix"
PALETTE_MONTHLY: str = "crest"
PALETTE_AGE_GENDER: str = "coolwarm"
PALETTE_WEAPONS: str = "Spectral"
PALETTE_STATUS: str = "Set2"
CMAP_HOTSPOTS: str = "Blues"
COLOR_HISTOGRAM: str = "green"

FONT_SIZE_TITLE: int = 20
FONT_SIZE_LABEL: int = 16
FONT_SIZE_TICKS: int = 14
FONT_SIZE_LEGEND: int = 14
FONT_SIZE_PIE_PCT: int = 12

FIG_SIZE_WIDE: tuple = (10, 6)
FIG_SIZE_MEDIUM: tuple = (12, 6)
FIG_SIZE_SQUARE: tuple = (8, 8)
FIG_SIZE_LARGE: tuple = (10, 8)

PIE_EXPLODE: tuple = (0.1, 0.1, 0.1, 0.1, 0.1)
PIE_START_ANGLE: int = 120
PIE_PCT_DISTANCE: float = 0.85

BAR_WIDTH_NARROW: float = 0.5
BAR_WIDTH_NORMAL: float = 0.7

STRIP_ALPHA: float = 0.7
GRID_ALPHA: float = 0.7
GRID_ALPHA_LIGHT: float = 0.3

MARKER_STYLE: str = 'o'

def setup_plot_style() -> None:
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 16,
        'axes.labelsize': 12
    })
