#!/usr/bin/env python
"""Main entry point for crime data analysis pipeline."""

import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.crime_analysis.pipeline import run_pipeline
from src.crime_analysis.config import (
    DEFAULT_INPUT_FILE,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_YEAR_RANGE
)

def main():
    """Main function to parse command line arguments and run pipeline."""
    parser = argparse.ArgumentParser(description="Crime Data Analysis Pipeline")
    
    # Input/output arguments
    parser.add_argument(
        "--input", "-i",
        default=DEFAULT_INPUT_FILE,
        help=f"Path to input CSV file (default: {DEFAULT_INPUT_FILE})"
    )
    
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save output files (default: {DEFAULT_OUTPUT_DIR})"
    )
    
    # Objective selection
    parser.add_argument(
        "--objectives", "-obj",
        nargs="+",
        help="List of objective IDs to run (e.g., --objectives 01 02). "
             "If not specified, all available objectives will be run."
    )
    
    # Year range
    parser.add_argument(
        "--start-year", "-s",
        type=int,
        default=DEFAULT_YEAR_RANGE[0],
        help=f"Start year for analysis (default: {DEFAULT_YEAR_RANGE[0]})"
    )
    
    parser.add_argument(
        "--end-year", "-e",
        type=int,
        default=DEFAULT_YEAR_RANGE[1],
        help=f"End year for analysis (default: {DEFAULT_YEAR_RANGE[1]})"
    )
    
    # List available objectives
    parser.add_argument(
        "--list-objectives", "-l",
        action="store_true",
        help="List all available objectives and exit"
    )
    
    args = parser.parse_args()
    
    # Handle --list-objectives flag
    if args.list_objectives:
        print("Available Objectives:")
        print("-" * 40)
        print("01: Basic crime trend analysis")
        print("02: Spatial analysis and victim demographics")
        print("03: Crime distribution by day of week and month")
        print("04: Crime type distribution analysis")
        print("05: Victim gender analysis by crime type")
        print("06: Hourly and daily crime heatmap analysis")
        print("07: Quarterly crime trend analysis")
        print("08: Combined comprehensive analysis summary")
        print("\nTo run specific objectives: python main.py --objectives 01 02")
        print("To run all objectives: python main.py")
        sys.exit(0)
    
    # Validate year range
    if args.start_year > args.end_year:
        print(f"Error: Start year ({args.start_year}) cannot be greater than end year ({args.end_year})")
        sys.exit(1)
    
    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        print("Please specify a valid input file using --input or -i flag.")
        sys.exit(1)
    
    # Print configuration
    print("=" * 60)
    print("Crime Data Analysis Pipeline Configuration")
    print("=" * 60)
    print(f"Input File: {args.input}")
    print(f"Output Directory: {args.output}")
    print(f"Year Range: {args.start_year} to {args.end_year}")
    if args.objectives:
        print(f"Objectives to Run: {', '.join(args.objectives)}")
    else:
        print("Objectives to Run: All available")
    print("=" * 60)
    print()
    
    try:
        results = run_pipeline(
            input_file=args.input,
            output_dir=args.output,
            objectives=args.objectives,
            year_range=(args.start_year, args.end_year)
        )
        
        # Print summary
        print("\n" + "=" * 60)
        print("Final Summary")
        print("=" * 60)
        
        success_count = sum(1 for r in results.values() if "error" not in r)
        error_count = sum(1 for r in results.values() if "error" in r)
        
        print(f"Total objectives run: {len(results)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {error_count}")
        
        if error_count > 0:
            print("\nFailed objectives:")
            for obj_id, result in results.items():
                if "error" in result:
                    print(f"  - Objective {obj_id}: {result['error']}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\nPipeline failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
