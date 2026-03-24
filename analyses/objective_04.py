from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
from .plotting import create_strip_plot, save_figure


def analyze(df: pd.DataFrame, config, output_dir: Path) -> Tuple[Dict[str, Any], Path]:
    df_valid = df[(df["Vict Age"] > 0) & (df["Vict Age"] <= 100)]
    top5_crimes = df_valid["Crm Cd Desc"].value_counts().head(5).index
    df_top5 = df_valid[df_valid["Crm Cd Desc"].isin(top5_crimes)]
    fig = create_strip_plot(
        data=df_top5,
        x="Crm Cd Desc",
        y="Vict Age",
        hue="Vict Sex",
        title="Victim Age Distribution by Crime Type and Gender",
        xlabel="Crime Type",
        ylabel="Victim Age"
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = save_figure(fig, "objective_04_age_distribution.png", output_dir)
    result = {
        "top_5_crimes": top5_crimes.tolist(),
        "avg_victim_age": float(df_valid["Vict Age"].mean()),
        "median_victim_age": float(df_valid["Vict Age"].median())
    }
    return result, fig_path
