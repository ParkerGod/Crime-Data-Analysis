from pathlib import Path
from typing import Dict, Any, List, Callable, Tuple
import importlib
import pandas as pd
from src.crime_analysis.config import Config
from src.crime_analysis.data import load_crime_data
from src.crime_analysis.preprocess import clean_crime_data
from src.crime_analysis.features import extract_date_features
from .plotting import setup_plotting_style


OBJECTIVE_MODULES = {
    1: "analyses.objective_01",
    2: "analyses.objective_02",
    3: "analyses.objective_03",
    4: "analyses.objective_04",
    5: "analyses.objective_05",
    6: "analyses.objective_06",
    7: "analyses.objective_07",
    8: "analyses.objective_08"
}


def get_objective_function(objective_id: int) -> Callable:
    if objective_id not in OBJECTIVE_MODULES:
        raise ValueError(f"Unknown objective ID: {objective_id}")
    module_name = OBJECTIVE_MODULES[objective_id]
    module = importlib.import_module(module_name)
    return module.analyze


def run_single_objective(
    df: pd.DataFrame,
    objective_id: int,
    config: Config,
    output_dir: Path
) -> Tuple[Dict[str, Any], Path]:
    analyze_func = get_objective_function(objective_id)
    return analyze_func(df, config, output_dir)


def run_pipeline(
    config: Config,
    objectives: List[int] = None
) -> Dict[int, Dict[str, Any]]:
    setup_plotting_style()
    df = load_crime_data(config)
    df = clean_crime_data(df)
    df = extract_date_features(df)
    output_dir = config.ensure_output_dir()
    if objectives is None:
        objectives = config.objectives
    results = {}
    for obj_id in objectives:
        if obj_id not in OBJECTIVE_MODULES:
            print(f"Skipping unknown objective: {obj_id}")
            continue
        print(f"Running objective {obj_id}...")
        try:
            result, fig_path = run_single_objective(df, obj_id, config, output_dir)
            results[obj_id] = {
                "data": result,
                "figure_path": str(fig_path)
            }
            print(f"  Completed: {fig_path}")
        except Exception as e:
            print(f"  Error: {e}")
            results[obj_id] = {"error": str(e)}
    return results


def run_full_pipeline(config: Config) -> Dict[int, Dict[str, Any]]:
    return run_pipeline(config, objectives=list(OBJECTIVE_MODULES.keys()))
