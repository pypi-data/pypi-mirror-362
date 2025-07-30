import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Apply post-GWAS QC filtering on merged Regenie summary statistics."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to merged Regenie file")
    parser.add_argument("-f", "--filter", required=True, help="Path to QC filter file")
    parser.add_argument("-o", "--output", default="filtered_output.txt", help="Path for filtered file")
    parser.add_argument("--fuma", default="fuma_output.txt", help="Path for FUMA-compatible file")
    parser.add_argument("--format", choices=["filtered", "fuma", "both"], default="both", help="Output format")
    return parser.parse_args()

def main():
    args = parse_arguments()

    print("✅ Loading filter file...")
    filter_df = pd.read_csv(args.filter, sep="\t")
    filter_df["A1_A2"] = filter_df.apply(lambda row: "_".join(sorted([row["Ref"], row["Alt"]])), axis=1)
    filter_df = filter_df[["Name", "A1_A2", "Chr"]]

    print("✅ Loading Regenie file...")
    regenie_df = pd.read_csv(args.input, sep="\t")
    regenie_df["Pos"] = regenie_df["Pos"].astype(int)
    regenie_df["A1_A2"] = regenie_df.apply(lambda row: "_".join(sorted([row["Ref"], row["Alt"]])), axis=1)

    print("✅ Filtering...")
    filtered_df = regenie_df.merge(filter_df, on=["Name", "A1_A2"])
    if "Chr" not in filtered_df.columns:
        filtered_df["Chr"] = filtered_df.get("Chr_x", filtered_df.get("Chr_y", None))
    
    if args.format in ["filtered", "both"]:
        print(f"💾 Saving filtered file to {args.output}")
        filtered_df.to_csv(args.output, sep="\t", index=False)

    if args.format in ["fuma", "both"]:
        if "Info" in filtered_df.columns:
            try:
                info_parts = filtered_df["Info"].str.split("=", n=2, expand=True)
                filtered_df["Pre_Beta"] = info_parts[2]
                beta_split = filtered_df["Pre_Beta"].str.split(";", n=1, expand=True)
                filtered_df["Beta"] = beta_split[0]
                se_split = beta_split[1].str.split(";", n=1, expand=True)
                filtered_df["Se"] = se_split[0]

                fuma_cols = ["Chr", "Pos", "Name", "Ref", "Alt", "Num_Cases", "Num_Controls", "Beta", "Se", "Pval"]
                filtered_df[fuma_cols].to_csv(args.fuma, sep="\t", index=False)
                print(f"💾 FUMA file saved to {args.fuma}")
            except Exception as e:
                print(f"⚠️ Error extracting FUMA columns: {e}")
        else:
            print("⚠️ 'Info' column missing — cannot create FUMA output")

    print("✅ Done.")

