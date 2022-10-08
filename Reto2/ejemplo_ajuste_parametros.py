import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import pandas as pd


def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['t', 'y1', 'y2'], usecols=[0, 1, 2], index_col=0, skiprows=2)

gmethod = 'RK45'

p1 = read_adf('./datos/Problema1_MN20221_WV_P2.adf')

i_t = (0, 0.003)

tiempo = np.array(p1.index)
v_final = np.array(p1.y1)
i_final = np.array(p1.y2)


# Ecuacion diferencial
def ecuacion(t, i, r, l, a, b):
    vf = np.exp(-a * t) - np.exp(-b * t)
    #vf = 1
    di = (vf - (r * i)) / l
    return di


"""
Funcion de error que calcula la diferencia entre el resultado final y el modelo
Variables: r, l, a, b
"""
#ut = np.arange(0, 10, 0.1)


def funcion_error(X, t, i_final):
    r, l, a, b = X
    sol = odeint(ecuacion, [0], t, (r, l, a, b))

    suma = 0
    nn = len(sol)

    print('Dimension sol', nn)
    print('Dimension i_final', len(i_final))

    for j, k in zip(sol, i_final):
        ei = (j - k) ** 2
        suma = + ei

    error = suma / nn
    #print(error)
    return error


#ej1 = solve_ivp(ecuacion, i_t, [0], args=(1, 0.1, 0, 0), t_eval=tiempo, method=gmethod)
#solej1 = ej1.y[0]

# Toma como argumentos
# Funcion de error
# Valores iniciales de busqueda
# Argumentos extras para la funcion error
res = minimize(funcion_error, [0.1, 0.1, 0, 0], args=(tiempo, i_final), method='Powell')
print(res)


prueba = odeint(ecuacion, [0], tiempo, (res.x[0], res.x[1], res.x[2], res.x[3]))

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(tiempo, i_final)
ax2.plot(tiempo, prueba)
plt.show()

