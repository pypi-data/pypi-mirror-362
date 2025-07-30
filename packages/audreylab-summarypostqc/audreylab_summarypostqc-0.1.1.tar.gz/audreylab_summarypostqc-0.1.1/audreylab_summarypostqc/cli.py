#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Plot QQ and/or Manhattan plots from GWAS results.")
    parser.add_argument("--input", required=True, help="Path to the GWAS QC merged file (.txt)")
    parser.add_argument("--qqplot", help="Output path for QQ plot image (default: <out>_qqplot.png)")
    parser.add_argument("--manhattan", help="Output path for Manhattan plot image (default: <out>_manhattan.png)")
    parser.add_argument("--out", help="Prefix for output files if --qqplot or --manhattan are not provided")

    args = parser.parse_args()

    # === Gestion des noms de fichiers de sortie ===
    if not args.qqplot and not args.manhattan and not args.out:
        parser.error("You must specify --qqplot, --manhattan, or a common --out prefix.")

    if not args.qqplot and args.out:
        args.qqplot = f"{args.out}_qqplot.png"

    if not args.manhattan and args.out:
        args.manhattan = f"{args.out}_manhattan.png"

    # === Chargement des résultats GWAS ===
    df = pd.read_csv(args.input, sep="\t")

    # Filtrage des P-values valides
    df = df[df["Pval"].notnull()]
    df["Pval"] = pd.to_numeric(df["Pval"], errors="coerce")
    df = df[df["Pval"] > 0]

    # Calcul du lambda GC
    df["chi2"] = chi2.isf(df["Pval"], df=1)
    lambda_gc = np.median(df["chi2"]) / chi2.ppf(0.5, 1)

    # === QQ plot ===
    if args.qqplot:
        observed = -np.log10(np.sort(df["Pval"]))
        expected = -np.log10(np.linspace(1 / len(observed), 1, len(observed)))

        plt.figure(figsize=(6, 6))
        plt.plot(expected, observed, 'o', markersize=2, label="Observed P-values")
        plt.plot([0, max(expected)], [0, max(expected)], 'r--', label="Expected")
        plt.xlabel("Expected -log10(P)")
        plt.ylabel("Observed -log10(P)")
        plt.title(f"QQ Plot (λGC = {lambda_gc:.3f})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(args.qqplot)
        plt.close()
        print(f"✅ QQ plot saved to {args.qqplot}")

    # === Manhattan plot ===
    if args.manhattan:
        df = df[df["Chr"].apply(lambda x: str(x).isdigit())]
        df["Chr"] = df["Chr"].astype(int)
        df = df.sort_values(["Chr", "Pos"])
        df["-log10(P)"] = -np.log10(df["Pval"])
        df["ind"] = range(len(df))

        df_grouped = df.groupby("Chr")
        colors = sns.color_palette("husl", n_colors=len(df_grouped))

        plt.figure(figsize=(12, 6))
        x_labels = []
        x_labels_pos = []

        for i, (chr_num, group) in enumerate(df_grouped):
            plt.scatter(group["ind"], group["-log10(P)"], color=colors[i], s=2, label=f"Chr {chr_num}")
            x_labels.append(str(chr_num))
            x_labels_pos.append((group["ind"].iloc[-1] + group["ind"].iloc[0]) / 2)

        plt.axhline(-np.log10(5e-8), color='red', linestyle='--', linewidth=1)
        plt.xticks(x_labels_pos, x_labels)
        plt.xlabel("Chromosome")
        plt.ylabel("-log10(P-value)")
        plt.title("Manhattan Plot")
        plt.tight_layout()
        plt.savefig(args.manhattan)
        plt.close()
        print(f"✅ Manhattan plot saved to {args.manhattan}")

    print(f"λGC (Lambda GC): {lambda_gc:.3f}")

if __name__ == "__main__":
    main()

