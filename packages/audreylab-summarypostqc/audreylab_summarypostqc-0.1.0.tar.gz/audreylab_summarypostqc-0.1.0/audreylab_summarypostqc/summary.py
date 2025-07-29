import pandas as pd
from .utils import read_gwas_file

def summarize_gwas(path, pval_threshold=5e-8):
    df = read_gwas_file(path)
    n_total = len(df)
    n_signif = (df["Pval"] < pval_threshold).sum()
    return {
        "Total variants": n_total,
        f"Variants with P < {pval_threshold}": n_signif
    }
