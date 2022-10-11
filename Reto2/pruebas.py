import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from utils import p1, error_func



def d_e(t):
    e0, a, b = 1000,  2000, 100000
    v = e0 * (np.exp(-a * t) - np.exp(-b * t))
    print(v)
    return v


def rl_equation1(t, i, r, li):

    angulo = 60 * np.pi / 180
    va = 20*np.cos(2*np.pi*60*t - angulo)

    di = (va - r*i)/li
    return di


def rl_equation2(t, i, r, li):
    e0, a, b = [1000,  2000, 100000]
    vs = e0 * (np.exp(-a * t) - np.exp(-b * t))
    di = (vs - r*i)/li
    return di


#sol = solve_ivp(rl_equation, (0.0, 0.003), [0], args=(150, 0.085))

time1 = np.linspace(0, 0.2, 200)

time2 = np.array(p1.index)

sol2 = solve_ivp(rl_equation1, (0.0, 0.2), [0], t_eval=time1, args=(4, 0.7))
sol2_prueba = np.array(sol2.y[0])


#sol3 = solve_ivp(rl_equation2, (0.0, 0.003), [0], t_eval=time2, args=(100, 0.2))
#sol3_prueba = np.array(sol3.y[0])


sol3_prueba = np.array(p1.y2)

res1 = minimize(error_func, [1, 0.1], args=(rl_equation1, sol2_prueba, (0, 0.2), [0], time1), method='Powell')
print(res1)

res2 = minimize(error_func, [1, 0.01], args=(rl_equation2, sol3_prueba, (0, 0.003), [0], time2), method='Powell')
print(res2)

nr, nl = res2.x

sol4 = solve_ivp(rl_equation2, (0.0, 0.003), [0], t_eval=time2, args=(nr, nl))


plt.plot(time2, sol4.y[0])
plt.plot(time2, sol3_prueba)
plt.show()
