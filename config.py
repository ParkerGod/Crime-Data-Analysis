from typing import Dict, List, Tuple

DATA_PATH: str = "Crime_Data.csv"
CLEANED_DATA_PATH: str = "crime_data_cleaned.csv"

SEABORN_STYLE: str = "whitegrid"
SEABORN_PALETTE: str = "husl"
FONT_PARAMS: Dict[str, int] = {
    "font.size": 12,
    "axes.titlesize": 16,
    "axes.labelsize": 12
}

CRIME_LABEL_MAPPING: Dict[str, str] = {
    "VEHICLE - STOLEN": "Stolen Vehicle",
    "BATTERY - SIMPLE ASSAULT": "Battery Assault",
    "BURGLARY FROM VEHICLE": "Burglary (Vehicle)",
    "VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)": "Felony Vandalism",
    "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT": "Aggr. Assault w/ Weapon",
    "INTIMATE PARTNER - SIMPLE ASSAULT": "IP Assault",
    "BURGLARY": "Burglary",
    "THEFT PLAIN - PETTY ($950 & UNDER)": "Petty Theft",
    "THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)": "Theft from Vehicle",
    "VANDALISM - MISDEMEANOR ($399 OR UNDER)": "Misdemeanor Vandalism"
}

MONTH_LABELS: List[str] = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

FIGSIZE_STANDARD: Tuple[int, int] = (10, 6)
FIGSIZE_LARGE: Tuple[int, int] = (12, 6)
FIGSIZE_PIE: Tuple[int, int] = (8, 8)
FIGSIZE_TRENDS: Tuple[int, int] = (10, 8)

PALETTE_TOP_CRIMES: str = "cubehelix"
PALETTE_MONTH_TRENDS: str = "crest"
PALETTE_VICTIM_DIST: str = "coolwarm"
PALETTE_WEAPONS: str = "Spectral"
PALETTE_STATUS: str = "Set2"
CMAP_HOTSPOTS: str = "Blues"
COLOR_HIST_AGE: str = "green"

COMPLETION_MESSAGE: str = "-----Analysis Done!-------"
