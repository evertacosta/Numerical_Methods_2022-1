import pandas as pd
import matplotlib.pyplot as plt

def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['t', 'y'], usecols=[0, 1], skiprows=2)


def read_csv(file):
    return pd.read_csv(file, sep=';', names=['t', 'y'])

def simple_plot(x, y, file_name):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(file_name)
