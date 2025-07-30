#!/usr/bin/env python

import shutil
from pathlib import Path
import argparse
import pandas as pd


def convert_to_csv(input_file, output_file):
    # Read the entire file into a DataFrame
    data = pd.read_csv(input_file, sep="\t", header=None)

    # Set the first row as the header
    data.columns = data.iloc[0]
    data = data.drop(data.index[0])

    # Transpose the DataFrame so that sample names become rows and microbial taxa with their abundance become columns
    data_transposed = data.T
    data_transposed.columns = data_transposed.iloc[0]
    data_transposed = data_transposed.drop(data_transposed.index[0])

    # Save the transposed data to a new CSV file
    data_transposed.to_csv(output_file, index_label="Sample_id")
    print(f"Data has been successfully converted and saved as '{output_file}'.")

    # Remove pycache if it exists
    current_dir = Path(__file__).resolve().parent
    pycache_dir = current_dir / "__pycache__"
    if pycache_dir.exists() and pycache_dir.is_dir():
        shutil.rmtree(pycache_dir)


if __name__ == "__main__":
    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Reads a TXT file, reorganizes the data, and converts it into a CSV file."
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to the input TXT file. This file should contain sample names in columns and microbial taxa in rows.",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path to the output CSV file. The script will restructure the data and save it here.",
    )

    args = parser.parse_args()

    # Call function with parsed arguments
    convert_to_csv(args.input, args.output)
