"""Configuration settings for crime analysis project."""

# File paths
DEFAULT_INPUT_FILE = "Crime_Data.csv"
DEFAULT_OUTPUT_DIR = "output"

# Analysis settings
DEFAULT_YEAR_RANGE = (2020, 2023)
DEFAULT_GRID_SIZE = 10  # Number of grid cells for spatial analysis
DEFAULT_SHOW_PLOTS = False  # Whether to display plots interactively

# Required columns in input data
REQUIRED_COLUMNS = [
    "DATE OCC",
    "TIME OCC",
    "AREA NAME",
    "Crm Cd Desc",
    "Vict Age",
    "Vict Sex",
    "LOCATION",
    "LAT",
    "LON"
]

# Feature engineering settings
DATE_FORMATS = [
    "%m/%d/%Y %I:%M:%S %p",
    "%m/%d/%Y",
    "%Y-%m-%d %H:%M:%S"
]
