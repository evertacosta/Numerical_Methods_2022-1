import numpy as np
from cmath import phase, polar

r1 = 40
l1 = 133e-3j*60
c1 = - 49e-6j*60
r2 = 40

sol = np.linalg.solve([[r1+l1, -l1, 0], [-l1, l1+c1, -c1], [0, -c1, r2+c1]], [120+0j, 0, -60+0j])

print(polar(sol[0]))
print(polar(sol[1]))
print(polar(sol[2]))

