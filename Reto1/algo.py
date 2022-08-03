from utils import read_adf, read_csv, simple_plot
import numpy as np
import pandas as pd


def get_signo(numero, promedio):
    if numero > promedio:
        return True
    else:
        return False


def inverse_signo(signo):
    if signo:
        return False
    else:
        return True


def segmentos(y):
    """

    :param y: ndarray de numpy
    :return:
    """

    contador = 0

    s = []

    signo = get_signo(y[0], y.mean())

    for valor in y:
        if get_signo(valor, y.mean()) != signo:
            signo = inverse_signo(signo)
            if contador == len(y)-1:
                pass
            else:
                s.append(contador)

        contador += 1

    s.append(len(y)-1)

    return s


def max_by_seg(t, y):
    """

    :param t: ndarray de numpy
    :param y: ndarray de numpy
    :return:
    """

    last_index = 0
    puntos = []

    s = segmentos(y)

    for punto in s:
        # print('segmento', last_index, punto)
        grupo = y[last_index:punto]
        grupo_t = t[last_index:punto]

        signo = get_signo(grupo[last_index], y.mean())
        # print('signo', signo)
        if signo:
            # print(grupo_t[last_index+grupo.argmax()], grupo.max())
            puntos.append((grupo_t[last_index+grupo.argmax()], grupo.max()))
        else:
            # print(grupo_t[last_index+grupo.argmin()], grupo.min())
            puntos.append((grupo_t[last_index + grupo.argmin()], grupo.min()))

        last_index = punto

    return puntos


def periodo(t, y):
    """

    :param t: lista de python
    :param y: lista de python
    :return:
    """
    puntos = max_by_seg(t, y)
    periodo = puntos[3][0] - puntos[1][0]

    return periodo


def frecuencia(t, y):
    """

    :param t: lista de python
    :param y: lista de python
    :return:
    """
    return 1/periodo(t, y)


def voltaje_pico(t, y):
    """

    :param t:
    :param y:
    :return:
    """
    puntos = max_by_seg(t, y)

    for punto in puntos[1:]:
        if get_signo(punto[1], y.mean()):
            return punto[1]-y.mean()



if __name__ == "__main__":
    #df = read_adf('./data/PAula1_WV_04v.adf')
    #df = read_csv('./data/Paula1_WV_04.csv')
    #df = read_csv('./data/Paula1_WV_01.csv')
    df = read_csv('./data/Paula1_WV_03.csv')

    t = df.t
    y = df.y

    aja = max_by_seg(t, y)
    print(periodo(t, y))
    print(frecuencia(t, y))
    print(voltaje_pico(t, y))
    simple_plot(t, y, 'adf 03')

