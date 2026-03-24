from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
from .plotting import create_pie_chart, save_figure


def analyze(df: pd.DataFrame, config, output_dir: Path) -> Tuple[Dict[str, Any], Path]:
    weapon_counts = df["Weapon Desc"].value_counts().head(5)
    fig = create_pie_chart(
        data=weapon_counts,
        title="Top 5 Weapons Used in Crimes",
        explode=(0.1, 0.1, 0.1, 0.1, 0.1),
        palette="Spectral"
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = save_figure(fig, "objective_05_weapons.png", output_dir)
    result = {
        "top_5_weapons": weapon_counts.to_dict(),
        "total_weapon_incidents": int(weapon_counts.sum())
    }
    return result, fig_path
