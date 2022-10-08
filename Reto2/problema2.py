import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from utils import p1


def rlc_equation(t, y, r, l, c):

    i = y[0]
    v = y[1]
    vs = 120*np.sin(2*np.pi*60*t)
    rih = -(r/l)*v - i/(l*c) - vs
    return [v, rih]


ejemplo1 = solve_ivp(rlc_equation, (0, 0.2), [0, 0], args=(100, 0.001, 0.000025))
print(ejemplo1)


plt.plot(ejemplo1.t, ejemplo1.y[0])
plt.show()