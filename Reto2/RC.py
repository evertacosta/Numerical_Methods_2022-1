# Se importan las librerias necesarias
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd


# Se define la función para lectura de archivo
def read_adf(file):
    return pd.read_csv(file, sep="\t", names=['t', 'y1', 'y2'], usecols=[0, 1, 2], index_col=0, skiprows=2)


# Fuente doble exponencial
def double_exp(time, p):
    t = time
    a, b = p[0], p[1]
    return np.exp(-a * t) - np.exp(-b * t)


# Funciones que modelan las respuestas del circuito
class RC_Functions:
    # Voltaje con corriente incial de cero en el inductor
    def rc_voltage(self, time, p):
        t = time
        r, c, vs = p[0], p[1], p[2]
        tao = r * c
        return vs * (1 - np.exp(-t / tao))

    # Corriente del inductor inicial cero
    def rc_current(self, time, p):
        t = time
        r, c, vs = p[0], p[1], p[2]
        tao = r * c
        return vs / r * np.exp(-t / tao)

    # Respuesta del voltaje teniendo en cuenta la excitación de la fuente
    def rc_voltage_exp(self, time, p):
        t = time
        r, c, vs = p[0], p[1], p[2]
        tao = r*c

        a, b = p[3], p[4]
        u_t = double_exp(t, [a, b])

        return (vs * (1 - np.exp(-t / tao))) * u_t

    # Corriente del circuito teniendo en cuenta la fuerza externa
    def rc_current_exp(self, time, p):
        t = time
        r, c, vs = p[0], p[1], p[2]
        tao = r * c

        a, b = p[3], p[4]
        u_t = double_exp(t, [a, b])

        return (vs/r*np.exp(-t/(r*c))) * u_t


# Clase para los graficos
class Baseplot:
    def __init__(self, dataframe):
        self.df = dataframe
        self.time = self.df.index
        self.response_voltage = self.df.y1
        self.response_current = self.df.y2

    def _plot(self, figure_title, user_voltage, user_current):
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)
        fig.suptitle(figure_title)
        ax1.plot(self.time, self.response_voltage)
        ax1.plot(self.time, user_voltage)
        ax1.set_ylabel('Voltage [V]')
        ax1.grid()
        ax2.plot(self.time, self.response_current)
        ax2.plot(self.time, user_current)
        ax2.set_xlabel('Time [s]')
        ax2.set_ylabel('Current [A]')
        ax2.grid()

    def _error_plot(self, figure_title, voltage_error, current_error):
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)
        fig.suptitle(figure_title)
        ax1.plot(self.time, voltage_error)
        ax1.set_ylabel('Voltage [V]')
        ax1.grid()
        ax2.plot(self.time, current_error)
        ax2.set_xlabel('Time [s]')
        ax2.set_ylabel('Current [A]')
        ax2.grid()

    def plot_compare_responses(self, figure_title, user_voltage, user_current):
        self._plot(figure_title, user_voltage, user_current)

    def plot_error(self, figure_title, voltage_error, current_error):
        self._error_plot(figure_title, voltage_error, current_error)


