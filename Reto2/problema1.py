import numpy as np
from scipy import integrate, optimize
import matplotlib.pyplot as plt
from utils import least_square_method, problem_1_df, error_function


time1 = np.array(problem_1_df.time)
voltage1 = np.array(problem_1_df.voltage)
current1 = np.array(problem_1_df.current)


def source_voltaje_1(t, theta):
    e0, a, b = theta
    return e0*(np.exp(-a*t) - np.exp(-b*t))


voltage_source_values1 = least_square_method(time1, source_voltaje_1, [1, 1, 1], voltage1)

print("Los valores de Amplitud, Alpha, y Betha para la funcion doble exponencial son")
print("Amplitud:{} Alpha:{} Betha:{}".format(voltage_source_values1[0], voltage_source_values1[1], voltage_source_values1[2]))


def rl_equation(t, i, r, li):
    e0, a, b = voltage_source_values1
    vs = e0 * (np.exp(-a * t) - np.exp(-b * t))
    di = (vs - r*i)/li
    return di


res1 = optimize.minimize(error_function, [1, 0.1], args=(rl_equation, current1, (0, 0.003), [0], time1), method='Powell')
print(res1)
print("Los valores encontrados para la resistencia y el inductor son: r:{}, l:{}".format(res1.x[0], res1.x[1]))
sol1 = integrate.solve_ivp(rl_equation, (0.0, 0.003), [0], t_eval=time1, args=tuple(res1.x))


def comparacion1():
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    ax1.plot(time1, voltage1, label='medido', lw=2)
    ax1.plot(time1, source_voltaje_1(time1, voltage_source_values1), '--', label='calculado')
    ax1.set_title('Voltage')
    ax1.legend()

    ax2.plot(time1, current1, label='medido', lw=2)
    ax2.plot(sol1.t, sol1.y[0], '--', label='calculado')
    ax2.set_title('Current')
    ax2.legend()


comparacion1()

