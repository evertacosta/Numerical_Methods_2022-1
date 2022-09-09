import scipy.fft as fft
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

fig, (ax1, ax2) = plt.subplots(2)

# sampling rate(points)
N = 60000

# total time
lon = 0.4

# sampling interval(spacing)
T = lon/N

t = np.linspace(0.0, lon, N)

f = 120*np.sin(2*np.pi*t*60) + 60*np.sin(2*np.pi*t*300)

ax1.plot(t, f)

ff = fft.rfft(f)
sf = fft.rfftfreq(N, T)


amplitude = 2.0 / N * np.abs(ff)

ax2.stem(sf, amplitude)


