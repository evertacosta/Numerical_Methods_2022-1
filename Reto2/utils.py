import pandas as pd


def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['t', 'y1', 'y2'], usecols=[0, 1, 2], index_col=0, skiprows=2)
