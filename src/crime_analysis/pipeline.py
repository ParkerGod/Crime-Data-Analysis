"""Pipeline module to orchestrate the entire analysis process."""

import os
import sys
from typing import List, Dict, Optional
import pandas as pd

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.crime_analysis.data import get_data
from src.crime_analysis.preprocess import clean_data
from src.crime_analysis.features import create_features
from src.crime_analysis.config import DEFAULT_YEAR_RANGE

def load_analysis_module(objective_id: str):
    """Dynamically load the analysis module for a given objective ID."""
    try:
        module_name = f"analyses.objective_{objective_id.zfill(2)}"
        module = __import__(module_name, fromlist=["run_analysis"])
        return module
    except ImportError:
        raise ValueError(f"Analysis module for objective {objective_id} not found.")

def filter_by_year(df: pd.DataFrame, 
                   year_range: tuple = DEFAULT_YEAR_RANGE) -> pd.DataFrame:
    """Filter DataFrame by year range."""
    if "Year" not in df.columns:
        return df
    
    start_year, end_year = year_range
    return df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

def run_pipeline(input_file: str,
                 output_dir: str,
                 objectives: List[str] = None,
                 year_range: tuple = DEFAULT_YEAR_RANGE,
                 **kwargs) -> Dict[str, Dict]:
    """
    Run the complete analysis pipeline.
    
    Args:
        input_file: Path to input CSV file
        output_dir: Directory to save output files
        objectives: List of objective IDs to run (e.g., ["01", "02"])
                    If None, run all available objectives
        year_range: Tuple of (start_year, end_year) for filtering
        **kwargs: Additional keyword arguments
        
    Returns:
        Dictionary with results for each objective
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Load and validate data
    print(f"Loading data from {input_file}...")
    df = get_data(input_file)
    print(f"Loaded {len(df)} records.")
    
    # Step 2: Clean data
    print("Cleaning data...")
    df_clean = clean_data(df)
    print(f"Cleaned data: {len(df_clean)} records remaining.")
    
    # Step 3: Create features
    print("Creating features...")
    df_features = create_features(df_clean)
    
    # Step 4: Filter by year range
    print(f"Filtering data for years {year_range[0]} to {year_range[1]}...")
    df_filtered = filter_by_year(df_features, year_range)
    print(f"Filtered data: {len(df_filtered)} records remaining.")
    
    # Step 5: Save preprocessed data
    preprocessed_file = os.path.join(output_dir, "preprocessed_data.csv")
    df_filtered.to_csv(preprocessed_file, index=False)
    print(f"Preprocessed data saved to {preprocessed_file}")
    
    # Determine which objectives to run
    if objectives is None:
        # Find all objective files
        analyses_dir = os.path.join(os.path.dirname(__file__), "../..", "analyses")
        objective_files = [f for f in os.listdir(analyses_dir) 
                          if f.startswith("objective_") and f.endswith(".py")]
        objectives = [f.split("_")[1].split(".")[0] for f in objective_files]
        print(f"Found {len(objectives)} objectives to run: {objectives}")
    
    # Step 6: Run each objective
    results = {}
    for obj_id in objectives:
        print(f"\n{'='*60}")
        print(f"Running Objective {obj_id}...")
        print('='*60)
        
        try:
            module = load_analysis_module(obj_id)
            obj_output_dir = os.path.join(output_dir, f"objective_{obj_id}")
            os.makedirs(obj_output_dir, exist_ok=True)
            
            result = module.run_analysis(df_filtered, obj_output_dir)
            results[obj_id] = result
            
            print(f"Objective {obj_id} completed successfully.")
            print(f"Results saved to: {obj_output_dir}")
            
        except Exception as e:
            error_msg = f"Error running Objective {obj_id}: {str(e)}"
            print(error_msg)
            results[obj_id] = {"error": error_msg}
    
    # Step 7: Save summary report
    summary_file = os.path.join(output_dir, "analysis_summary.txt")
    with open(summary_file, "w") as f:
        f.write("Crime Data Analysis Summary\n")
        f.write("="*60 + "\n\n")
        f.write(f"Input File: {input_file}\n")
        f.write(f"Output Directory: {output_dir}\n")
        f.write(f"Year Range: {year_range[0]} to {year_range[1]}\n")
        f.write(f"Total Records Analyzed: {len(df_filtered)}\n")
        f.write(f"Objectives Run: {', '.join(objectives)}\n\n")
        
        for obj_id, result in results.items():
            f.write(f"\nObjective {obj_id} Results:\n")
            f.write("-" * 40 + "\n")
            if "error" in result:
                f.write(f"ERROR: {result['error']}\n")
            else:
                for key, value in result.items():
                    if isinstance(value, dict):
                        f.write(f"{key}:\n")
                        for k, v in value.items():
                            f.write(f"  {k}: {v}\n")
                    else:
                        f.write(f"{key}: {value}\n")
    
    print(f"\n{'='*60}")
    print("Pipeline completed!")
    print(f"Summary saved to: {summary_file}")
    print('='*60)
    
    return results
