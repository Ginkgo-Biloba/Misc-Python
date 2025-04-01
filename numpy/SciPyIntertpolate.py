# coding=utf-8
import numpy as np
from scipy import interpolate as intplt
import matplotlib.pyplot as plt

def intpltDemo():
	x = np.linspace(0, 10, 11)
	y = np.sin(x)
	xNew = np.linspace(0, 10, 101)
	plt.plot(x, y, "ro")
	kinds = ["nearest", "zero", "slinear", "quadratic"]
	for k in kinds:
		f = intplt.interp1d(x, y, kind=k)
		yNew = f(xNew)
		plt.plot(xNew, yNew, label=k)
	plt.legend(loc="lower right")
	plt.show()

# 外推插值
def univariateSplineDemo():
	x1 = np.linspace(0, 10, 21)
	y1 = np.sin(x1)
	sx1 = np.linspace(0, 12, 121)
	sy1 = intplt.UnivariateSpline(x1, y1, s=0)(sx1)
	x2 = np.linspace(0, 20, 201)
	y20 = np.sin(x2)
	y2 = y20 + np.random.standard_normal(len(x2)) * 0.2
	sx2 = np.linspace(0, 20, 2001)
	sy2 = intplt.UnivariateSpline(x2, y2, s=8)(sx2)
	plt.figure(figsize=(8, 5))
	plt.subplot(211)
	plt.plot(x1, y1, ".", label=u"数据点")
	plt.plot(sx1, sy1, label=u"Spline 曲线")
	plt.legend()
	plt.subplot(212)
	plt.plot(x2, y2, ".", label=u"数据点")
	plt.plot(sx2, sy2, label=u"Spline 曲线")
	plt.plot(x2, y20, ".", label=u"无噪声曲线")
	plt.legend(loc="best")
	plt.show()
	
# 参数曲线插值
def splprepDemo():
	x = [ 4.913, 4.913, 4.918, 4.938, 4.955, 4.949, 4.911, 4.848, 4.864, 4.893, 4.935, 4.981, 5.01 , 5.021]
	y = [ 5.2785, 5.2875, 5.291 , 5.289 , 5.28 , 5.26 , 5.245 , 5.245 , 5.2615, 5.278 , 5.2775, 5.261 , 5.245 , 5.241]
	plt.figure()
	plt.plot(x, y, "o")
	for s in (0, 1e-4, 1e-2):
		(tck, t) = intplt.splprep([x, y], s = s)
		(xi, yi) = intplt.splev(np.linspace(t[0], t[-1], 200), tck)
		plt.plot(xi, yi, label=u"s = {:g}".format(s))
	plt.legend()
	plt.show()

# 单调插值
def pchipDemo():
	x = [0, 1, 2, 3, 4, 5]
	y = [1, 2, 1.5, 2.5, 3, 2.5]
	xs = np.linspace(x[0], x[-1], 100)
	curve = intplt.pchip(x, y)
	ys = curve(xs)
	dys = curve.derivative(1)(xs) # 一阶导数
	plt.figure()
	plt.plot(xs, ys, label=u"pchip")
	plt.plot(xs, dys, label=u"一阶导数")
	plt.plot(x, y, "o")
	plt.legend(loc="best")
	plt.grid()
	plt.margins(0.1, 0.1)
	plt.show()


if (__name__ == "__main__"):
	# intpltDemo()
	# univariateSplineDemo()
	# splprepDemo()
	pchipDemo()
	