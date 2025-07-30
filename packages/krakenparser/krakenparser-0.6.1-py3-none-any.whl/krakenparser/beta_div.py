#!/usr/bin/env python

import pandas as pd
import numpy as np
import sys
import shutil
import argparse
from pathlib import Path
from skbio.diversity import beta_diversity
from skbio.stats.subsample import subsample_counts


def calc_beta_div(source_file, output_prefix, rarefaction_depth=1000):
    df = pd.read_csv(source_file, index_col=0)

    # Rarefy samples
    rarefied_counts = []
    sample_ids = []

    for sample, row in df.iterrows():
        counts = row.values.astype(int)
        if counts.sum() >= rarefaction_depth:
            rarefied = subsample_counts(counts, n=rarefaction_depth)
            rarefied_counts.append(rarefied)
            sample_ids.append(sample)

    if len(rarefied_counts) < 2:
        raise ValueError("Not enough samples passed the rarefaction threshold.")

    # Compute Bray-Curtis and Jaccard
    bray_dm = beta_diversity("braycurtis", rarefied_counts, ids=sample_ids)
    jaccard_dm = beta_diversity("jaccard", rarefied_counts, ids=sample_ids)

    # Save to CSV
    bray_df = bray_dm.to_data_frame()
    jaccard_df = jaccard_dm.to_data_frame()

    bray_df.to_csv(f"{output_prefix}_braycurtis.csv")
    jaccard_df.to_csv(f"{output_prefix}_jaccard.csv")

    # Clean up __pycache__
    current_dir = Path(__file__).resolve().parent
    pycache_dir = current_dir / "__pycache__"
    if pycache_dir.exists() and pycache_dir.is_dir():
        shutil.rmtree(pycache_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate β-diversity (Bray-Curtis and Jaccard) with rarefaction."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Input CSV count table (samples as rows)."
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Output prefix for distance matrices."
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=1000,
        help="Rarefaction depth (default: 1000).",
    )
    args = parser.parse_args()

    calc_beta_div(args.input, args.output, args.depth)
