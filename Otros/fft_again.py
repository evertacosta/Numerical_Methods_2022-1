import scipy.fft as fft
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

fig, (ax1, ax2) = plt.subplots(2)

# Sampling frequency or sampling rate (fs)
# Is the average number of samples obtained in one second, thus fs=1/T
# Its units are samples per second or hertz e.g. 48.000 samples per second
# is 48kHz
fs = 7000

# Sampling interval(spacing) or sample period
T = 1/fs

# Total time1
lon = 1


t = np.arange(0, lon, T)

f = 120*np.sin(2*np.pi*t*60) + 20*np.sin(2*np.pi*t*180)
f += 10*np.sin(2*np.pi*t*300)

ax1.plot(t, f)

ff = fft.rfft(f)
sf = fft.rfftfreq(fs, T)


amplitude = 2.0 / fs * np.abs(ff)

ax2.stem(sf, amplitude)


