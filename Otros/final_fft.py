import scipy.fft as fft
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('TkAgg')


def fun(t):
    return t


t = np.linspace(-1, 1, 100)

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(t, fun(t))
ax1.grid()

aja = fft.fft(fun(t))


def final(coe, t, stop):

    w0 = (2*np.pi)/2
    f = np.zeros(len(coe), dtype='complex128')

    #longitud de coe
    l = len(coe[1:])

    punto_medio = len(aja[1:])//2 + 1

    # fundamental
    c0 = coe[0]

    # complejos
    cn_p = coe[1: punto_medio]

    # complejos conjugados
    cn_n = coe[punto_medio:]

    f += c0

    n = 1
    for a, b in zip(cn_p, cn_n):
        if n < stop:
            f += a * np.exp(n * w0 * t * complex(0, 1))

            f += b * np.exp(n*w0*t*complex(0, -1))

            n += 1
        else:
            break
    return f


r_final = final(aja, t, 99)

ax2.plot(t, r_final.real)


def fts(coe, t, T, stop):

    l = len(coe)

    punto_medio = len(aja[1:]) // 2 + 1

    # fundamental
    c0 = coe[0]

    # complejos
    cn_p = coe[1: punto_medio]

    # complejos conjugados
    cn_n = coe[punto_medio:]



    w0 = (2*np.pi)/2

    f = np.zeros(5)

    a0 = coe[0]

    f += a0

    n = 1
    for an, bn in aja:
        f += an * np.cos(n*w0*t)
        f += bn * np.sin(n*w0*t)


