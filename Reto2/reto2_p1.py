import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import matplotlib
from utils import read_adf

matplotlib.use('TkAgg')

p1 = read_adf('./datos/Problema1_MN20221_WV_P2.adf')
v_vs_t = p1.y1
i_vs_t = p1.y2


# voltage
def v_t(vs, t, r, l):
    tao = l/r
    return vs * np.exp(-t/tao)


# current
def i_t(vs, t, r, l):
    tao = l / r
    return (vs/r) * (1 - np.exp(-t/tao))

"""
Solucion explicita

"""

vs = v_vs_t.max()

vs_div_r = i_vs_t.max()

t_a = 0.0015
v_a = p1.y1.loc[t_a]
#print(v_a)

tao = -t_a / np.log(v_a/vs)

r = vs/vs_div_r
l = tao*r


def the_plot():
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(p1.index, p1.y1, label='original')
    ax1.plot(p1.index, v_t(vs, p1.index, r, l), label='explicita')
    ax1.legend()

    ax2.plot(p1.index, p1.y2, label='origibal')
    ax2.plot(p1.index, i_t(vs, p1.index, r, l))

the_plot()



"""
Solucion usando el metodo de los minimos cuadrados
"""

def y(theta, t):
    rt, lt = theta[0], theta[1]
    return v_t(vs, t, rt, lt)

t = p1.index

def fun(theta):
    return y(theta, t) - p1.y1


sol1 = opt.least_squares(fun, [1, 0.1])

print(sol1.x)

fig1, ax1 = plt.subplots()
ax1.plot(p1.index, y(sol1.x, p1.index), label='minimos')
ax1.plot(p1.index, p1.y1, label='original')
ax1.legend()




