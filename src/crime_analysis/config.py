from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import os


@dataclass
class Config:
    input_file: str = "Crime_Data.csv"
    output_dir: str = "output"
    year_start: int = 2000
    year_end: Optional[int] = None
    lat_bins: int = 4
    lon_bins: int = 4
    show_plots: bool = False
    objectives: List[int] = field(default_factory=lambda: list(range(1, 9)))

    required_columns: List[str] = field(default_factory=lambda: [
        "DR_NO", "Date Rptd", "DATE OCC", "TIME OCC", "AREA", "AREA NAME",
        "Rpt Dist No", "Part 1-2", "Crm Cd", "Crm Cd Desc", "Mocodes",
        "Vict Age", "Vict Sex", "Vict Descent", "Premis Cd", "Premis Desc",
        "Weapon Used Cd", "Weapon Desc", "Status", "Status Desc",
        "Crm Cd 1", "Crm Cd 2", "Crm Cd 3", "LOCATION", "LAT", "LON"
    ])

    crime_short_labels: dict = field(default_factory=lambda: {
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
    })

    def __post_init__(self):
        if self.year_end is None:
            from datetime import datetime
            self.year_end = datetime.now().year

    @property
    def input_path(self) -> Path:
        return Path(self.input_file)

    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)

    def ensure_output_dir(self) -> Path:
        self.output_path.mkdir(parents=True, exist_ok=True)
        return self.output_path

    @classmethod
    def from_args(cls, args) -> "Config":
        return cls(
            input_file=args.input if hasattr(args, 'input') else "Crime_Data.csv",
            output_dir=args.output if hasattr(args, 'output') else "output",
            year_start=args.year_start if hasattr(args, 'year_start') else 2000,
            year_end=args.year_end if hasattr(args, 'year_end') else None,
            lat_bins=args.lat_bins if hasattr(args, 'lat_bins') else 4,
            lon_bins=args.lon_bins if hasattr(args, 'lon_bins') else 4,
            show_plots=args.show if hasattr(args, 'show') else False,
            objectives=args.objectives if hasattr(args, 'objectives') and args.objectives else list(range(1, 9))
        )


def get_default_config() -> Config:
    return Config()
