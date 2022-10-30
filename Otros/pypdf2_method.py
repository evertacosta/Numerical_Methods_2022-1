import io
import os
import zlib

txt = './hola.txt'
pdf = './Hellou World.pdf'
pdf2 = './Holamundo.pdf'

b = io.IOBase()

a = io.open(pdf, mode='rb', buffering=0)

a.seek(-40, 2)

for i in a:
    print(i, '\n')


