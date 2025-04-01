# coding=utf-8
import numpy as np
from scipy import sparse

def dokDemo():
	print("-- dok_matrix --")
	a = sparse.dok_matrix((10, 5))
	a[2:5, 3] = [[1.0], [2.0], [3.0]]
	print(a.keys())
	print(a.values())

def LilDemo():
	print("-- lil_matrix --")	
	b = sparse.lil_matrix((10, 5))
	b[2, 3] = 1.0
	b[3, 4] = 2.0
	b[3, 2] = 3.0
	print(b.data)
	print(b.rows)

def cooDemo():
	print("-- coo_matrix --")
	row = [2, 3, 3, 2]
	col = [3, 4, 2, 3]
	data = [1, 2, 3, 10]
	c = sparse.coo_matrix((data, (row, col)), shape=(5, 6))
	print(c.col, c.row, c.data)
	print(c.toarray())

if (__name__ == "__main__"):
	dokDemo()
	LilDemo()
	cooDemo()