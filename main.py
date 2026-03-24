import argparse
import json
from pathlib import Path
from src.crime_analysis.config import Config
from analyses.pipeline import run_pipeline, run_full_pipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Crime Data Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="Crime_Data.csv",
        help="Input data file path (default: Crime_Data.csv)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output",
        help="Output directory path (default: output)"
    )
    parser.add_argument(
        "--objectives",
        type=int,
        nargs="+",
        choices=range(1, 9),
        help="Specific objectives to run (1-8). If not specified, runs all."
    )
    parser.add_argument(
        "--year-start",
        type=int,
        default=2000,
        help="Start year for filtering (default: 2000)"
    )
    parser.add_argument(
        "--year-end",
        type=int,
        default=None,
        help="End year for filtering (default: current year)"
    )
    parser.add_argument(
        "--lat-bins",
        type=int,
        default=4,
        help="Number of latitude bins for heatmap (default: 4)"
    )
    parser.add_argument(
        "--lon-bins",
        type=int,
        default=4,
        help="Number of longitude bins for heatmap (default: 4)"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show plots interactively (default: save to files)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config = Config(
        input_file=args.input,
        output_dir=args.output,
        year_start=args.year_start,
        year_end=args.year_end,
        lat_bins=args.lat_bins,
        lon_bins=args.lon_bins,
        show_plots=args.show,
        objectives=args.objectives if args.objectives else list(range(1, 9))
    )
    print("=" * 50)
    print("Crime Data Analysis Pipeline")
    print("=" * 50)
    print(f"Input file: {config.input_file}")
    print(f"Output directory: {config.output_dir}")
    print(f"Objectives: {config.objectives}")
    print("=" * 50)
    if args.objectives:
        results = run_pipeline(config, args.objectives)
    else:
        results = run_full_pipeline(config)
    output_dir = config.ensure_output_dir()
    results_file = output_dir / "analysis_results.json"
    serializable_results = {}
    for obj_id, result in results.items():
        if "error" in result:
            serializable_results[str(obj_id)] = result
        else:
            serializable_results[str(obj_id)] = {
                "data": result.get("data", {}),
                "figure_path": result.get("figure_path", "")
            }
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    print("=" * 50)
    print(f"Analysis complete! Results saved to: {results_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()
