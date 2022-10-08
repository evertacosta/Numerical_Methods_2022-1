import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import pandas as pd


def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['t', 'y1', 'y2'], usecols=[0, 1, 2], index_col=0, skiprows=2)


p1 = read_adf('./datos/Problema1_MN20221_WV_P2.adf')


def vf(t):
    e0, a, b = [1000,  2000, 100000]
    return e0 * (np.exp(-a * t) - np.exp(-b * t))


def rl_equation(t, i, r, li):
    di = (vf(t)/li) - ((r * i) / li)
    return di


def funcion_error(eq_args, eq, final_result, t_span, y0, time_eval, eq_method='RK45'):
    r, l = eq_args
    sol = solve_ivp(eq, y0, time_eval, (r, l))

    suma = 0
    nn = len(final_result)

    for j, k in zip(sol, final_result):
        ei = (j - k) ** 2
        suma = + ei

    error = suma / nn
    return error


x0 = np.array([1, 0.1])

equation_to_solve = rl_equation
#i_final = funcion_prueba
time_span = (0, 0.003)
y0 = [0]
time = np.array(p1.index)
method = 'RK45'
#error_func_arg = (equation_to_solve, i_final, time_span, y0, time1, method)
minimize_method = 'Powell'


#res = minimize(funcion_error, x0, args=error_func_arg, method=minimize_method, tol=1e-10)
#r, l = res.x
#print(r, l)

#print(funcion_error((r, l), equation_to_solve, i_final, time_span, y0, time1, method))


funcion_prueba = solve_ivp(rl_equation, (0, 0.003), [0], t_eval=time, args=(2400, 0.029))

print(funcion_prueba)

plt.plot(p1.index, funcion_prueba.y[0])
#plt.plot(soln.t, soln.y[0])
plt.show()
