import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.integrate import solve_ivp


def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['t', 'y1', 'y2'], usecols=[0, 1, 2], index_col=0, skiprows=2)


p1 = read_adf('./datos/Problema1_MN20221_WV_P2.adf')
p2 = read_adf('./datos/Problema2_MN20221_WV_P2.adf')
p3 = read_adf('./datos/Problema3_MN20221_WV_P2.adf')


def error_func(eq_args, eq, final_result, t_span, y0, time_eval):
    r, l = eq_args
    sol = solve_ivp(eq, t_span, y0, t_eval=time_eval, args=(r, l)).y[0]

    suma = 0
    nn = len(final_result)

    for i in range(nn):
        ei = (final_result[i] - sol[i]) ** 2
        suma = suma + ei

    error = suma / nn
    return error
