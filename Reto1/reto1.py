import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
import scipy

matplotlib.use('TkAgg')

# comentario hecho desde github

"""
- Lectura de datos adf
Realizar los siguientes calculos
- Frecuencia
- Valor Pico
- Valor DC
- Valor AC
- Componentes armonicas
- Desface respecto a onda de referencia
- Otros metodos complementarios
"""


def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['t', 'y'], usecols=[0, 1], skiprows=2)


def read_csv(file):
    return pd.read_csv(file, sep=';', names=['t', 'y'])


def simple_plot(x, y, file_name):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(file_name)


if __name__ == "__main__":

    data_url = 'https://raw.githubusercontent.com/evertacosta/Numerical_Methods_2022-1/main/Reto1/data/'

    # csv files list with their names
    csv_files_list_names = ['Paula1_WV_01.csv', 'Paula1_WV_02.csv', 'Paula1_WV_03.csv', 'Paula1_WV_04.csv']

    # adf files list with their names
    adf_files_list_names = ['PAula1_WV_03.adf', 'PAula1_WV_03v.adf', 'PAula1_WV_04.adf',
                            'PAula1_WV_04v.adf']

    dfs_from_csv = []
    dfs_from_adf = []

    for file in csv_files_list_names:
        if file == 'Paula1_WV_03.csv':
            data = pd.read_csv('./data/Paula1_WV_03.csv', sep=';', names=['t', 'y'])
            data['y'] = data['y'].apply(lambda x: float(x.strip('[]')))
            dfs_from_csv.append(data)
        else:
            data = read_csv(data_url+file)
            dfs_from_csv.append(data)

    for file in adf_files_list_names:
        data = read_adf(data_url+file)
        dfs_from_adf.append(data)


    df0 = dfs_from_csv[0]
    df1 = dfs_from_csv[1]
    df2 = dfs_from_csv[2]
    df3 = dfs_from_csv[3]
    simple_plot(df0.t, df0.y, 'csv grafico 1')
    simple_plot(df1.t, df1.y, 'csv grafico 2')
    simple_plot(df2.t, df2.y, 'csv grafico 3')
    simple_plot(df3.t, df3.y, 'csv grafico 4')

    df0a = dfs_from_adf[0]
    df1a = dfs_from_adf[1]
    df2a = dfs_from_adf[2]
    df3a = dfs_from_adf[3]
    simple_plot(df0a.t, df0a.y, 'adf grafico 0')
    simple_plot(df1a.t, df1a.y, 'adf grafico 1')
    simple_plot(df2a.t, df2a.y, 'adf grafico 2')
    simple_plot(df3a.t, df3a.y, 'adf grafico 3')