# Clase que modela el primer problema
class RC(RC_Functions, Baseplot):
    def __init__(self, dataframe, resistance, capacitance, voltage_source):
        self.df = dataframe
        self.t = self.df.index
        self.r = resistance
        self.c = capacitance
        self.vs = voltage_source
        Baseplot.__init__(self, self.df)
        self.response_voltage = self.df.y1
        self.response_current = self.df.y2

        self.user_voltage = self.rc_voltage(self.t, [self.r, self.c, self.vs])
        self.user_current = self.rc_current(self.t, [self.r, self.c, self.vs])

        self.exp_voltage = None
        self.exp_current = None

        self.user_responce_type = None

    # Función que grafica y compara la respuesta del problema con la respuesta calculada
    def compare_responses(self, title):
        self.user_responce_type = 'simple'
        self.plot_compare_responses(title, self.user_voltage, self.user_current)

    def compare_responses_exp(self, title, a, b):
        self.user_responce_type = 'exp'
        self.exp_voltage = self.rc_voltage_exp(self.t, [self.r, self.c, self.vs, a, b])
        self.exp_current = self.rc_current_exp(self.t, [self.r, self.c, self.vs, a, b])
        self.plot_compare_responses(title, self.exp_voltage, self.exp_current)

    def plot_relative_error(self, title):
        if self.user_responce_type == 'simple':
            voltage_relative_error = (np.abs(self.user_voltage - self.response_voltage)/self.response_voltage)*100
            current_relative_error = (np.abs(self.user_current - self.response_current)/self.response_current)*100

            voltage_relative_error[voltage_relative_error >= 3.55e2] = 0
            current_relative_error[current_relative_error >= 3.55e2] = 0
            voltage_relative_error[voltage_relative_error <= 3.55e-2] = 0
            current_relative_error[current_relative_error <= 3.55e-2] = 0
            self.plot_error(title, voltage_relative_error, current_relative_error)

        elif self.user_responce_type == 'exp':
            voltage_relative_errore = (np.abs(self.exp_voltage - self.response_voltage) / self.response_voltage) * 100
            current_relative_errore = (np.abs(self.exp_current - self.response_current) / self.response_current) * 100
            voltage_relative_errore[voltage_relative_errore >= 9.4e2] = 0
            current_relative_errore[current_relative_errore >= 9.4e2] = 0
            voltage_relative_errore[voltage_relative_errore <= 9.4e-2] = 0
            current_relative_errore[current_relative_errore <= 9.4e-2] = 0
            self.plot_error(title, voltage_relative_errore, current_relative_errore)


# Dataframe de problema 1
df_p3 = read_adf(
    'https://raw.githubusercontent.com/evertacosta/Numerical_Methods_2022-1/main/Reto2/datos/Problema3_MN20221_WV_P2.adf')


# Clase para el primer problema
class RC_sol(RC_Functions):
    def __init__(self, dataframe):
        self.df = dataframe
        self.time = self.df.index
        self.response_voltage = self.df.y1
        self.response_current = self.df.y2

    def calculate_r_c_direct(self):
        vs = self.response_voltage.max()
        v_s_r = self.response_current.max()
        r = vs / v_s_r
        tiempo = 0.00005
        i_n = self.response_current[tiempo]
        print(i_n)

        tao_p3 = -tiempo / np.log((i_n * r) / vs)

        c = tao_p3 / r

        return r, c, vs

    def direct_solution_p1(self):
        r, c, vs = self.calculate_r_c_direct()
        model_rc_direct_solution = RC(self.df, r, c, vs)
        model_rc_direct_solution.compare_responses('Direct Solution of R and C')
        model_rc_direct_solution.plot_relative_error('error')

        print(r, c, vs)

    def get_a_b_voltage_input_least_square(self, r, c, vs):
        # Función que modela el problema
        def y(theta, t):
            a, b = theta[0], theta[1]
            return self.rc_voltage_exp(t, [r, c, vs, a, b])

        # Función de diferencia vectorial
        def fun(theta):
            return y(theta, self.time) - self.response_voltage

        sol = opt.least_squares(fun, [1, 1])

        return sol.x

    # Solución directa y a-b por medio de mínimos cuadrados
    def direct_solution_and_a_b_least_square(self):
        r, c, vs = self.calculate_r_c_direct()
        a, b = self.get_a_b_voltage_input_least_square(r, c, vs)
        mod_mc_rl = RC(self.df, r, c, vs)
        mod_mc_rl.compare_responses_exp('a and b by least squares', a, b)
        mod_mc_rl.plot_relative_error('a y b mc error')

    def calculate_all_least_square(self):
        def y(theta, t):
            r, c, vs, a, b = theta[0], theta[1], theta[2], theta[3], theta[4]
            return self.rc_voltage_exp(t, [r, c, vs, a, b])

        def fun(theta):
            return y(theta, self.time) - self.response_voltage

        sol = opt.least_squares(fun, [0.1, 3.5, 1, 0.1, 0.1])
        print('r, c, vs, a, b', sol.x)
        return sol.x

    def solution_all_least_square_p1(self):
        r, c, vs, a, b = self.calculate_all_least_square()

        mod_ls_rc = RC(self.df, r, c, vs)
        mod_ls_rc.compare_responses_exp('All varaibles by least squares', a, b)
        mod_ls_rc.plot_relative_error('todos')

p3_sol = RC_sol(df_p3)

p3_sol.direct_solution_p1()
p3_sol.direct_solution_and_a_b_least_square()
p3_sol.solution_all_least_square_p1()
