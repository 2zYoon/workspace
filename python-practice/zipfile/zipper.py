import zipfile
import os

tozips = ['tozip1', 'tozip2', 'tozip3']

for i in tozips:
    f = zipfile.ZipFile("out/p1-" + i + ".zip", 'a')
    f.write("in/" + i)
    f.close()

print("hmmm...sucks")