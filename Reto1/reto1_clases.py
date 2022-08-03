import numpy as np
from utils import read_adf, read_csv, simple_plot
import matplotlib.pyplot as plt
import matplotlib


matplotlib.use('TkAgg')


class MaxBySegments:
    def __init__(self, df):
        self.dataframe = df
        self.time = self.dataframe.t
        self.y = self.dataframe.y
        self.y_mean = self.dataframe.y.mean()

    def _reverse_sign(self, sign):
        if sign:
            return False
        else:
            return True

    def _get_sign(self, value):
        if value > self.y_mean:
            return True
        else:
            return False

    def _segments(self):
        s = []
        index = 0

        initial_sign = self._get_sign(self.y[0])

        for valor in self.y:
            if self._get_sign(valor) != initial_sign:
                initial_sign = self._reverse_sign(initial_sign)
                s.append(index)

            index += 1

        s.append(len(self.y) - 1)

        return s

    def _max_by_seg(self):
        last_index = 0
        max_points = []

        s = self._segments()

        for punto in s:
            # print('segmento', last_index, punto)
            grupo = self.y[last_index:punto]
            grupo_t = self.time[last_index:punto]

            signo = self._get_sign(grupo[last_index])
            # print('signo', signo)
            if signo:
                # print(grupo_t[last_index+grupo.argmax()], grupo.max())
                max_points.append((grupo_t[last_index + grupo.argmax()], grupo.max()))
            else:
                # print(grupo_t[last_index+grupo.argmin()], grupo.min())
                max_points.append((grupo_t[last_index + grupo.argmin()], grupo.min()))

            last_index = punto

        return max_points

    def get_max_points(self):
        return self._max_by_seg()


class Fourier:
    def __init__(self, df, n, periodo):
        self.dataframe = df
        self.time = self.dataframe.t
        self.y = self.dataframe.y
        self.periodo = periodo
        self.n = n

    def _frecuencia_angular(self, periodo):
        """
        Calcula la frecuencia angular de una funcion discreta
        :param t: np.array
        :return: float
        """
        return (2 * np.pi) / periodo

    def _integracion_trapezoidal_discretas(self, t, y):

        h = (t[len(y) - 1] - t[0]) / t.size

        suma = y[0]

        suma += (2 * y[1:]).sum()

        suma += y[len(y) - 1]

        I = h * (suma / 2)

        return I

    def _coeficientes_regla_trapezoidal(self, t, y, n):
        aj_list = []
        bj_list = []

        T = self.periodo

        w = self._frecuencia_angular(T)

        for j in range(1, n + 1):
            componente_cos = y * np.cos(j * w * t)
            componente_sen = y * np.sin(j * w * t)

            aj = (2 / T) * self._integracion_trapezoidal_discretas(t, componente_cos)
            bj = (2 / T) * self._integracion_trapezoidal_discretas(t, componente_sen)

            aj_list.append(aj)
            bj_list.append(bj)

        return aj_list, bj_list

    def get_coeficientes(self):
        return self._coeficientes_regla_trapezoidal(self.time, self.y, self.n)


class Signal:
    def __init__(self, df, n):
        self.dataframe = df
        self.time = self.dataframe.t
        self.y = self.dataframe.y

        self.maximos = MaxBySegments(df).get_max_points()

        self.periodo = self._periodo()

        self.frecuencia = self._frecuencia()

        self.valor_dc = self._valor_dc()

        self.valor_pico = self._valor_pico()

        self.coeficientes_fourier = Fourier(df, n, self.periodo).get_coeficientes()

        self.valor_pico_pico = self._valor_pico_pico()

    def _periodo(self):
        return self.maximos[3][0] - self.maximos[1][0]

    def get_periodo(self):
        return self.periodo

    def _frecuencia(self):
        return 1 / self.periodo

    def get_frecuencia(self):
        return self.frecuencia

    def _valor_pico(self):
        return abs(self.maximos[3][1] - self.valor_dc)

    def get_valor_pico(self):
        return self.valor_pico

    def _valor_dc(self):
        return self.y.mean()

    def get_valor_dc(self):
        return self.valor_dc

    def get_componentes_armonicas(self):
        return self.coeficientes_fourier

    def _valor_pico_pico(self):
        return self._valor_pico() * 2


class Graficar:
    def __init__(self, df, title):
        self.data = df
        self.s = Signal(df, 10)
        self.title = title
    def plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.data.t, self.data.y, label='Signal')
        ax.hlines(self.s.valor_dc, xmin=self.data.t.iat[0], xmax=self.data.t.iat[-1],
                  label='dc={}'.format(self.round_result(s.valor_dc)), ls='-.', color='y')
        ax.hlines(self.s.valor_pico, xmin=self.data.t.iat[0], xmax=self.data.t.iat[-1],
                  label='Vp={}'.format(self.round_result(s.valor_pico)), ls='--', color='m')
        ax.hlines(self.s.valor_pico*-1, xmin=self.data.t.iat[0], xmax=self.data.t.iat[-1],
                  label='Vpp={}'.format(self.round_result(s.valor_pico_pico)), ls='--', color='r')

        ax.set_xlabel('time')
        ax.set_ylabel('y')
        ax.set_title('{} T={}, f={}'.format(self.title, self.round_result(s.get_periodo()),
                                            self.round_result(s.get_frecuencia())))
        ax.legend()

        fig2, ax2 = plt.subplots()
        ax2.stem(np.arange(0, 10, 1), np.abs(s.get_componentes_armonicas()[0]))
        ax2.set_title('{} Armonicos'.format(self.title))
        ax2.set_xlabel('ARmonico')
        ax2.set_ylabel('Amplitud')
        #ax2.set_xticks(np.arange(0, 10, 1), labels=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10'])


    def round_result(self, a):
        return np.round(a, 2)


if __name__ == "__main__":
    # adf03
    # df = read_adf('./data/PAula1_WV_03.adf')
    # adf03v
    #df = read_adf('./data/PAula1_WV_03v.adf')
    # adf04
    df = read_adf('./data/PAula1_WV_04.adf')
    # adf04v
    #df = read_adf('./data/PAula1_WV_04v.adf')

    #simple_plot(df.t, df.y, 'adf 04v')

    s = Signal(df, 10)

    Graficar(df, 'PAula1_WV_04.adf').plot()
    print(s.get_periodo())
    print(s.get_frecuencia())
    print(s.get_componentes_armonicas())
    print(s.get_valor_pico())
    print(s.get_valor_dc())





