from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
from .plotting import create_bar_plot, save_figure


def analyze(df: pd.DataFrame, config, output_dir: Path) -> Tuple[Dict[str, Any], Path]:
    if "Month" not in df.columns:
        raise ValueError("Month column not found. Please run feature extraction first.")
    crime_trends_by_month = df.groupby("Month").size()
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig = create_bar_plot(
        data=crime_trends_by_month,
        title="Average Crime Trends by Month",
        xlabel="Month",
        ylabel="Number of Crimes",
        horizontal=False,
        palette="crest"
    )
    fig.axes[0].set_xticks(np.arange(12))
    fig.axes[0].set_xticklabels(month_labels, fontsize=14)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = save_figure(fig, "objective_02_monthly_trends.png", output_dir)
    result = {
        "monthly_crime_counts": crime_trends_by_month.to_dict(),
        "peak_month": int(crime_trends_by_month.idxmax()),
        "lowest_month": int(crime_trends_by_month.idxmin())
    }
    return result, fig_path
