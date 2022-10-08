import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from utils import p1


def v(t):
    return np.interp(t, p1.index, p1.y1)





def least_square_method(t, func, initial, final):
    # Función que modela el problema
    def y(theta, t):
        return func(t, theta)

    # Función de diferencia vectorial
    def fun_dif(theta):
        return y(theta, t) - final

    sol = least_squares(fun_dif, initial)
    return sol.x


def double_exp(t, theta):
    e0, a, b = theta
    return e0*(np.exp(-a*t) - np.exp(-b*t))


print(least_square_method(p1.index, double_exp, [0.1, 0.1, 0.1], p1.y1))

plt.plot(p1.index, p1.y1)
plt.plot(p1.index, v(p1.index))
plt.plot(p1.index, double_exp(p1.index, [999.99999421,  1999.99998294, 99999.99942604]))
plt.show()