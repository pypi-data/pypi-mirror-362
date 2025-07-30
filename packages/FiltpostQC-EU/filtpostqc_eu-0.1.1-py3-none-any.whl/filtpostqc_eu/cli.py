#!/usr/bin/env python3

import argparse
import pandas as pd
from importlib.metadata import version as get_version

def parse_arguments():
    """
    Parse command-line arguments for post-GWAS QC filtering.
    """
    parser = argparse.ArgumentParser(
        description="Apply post-GWAS QC filtering on merged Regenie summary statistics using a variant QC filter."
    )
    parser.add_argument(
        "-i", "--input", required=False,
        help="Path to the merged Regenie summary statistics file."
    )
    parser.add_argument(
        "-f", "--filter", required=False,
        help="Path to the QC variant filter file (e.g., EUR_QC_filter_regenie.tsv)."
    )
    parser.add_argument(
        "-o", "--output", default="filtered_output.txt",
        help="Output file for the filtered result (default: filtered_output.txt)."
    )
    parser.add_argument(
        "--fuma", default="fuma_output.txt",
        help="Output file in FUMA-compatible format (default: fuma_output.txt)."
    )
    parser.add_argument(
        "--format", choices=["filtered", "fuma", "both"], default="both",
        help="Choose output format: filtered, fuma, or both (default: both)."
    )
    parser.add_argument("--version", action="version", version="FiltpostQC-EU v0.1.1")
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    if not args.input or not args.filter:
        print("❌ Error: --input and --filter are required unless --version is used.\n")
        print("📘 Use --help to see usage.")
        return

    print("✅ Loading QC filter file...")
    filter_df = pd.read_csv(args.filter, sep="\t")
    filter_df["A1_A2"] = filter_df.apply(lambda row: "_".join(sorted([row["Ref"], row["Alt"]])), axis=1)
    filter_df = filter_df[["Name", "A1_A2", "Chr"]]

    print("✅ Loading Regenie merged summary statistics...")
    regenie_df = pd.read_csv(args.input, sep="\t")
    regenie_df["Pos"] = regenie_df["Pos"].astype(int)
    regenie_df["A1_A2"] = regenie_df.apply(lambda row: "_".join(sorted([row["Ref"], row["Alt"]])), axis=1)

    print("✅ Applying post-GWAS QC filtering...")
    filtered_df = regenie_df.merge(filter_df, on=["Name", "A1_A2"])
    if "Chr" not in filtered_df.columns:
        filtered_df["Chr"] = filtered_df.get("Chr_x", filtered_df.get("Chr_y", None))

    if args.format in ["filtered", "both"]:
        print(f"💾 Saving filtered file to: {args.output}")
        filtered_df.to_csv(args.output, sep="\t", index=False)

    if args.format in ["fuma", "both"]:
        if "Info" in filtered_df.columns:
            try:
                print("✅ Parsing 'Info' column to extract Beta and SE for FUMA...")
                info_parts = filtered_df["Info"].str.split("=", n=2, expand=True)
                filtered_df["Pre_Beta"] = info_parts[2]
                beta_split = filtered_df["Pre_Beta"].str.split(";", n=1, expand=True)
                filtered_df["Beta"] = beta_split[0]
                se_split = beta_split[1].str.split(";", n=1, expand=True)
                filtered_df["Se"] = se_split[0]

                fuma_cols = ["Chr", "Pos", "Name", "Ref", "Alt", "Num_Cases", "Num_Controls", "Beta", "Se", "Pval"]
                filtered_df[fuma_cols].to_csv(args.fuma, sep="\t", index=False)
                print(f"💾 FUMA-compatible file saved to: {args.fuma}")
            except Exception as e:
                print(f"⚠️ Failed to extract FUMA fields: {e}")
        else:
            print("⚠️ Column 'Info' not found in input file — skipping FUMA output.")

    print("✅ Post-QC completed successfully.")

