# coding = utf-8
import cclip
import array
import numpy as np
from timeit import timeit

a = array.array("d", [1, -3, 4, 7, 2, 0])
print(a)
cclip.clip(a, 0.5, 4.5, a)
print(a)

b = np.random.uniform(-10, 10, 100000)
print(b)
c = np.zeros_like(b)
cclip.clip(b, -5, 5, c)
print(c)
print(np.min(c), np.max(c))


# 速度查看
t1 = timeit("np.clip(b, -5, 5, c)", "from __main__ import b, c, np", number=5000)
print("numpy.clip: {:f}".format(t1))
t2 = timeit("cclip.clip(b, -5, 5, c)", "from __main__ import b, c, cclip", number=5000)
print("cclip.clip: {:f}".format(t2))
