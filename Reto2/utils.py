import numpy as np
import pandas as pd
from scipy import integrate, optimize


def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['time', 'voltage', 'current'], usecols=[0, 1, 2], skiprows=2)


problem_1_df = read_adf('./datos/Problema1_MN20221_WV_P2.adf')
problem_2_df = read_adf('./datos/Problema2_MN20221_WV_P2.adf')
problem_3_df = read_adf('./datos/Problema3_MN20221_WV_P2.adf')


def error_function(eq_args, eq, final_result, t_span, y0, time_eval):
    """

    :param eq_args:
    :param eq:
    :param final_result:
    :param t_span:
    :param y0:
    :param time_eval:
    :return:
    """

    sol = integrate.solve_ivp(eq, t_span, y0, t_eval=time_eval, args=tuple(eq_args))
    #print('len final y sol', len(final_result), len(sol), 'argumentos: tspan y time_eval', t_span, len(time_eval), 'args', tuple(eq_args))
    #print(sol)
    suma = 0
    nn = len(final_result)
    #print(sol)
    soly = sol.y[0]
    #print(len(sol.y))

    infinitos = 0

    if len(final_result) == len(soly):
        for i in range(nn):
            ei = (soly[i] - final_result[i]) ** 2
            suma = suma + ei
    else:
        suma = 0
        infinitos += 1

    error = suma / nn
    #print('infinitos encontrados', infinitos)
    print(error)
    return error


def least_square_method(time, func, initial, final):
    # Función que modela el problema
    def y(theta, time):
        return func(time, theta)

    # Función de diferencia vectorial
    def fun_dif(theta):
        return y(theta, time) - final

    sol = optimize.least_squares(fun_dif, initial)
    return sol.x
