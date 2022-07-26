import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from utils import p1, p2


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


# print(least_square_method(p1.index, double_exp, [0.1, 0.1, 0.1], p1.y1))

def seno(t, theta):
    am, f, a = theta
    w = np.pi*2*f
    return am*np.sin(t*w + a)


tiempo_original = np.array(p2.index)
voltaje = np.array(p2.y1)[50:]
print(tiempo_original)
print(voltaje)

n_tiempo = np.arange(0, 0.0951, 0.0001)

print(least_square_method(n_tiempo, seno, [99, 55, 0.1], voltaje))

"""
plt.plot(p1.index, p1.y1)
plt.plot(p1.index, v(p1.index))
plt.plot(p1.index, double_exp(p1.index, [999.99999421,  1999.99998294, 99999.99942604]))
plt.show()
"""


#plt.plot(tiempo_original, voltaje)
#plt.plot(aja1, v(aja1))
plt.plot(n_tiempo, seno(n_tiempo, [99.98136029, 60.00641109, -2.8299782]))
plt.show()





