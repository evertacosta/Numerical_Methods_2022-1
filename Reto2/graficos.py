import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

matplotlib.use('TkAgg')


def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['t', 'y1', 'y2'], usecols=[0, 1, 2], index_col='t', skiprows=2)


p1 = read_adf('./datos/Problema1_MN20221_WV_P2.adf')
p2 = read_adf('./datos/Problema2_MN20221_WV_P2.adf')
p3 = read_adf('./datos/Problema3_MN20221_WV_P2.adf')


def simple_plot(p, title, ylabel1, ylabel2):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)

    fig.suptitle(title)
    ax1.plot(p.index, p.y1)
    #ax1.set_xlabel('aja')
    ax1.set_ylabel(ylabel1)
    ax1.grid()

    ax2.plot(p.index, p.y2)
    ax2.set_xlabel('Tiempo [s]')
    ax2.set_ylabel(ylabel2)
    ax2.grid()


simple_plot(p1, 'Respuesta Circuito RL', 'Voltaje [V]', 'Corriente [A]')
simple_plot(p2, 'Respuesta Circuito RLC', 'Voltaje [V]', 'Corriente [A]')
simple_plot(p3, 'Respuesta Circuito RC', 'Voltaje [V]', 'Corriente [A]')
