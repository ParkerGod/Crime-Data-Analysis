from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
from .plotting import create_histogram, save_figure


def analyze(df: pd.DataFrame, config, output_dir: Path) -> Tuple[Dict[str, Any], Path]:
    df_valid = df[(df["Vict Age"] > 0) & (df["Vict Age"] <= 100)]
    fig = create_histogram(
        data=df_valid["Vict Age"],
        bins=20,
        title="Victim Age Distribution",
        xlabel="Age",
        ylabel="Frequency",
        color="green",
        kde=True
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = save_figure(fig, "objective_06_age_histogram.png", output_dir)
    result = {
        "total_valid_victims": len(df_valid),
        "age_statistics": {
            "mean": float(df_valid["Vict Age"].mean()),
            "median": float(df_valid["Vict Age"].median()),
            "std": float(df_valid["Vict Age"].std()),
            "min": int(df_valid["Vict Age"].min()),
            "max": int(df_valid["Vict Age"].max())
        }
    }
    return result, fig_path
