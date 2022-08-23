import scipy.optimize as opt
import numpy as np
from utils import read_adf
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

matplotlib.use('TkAgg')

p1 = read_adf('./datos/Problema1_MN20221_WV_P2.adf')


# voltage function in a rl circuit

def y(theta, t):
    r, l = theta[0], theta[1]
    return 904.801*np.exp(-t*(r/l))

t = p1.index

def fun(theta):
    return y(theta, t) - p1.y1


sol1 = opt.least_squares(fun, [47.97, 0.024])

print(sol1.x)

fig, ax1 = plt.subplots()
ax1.plot(p1.index, y(sol1.x, p1.index))
ax1.plot(p1.index, p1.y1)

