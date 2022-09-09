from modelos import RL, RC, RLC, MC, rl_current, rl_voltage, rl_voltage_exp, rl_current_exp
from utils import read_adf
import numpy as np
import scipy.optimize as opt

"""
punto 1
"""
p1 = read_adf('https://raw.githubusercontent.com/evertacosta/Numerical_Methods_2022-1/main/Reto2/datos/Problema1_MN20221_WV_P2.adf')


def calculate_r_l_direct():
    v_vs_t = p1.y1
    i_vs_t = p1.y2
    vs = v_vs_t.max()
    vs_div_r = i_vs_t.max()
    t_a = 0.0015
    v_a = p1.y1.loc[t_a]
    tao = -t_a / np.log(v_a / vs)
    r = vs / vs_div_r
    l = tao * r
    return r, l, vs


def direct_solution_p1():

    r, l, vs = calculate_r_l_direct()
    model_rl_direct_solution = RL(p1, r, l, vs)
    model_rl_direct_solution.plot('Direct Solution of R and L')

    print(r, l, vs)


direct_solution_p1()


def get_a_b_voltage_input_least_square(r, l, vs):
    def y(theta, t):
        a, b = theta[0], theta[1]
        return rl_voltage_exp(t, [r, l, vs, a, b])

    t = p1.index

    def fun(theta):
        return y(theta, t) - p1.y1

    sol = opt.least_squares(fun, [0.1, 0.1])
    print(sol.x)
    return sol.x


def direct_solution_and_a_b_least_square():
    r, l, vs = calculate_r_l_direct()

    a, b = get_a_b_voltage_input_least_square(r, l, vs)

    mod_mc_rl = RL(p1, r, l, vs)
    mod_mc_rl.exp_plot('Calculo de a y b por MC', a, b)


direct_solution_and_a_b_least_square()


def calculate_all_least_square():
    def y(theta, t):
        r, l, vs, a, b = theta[0], theta[1], theta[2], theta[3], theta[4]
        return rl_voltage_exp(t, [r, l, vs, a, b])

    t = p1.index
    voltage = p1.y1

    def fun(theta):
        return y(theta, t) - voltage

    sol = opt.least_squares(fun, [0.1, 0.1, 0.1, 0.1, 0.1])
    print(sol.x)
    return sol.x


def solution_all_least_square_p1():
    r, l, vs, a, b = calculate_all_least_square()

    mod_ls_rl = RL(p1, r, l, vs)
    mod_ls_rl.exp_plot('Calculo de todas las variables', a, b)


solution_all_least_square_p1()



def solucion_explicita_p2():
    pass

def solucion_mc_p2():
    pass

