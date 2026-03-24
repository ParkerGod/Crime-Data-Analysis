from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
from .plotting import create_bar_plot, save_figure


def analyze(df: pd.DataFrame, config, output_dir: Path) -> Tuple[Dict[str, Any], Path]:
    status_counts = df["Status Desc"].value_counts()
    fig = create_bar_plot(
        data=status_counts,
        title="Distribution of Crimes by Status Description",
        xlabel="Status",
        ylabel="Number of Crimes",
        horizontal=False,
        palette="Set2"
    )
    fig.axes[0].tick_params(axis="x", rotation=0)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = save_figure(fig, "objective_07_status_distribution.png", output_dir)
    result = {
        "status_distribution": status_counts.to_dict(),
        "total_crimes": int(status_counts.sum())
    }
    return result, fig_path
