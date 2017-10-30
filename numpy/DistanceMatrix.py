# coding = utf-8
import numpy as np
from scipy.spatial.distance import pdist, squareform
import time

np.random.seed(0)
X = np.random.random((200, 3))

# 三层循环逐个元素计算
def elewiseDis(X):
	(m, n) = X.shape
	D = np.empty((m, m), dtype=float)
	dist = 0.0
	diff = 0.0
	for i in range(m):
		for j in range(i, m):
			dist = 0.0
			for k in range(n):
				diff = X[i, k] - X[j, k]
				dist += diff * diff
			D[i, j] = D[j, i] = np.sqrt(dist)
	return D

stc = time.clock();
D1 = elewiseDis(X);
midc = time.clock()
D2 = squareform(pdist(X))
edc = time.clock()

print(np.allclose(D1, D2))
print(midc - stc)
print(edc - midc)
