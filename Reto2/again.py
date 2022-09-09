import numpy as np
from utils import read_adf
import scipy.optimize as opt
import matplotlib.pyplot as plt

p1 = read_adf('https://raw.githubusercontent.com/evertacosta/Numerical_Methods_2022-1/main/Reto2/datos/Problema1_MN20221_WV_P2.adf')


def respuesta(x, r, l, a, b):

    p1 = np.exp(-(r*x)/l)
    p2 = (-(a*l))+(b*l)
    p3 = (a*l)-r
    p4 = (b*l)-r

    p5 = np.exp((-(a+b-r/l))*x)
    p6 = a*l*np.exp(a*x)
    p7 = b*l*np.exp(b*x)
    p8 = -np.exp(a*x)
    p9 = np.exp(b*x)
    p10 = ((-a*l)+r)
    p11 = ((-b*l)+r)

    return p1 * ((p2/(p3*p4)) + ((p5*(p6-p7+(r*(p8+p9))))/(p10*p11)))


def y(theta, x):
    r, l, a, b = theta[0], theta[1], theta[2], theta[3]
    return respuesta(x, r, l, a, b)

t = p1.index

def fun(theta):
    return y(theta, t) - p1.y1

sol1 = opt.least_squares(fun, [0, 0, 0.01, 0.01])

print(sol1.x)



fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle('title')
ax1.plot(p1.index, p1.y1)
ax2.plot(p1.index, y(sol1.x, p1.index))

#ax1.set_xlabel('aja')
ax1.set_ylabel('')
ax1.grid()


plt.show()