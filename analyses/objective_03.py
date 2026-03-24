from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
from .plotting import create_heatmap, save_figure


def analyze(df: pd.DataFrame, config, output_dir: Path) -> Tuple[Dict[str, Any], Path]:
    lat_min, lat_max = df["LAT"].min(), df["LAT"].max()
    lon_min, lon_max = df["LON"].min(), df["LON"].max()
    lat_bins = np.linspace(lat_min, lat_max, config.lat_bins + 1)
    lon_bins = np.linspace(lon_min, lon_max, config.lon_bins + 1)
    crime_density, _, _ = np.histogram2d(df["LAT"], df["LON"], bins=[lat_bins, lon_bins])
    fig = create_heatmap(
        data=crime_density,
        title="Crime Hotspots (Enhanced Heatmap)",
        xlabel="Longitude",
        ylabel="Latitude",
        extent=(lon_min, lon_max, lat_min, lat_max),
        cmap="Blues"
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = save_figure(fig, "objective_03_hotspots.png", output_dir)
    result = {
        "lat_range": (float(lat_min), float(lat_max)),
        "lon_range": (float(lon_min), float(lon_max)),
        "grid_size": (config.lat_bins, config.lon_bins),
        "max_density_cell": int(np.unravel_index(np.argmax(crime_density), crime_density.shape))
    }
    return result, fig_path
