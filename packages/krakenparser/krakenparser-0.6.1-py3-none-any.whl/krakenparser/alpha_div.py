#!/usr/bin/env python

import pandas as pd
import numpy as np
import sys
import shutil
import argparse
from pathlib import Path


# Define Shannon index
def shannon_index(counts):
    counts = np.array(counts)
    counts = counts[counts > 0]
    proportions = counts / counts.sum()
    return -np.sum(proportions * np.log(proportions))


# Define Pielou's evenness
def pielou_evenness(counts):
    counts = np.array(counts)
    counts = counts[counts > 0]
    H = shannon_index(counts)
    S = len(counts)
    return H / np.log(S) if S > 1 else 0


# Define Chao1 richness estimator
def chao1_index(counts):
    counts = np.array(counts)
    S_obs = np.sum(counts > 0)
    F1 = np.sum(counts == 1)
    F2 = np.sum(counts == 2)
    if F2 == 0:
        return S_obs + F1 * (F1 - 1) / 2
    return S_obs + (F1 * F1) / (2 * F2)


def calc_alpha_div(source_file, destination_file):
    df = pd.read_csv(source_file, index_col=0)

    results = []
    for sample_id, row in df.iterrows():
        counts = row.values
        results.append(
            {
                "Sample": sample_id,
                "Shannon": shannon_index(counts),
                "Pielou": pielou_evenness(counts),
                "Chao1": chao1_index(counts),
            }
        )

    alpha_div_df = pd.DataFrame(results).set_index("Sample")
    alpha_div_df.to_csv(destination_file)

    # Get the path to the current directory (same location as the script)
    current_dir = Path(__file__).resolve().parent
    pycache_dir = current_dir / "__pycache__"

    # Check if __pycache__ exists and remove it
    if pycache_dir.exists() and pycache_dir.is_dir():
        shutil.rmtree(pycache_dir)


if __name__ == "__main__":
    # Use argparse to parse command-line arguments
    parser = argparse.ArgumentParser(description="Calculates α-diversity per sample.")
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to the source file (total abundance on species level).",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path to the destination file.",
    )

    args = parser.parse_args()

    # Call the function with parsed arguments
    calc_alpha_div(args.input, args.output)
