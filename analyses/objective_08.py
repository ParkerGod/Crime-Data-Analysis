from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
from .plotting import create_line_plot, save_figure


def analyze(df: pd.DataFrame, config, output_dir: Path) -> Tuple[Dict[str, Any], Path]:
    if "Year" not in df.columns or "MonthName" not in df.columns:
        raise ValueError("Year/MonthName columns not found. Please run feature extraction first.")
    df_2020 = df[df["Year"] == 2020].copy()
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_2020["MonthName"] = pd.Categorical(df_2020["MonthName"], categories=month_order, ordered=True)
    monthly_crimes = df_2020.groupby(["MonthName", "AREA NAME"]).size().unstack(fill_value=0)
    fig = create_line_plot(
        data=monthly_crimes,
        title="Monthly Crime Trends by Area (2020, Horizontal View)",
        xlabel="Number of Crimes",
        ylabel="Month",
        hue="Area"
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = save_figure(fig, "objective_08_monthly_by_area.png", output_dir)
    result = {
        "year": 2020,
        "areas": monthly_crimes.columns.tolist(),
        "total_crimes_2020": int(monthly_crimes.sum().sum())
    }
    return result, fig_path
