import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')


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

aja = ['Paula1_WV_01.csv', 'Paula1_WV_02.csv', 'Paula1_WV_03.csv', 'Paula1_WV_04.csv']


def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['a', 'b'], usecols=[0, 1], skiprows=2)


def read_csv(file):
    return pd.read_csv(file, sep=';', names=['a', 'b'])


def simple_plot(x, y, file_name):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(file_name)


if __name__ == "__main__":
    file1 = './data/PAula1_WV_03.adf'
    file2 = './data/PAula1_WV_03v.adf'
    file3 = './data/PAula1_WV_04.adf'
    file4 = './data/PAula1_WV_04v.adf'

    a = read_adf(file1)
    b = read_adf(file2)
    c = read_adf(file3)
    d = read_adf(file4)
    simple_plot(a.a, a.b, file1)
    simple_plot(b.a, b.b, file2)
    simple_plot(c.a, c.b, file3)
    simple_plot(d.a, d.b, file4)

    main_path = './data/'

    for i in aja:
        if i == 'Paula1_WV_03.csv':
            dfe = pd.read_csv('./data/Paula1_WV_03.csv', sep=';', names=['x', 'y'])
            dfe['y'] = dfe['y'].apply(lambda x: float(x.strip('[]')))
            simple_plot(dfe.x, dfe.y, i)
        else:
            df = read_csv(main_path+i)
            simple_plot(df.a, df.b, i)
