import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import matplotlib
matplotlib.use('TkAgg')


def double_exp(time, p):
    t = time
    a, b = p[0], p[1]
    return np.exp(-a * t) - np.exp(-b * t)


def rl_voltage(time, p):
    t = time
    r, l, vs = p[0], p[1], p[2]
    tao = l / r
    return vs * np.exp(-t / tao)


def rl_current(time, p):
    t = time
    r, l, vs = p[0], p[1], p[2]
    tao = l / r
    return (vs / r) * (1 - np.exp(-t / tao))


def rl_voltage_exp(time, p):
    t = time
    r, l, vs = p[0], p[1], p[2]
    tao = l / r

    a, b = p[3], p[4]
    u_t = double_exp(t, [a, b])

    return (vs * np.exp(-t / tao)) * u_t


def rl_current_exp(time, p):
    t = time
    r, l, vs = p[0], p[1], p[2]
    tao = l / r

    a, b = p[3], p[4]
    u_t = double_exp(t, [a, b])

    return ((vs/r) * (1 - np.exp(-t/tao))) * u_t


def rc_voltage():
    pass


def rc_current():
    pass


def rc_voltage_exp(time, ):
    pass


def rc_current_exp():
    pass

class RL:
    def __init__(self, dataframe, resistance, inductance, voltage_source):
        self.df = dataframe
        self.t = self.df.index
        self.r = resistance
        self.l = inductance
        self.vs = voltage_source

    def _base_plot(self, title, voltage, current):
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)

        fig.suptitle(title)
        ax1.plot(self.t, self.df.y1)
        ax1.plot(self.t, voltage)
        ax1.set_ylabel('Voltage [V]')

        ax1.grid()

        ax2.plot(self.t, self.df.y2)
        ax2.plot(self.t, current)
        ax2.set_xlabel('Time [s]')
        ax2.set_ylabel('Current [A]')
        ax2.grid()

    def plot(self, title):
        voltage = rl_voltage(self.t, [self.r, self.l, self.vs])
        current = rl_current(self.t, [self.r, self.l, self.vs])
        self._base_plot(title, voltage, current)

    def exp_plot(self, title, a, b):
        exp_voltage = rl_voltage_exp(self.t, [self.r, self.l, self.vs, a, b])
        exp_current = rl_current_exp(self.t, [self.r, self.l, self.vs, a, b])
        self._base_plot(title, exp_voltage, exp_current)





class RC:
    def __init__(self,r, c, ):

        pass

    def voltaje(self):
        pass

    def current(self):
        pass




class RLC:
    def __init__(self):
        pass

    def voltaje(self):
        pass

    def current(self):
        pass

class MC:
    def __init__(self, time, func, respuesta, guest):
        self.t = time
        self.function = func
        self.respuesta = respuesta
        self.init = guest

    def y(self, theta, t):
        return self.function(t, theta)

    def residuos(self, theta):
        return self.y(theta, self.t) - self.respuesta

    def solucion(self):
        sol = opt.least_squares(self.residuos, self.init).x
        return sol
# la funcion que modela la respuesta
# la respuesta
# las variables
# tiempo