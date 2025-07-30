import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2

def plot_qq(df, out_path, lambda_gc):
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
    plt.savefig(out_path)
    plt.close()

def plot_manhattan(df, out_path):
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
        plt.scatter(group["ind"], group["-log10(P)"], color=colors[i], s=2)
        x_labels.append(str(chr_num))
        x_labels_pos.append((group["ind"].iloc[-1] + group["ind"].iloc[0]) / 2)

    plt.axhline(-np.log10(5e-8), color='red', linestyle='--', linewidth=1)
    plt.xticks(x_labels_pos, x_labels)
    plt.xlabel("Chromosome")
    plt.ylabel("-log10(P-value)")
    plt.title("Manhattan Plot")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

