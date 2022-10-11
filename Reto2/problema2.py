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
            ei = (sol[i] - final_result[i]) ** 2
            suma = suma + ei

        error = suma / nn
        return error

    def solve_minimize(self, initial_guess, equation, final_result, initial_values):
        a = minimize(self.error_func, initial_guess, args=(equation, final_result, self.time_span, initial_values,
                                                           self.time_eval), method=self.minimize_method)

        return a
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

def rlc_equation(t, y, r, l, c):
    # primera derivada y' = omega
    am, f, a = [99.98136029, 60.00641109, -2.8299782]
    w = np.pi * 2 * f
    vs = am * np.sin((t*w) + a)

    # version original Evert acosta 10/10/2022

    Is, Vc = y  # corriente del circuito, voltaje en condensador

    di = (1 / l) * (vs - r*Is - Vc)
    dvc = (1/c) * Is
    return [di, dvc]


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
    tiempo = np.arange(0, 0.0951, 0.0001)
    # solucion
    valor_medido = np.array(p2.y2)[50:]
    print(tiempo[0], tiempo[-1])
    print(valor_medido[1], valor_medido[-1])
    print(len(np.arange(0, 0.0951, 0.0001)) == len(np.array(p2.y2)[50:]))
    sol_valores_respuesta = solve_ivp(rlc_equation, (0, 0.095), [0, 0], t_eval=tiempo, args=(3.99517494e+00, 1.00170237e-01, 9.99989481e-06))

    res_final = minimize(error_func, np.array([1, 0.095, 9e-6]), args=(rlc_equation, valor_medido, (0, 0.1), [0, 0], tiempo), method='Powell')

    print(res_final)
    print(res_final.x)
    sol_comprobacion = solve_ivp(rlc_equation, (0, 0.095), [0, 0], t_eval=tiempo, args=tuple(res_final.x))

    plt.plot(tiempo, valor_medido)
    plt.plot(sol_valores_respuesta.t, sol_valores_respuesta.y[0])
    plt.plot(sol_comprobacion.t, sol_comprobacion.y[0])
    plt.show()



