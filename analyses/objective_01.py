from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
from .plotting import create_bar_plot, save_figure


def analyze(df: pd.DataFrame, config, output_dir: Path) -> Tuple[Dict[str, Any], Path]:
    crime_counts = df["Crm Cd Desc"].value_counts()
    top_crimes = crime_counts.head(10)
    top_crimes.index = top_crimes.index.map(
        lambda x: config.crime_short_labels.get(x, x)
    )
    fig = create_bar_plot(
        data=top_crimes,
        title="Top 10 Crime Categories",
        xlabel="Number of Crimes",
        ylabel="Crime Type",
        horizontal=True,
        palette="cubehelix"
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = save_figure(fig, "objective_01_top_10_crimes.png", output_dir)
    result = {
        "top_10_crimes": top_crimes.to_dict(),
        "total_crimes_analyzed": len(df)
    }
    return result, fig_path
