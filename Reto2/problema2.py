import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from utils import read_adf, error_func, p2


class Solver:
    def __init__(self, time, minimize_met='Powell'):
        self.time_eval = time
        self.time_span = (self.time_eval[0], self.time_eval[-1])
        self.minimize_method = minimize_met

    def error_func(self, eq_args, eq, final_result, t_span, y0, time_eval):
        """
        Error function
        :param eq_args:
        :param eq:
        :param final_result:
        :param t_span:
        :param y0:
        :param time_eval:
        :return:
        """
        equation_arg = tuple(eq_args)
        sol = solve_ivp(eq, t_span, y0, t_eval=time_eval, args=equation_arg).y[0]

        suma = 0
        nn = len(final_result)

        for i in range(nn):
            ei = (final_result[i] - sol[i]) ** 2
            suma = suma + ei

        error = suma / nn
        return error

    def solve_minimize(self, initial_guess, equation, final_result, initial_values):
        a = minimize(self.error_func, initial_guess, args=(equation, final_result, self.time_span, initial_values,
                                                           self.time_eval), method=self.minimize_method)

        return a


def rlc_equation(t, y, r, l, c):
    # primera derivada y' = omega
    am, f, a = [-99.98136029, 60.00641109, -1.57354255]
    w = np.pi * 2 * f
    vs = am * np.sin((t*w) + a)

    # version original Evert acosta 10/10/2022

    theta, omega = y

    return [omega, -(r/l)*omega - (1/(l*c))*theta + (vs/l)]


class RLC(Solver):
    def __init__(self, file):
        time_start = 50
        self.df = read_adf(file)

        self.time = self.df.index[time_start:]
        self.voltage = self.df.y1[time_start:]
        self.current = self.df.y1[time_start:]
        super().__init__(self.time)

    def solve(self):
        self.solve_minimize([0.1, 0.1, 0.1], rlc_equation, self.current, [-34.4643, 0])


if __name__ == "__main__":
    """
    tiempo_prueba = np.linspace(0, 0.1, 1000)
    modelo_prueba = solve_ivp(rlc_equation, (0, 0.1), [0, 1], t_eval=tiempo_prueba, args=(10, 0.1, 0.0001))
    modelo_pruebay = modelo_prueba.y[0]

    res_prueba = minimize(error_func, [0.1, 0.1, 0.1], args=(rlc_equation, modelo_pruebay, (0, 0.1), [0, 1],
                                                             tiempo_prueba), method='Powell')
    print(res_prueba)

    sol_compro = solve_ivp(rlc_equation, (0, 0.1), [0, 1], t_eval=tiempo_prueba, args=tuple(res_prueba.x))
    sol_comproy = sol_compro.y[0]

    plt.plot(tiempo_prueba, modelo_pruebay)
    plt.plot(sol_compro.t, sol_comproy)
    plt.show()
    """



    # tiempo
    aja1 = np.array(p2.index)[50:]
    # solucion
    aja3 = np.array(p2.y2)[50:]

    res_final = minimize(error_func, [0.1, 0.1, 0.1], args=(rlc_equation, aja3, (0, 0.1), [0, 0],
                                                             aja1), method='Powell')

    print(res_final.x)
    sol_comprobacion = solve_ivp(rlc_equation, (0, 0.1), [0, 0], t_eval=aja1, args=tuple(res_final.x))

    plt.plot(aja1, aja3)
    plt.plot(sol_comprobacion.t, sol_comprobacion.y[0])
    plt.show()



