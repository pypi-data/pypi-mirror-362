import pandas as pd

def read_gwas_file(path):
    return pd.read_csv(path, sep="\t")

def save_dataframe(df, path):
    df.to_csv(path, sep="\t", index=False)
