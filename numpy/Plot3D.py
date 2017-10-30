# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D as a3d
import scipy.io as sio

def plotSurface():
	f1 = plt.figure(1)
	ax = a3d(f1)
	x = np.arange(-4, 4, 0.2)
	y = np.arange(-4, 4, 0.2)
	(x, y) = np.meshgrid(x, y)
	r = np.sqrt(x * x + y * y)
	z = np.sin(r)
	ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap="rainbow")
	plt.show()

def plotScatter():
	data = sio.loadmat("4a.mat")
	m = data["data"]
	(x, y, z) = (m[0], m[1], m[2])
	f2 = plt.figure(2)
	ax = plt.subplot(projection="3d") #创建一个三维的绘图工程
	#将数据点分成三部分画，在颜色上有区分度
	ax.scatter(x[:1000], y[:1000], z[:1000], cmap="yellow")
	ax.scatter(x[1000:4000], y[1000:4000], z[1000:4000], cmap="red")
	ax.scatter(x[4000:], y[4000:], z[4000:], cmap="green")
	ax.set_zlabel("z")
	ax.set_ylabel("y")
	ax.set_xlabel("x")
	plt.show()

if __name__ == "__main__":
	plotSurface()
	plotScatter()
