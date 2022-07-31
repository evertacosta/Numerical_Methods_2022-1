from utils import read_adf, simple_plot
import numpy as np
import pandas as pd

df = read_adf('./data/PAula1_WV_03.adf')


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
        #print('segmento', last_index, punto)
        grupo = y[last_index:punto]
        grupo_t = t[last_index:punto]

        signo = get_signo(grupo[last_index], y.mean())
        #print('signo', signo)
        if signo:
            #print(grupo_t[last_index+grupo.argmax()], grupo.max())
            puntos.append((grupo_t[last_index+grupo.argmax()], grupo.max()))
        else:
            #print(grupo_t[last_index+grupo.argmin()], grupo.min())
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


# lectura de archivos
def lectura(nombre):
    """
    nombre: archivo (str)
    Lectura de archivos adf o csv.
    La información está separada en columnas por espacio en blanco o punto y
    coma.
    Columna 1: Tiempo.
    Columna 2: Voltaje.
    Retorna una matriz (lista de listas).
    """
    datos = open(nombre)
    datos.readline() # primera línea
    datos.readline() # segunda línea
    dt = [] # tiempo
    dv = [] # señal
    data = dict()
    for i in datos:
        if nombre.endswith(".adf"):
            a = i.split("\t")
        elif nombre.endswith(".csv"):
            a = i.split(";")
        else:
            print("Tipo de archivo no válido.")
        dt.append(float(a[0]))
        dv.append(float(a[1]))
    datos.close()
    data = dict(zip(dv, dt))
    return [dt, dv, data]

datos = lectura('./data/PAula1_WV_03.adf')

t = pd.Series(datos[0])
y = pd.Series(datos[1])

print(periodo(t, y))
print(frecuencia(t, y))
print(voltaje_pico(t, y))
simple_plot(t, y, 'adf 03')

