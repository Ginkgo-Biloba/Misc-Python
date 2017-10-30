# coding=utf-8
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as Rect
from math import sin, cos

# 求非线性方程组的例子，各方程等于 0
def f(x):
	(x0, x1, x2) = x.tolist()
	return [5 * x1 + 3, 4 * x0 * x0 - 2 * sin(x1 * x2), x1 * x2 - 1.5]

# 使用雅可比矩阵
def j(x):
	(x0, x1, x2) = x.tolist()
	return [
		[0, 5, 0],
		[8 * x0, -2 * x2 * cos(x1 * x2), -2 * x1 * cos(x1 * x2)],
		[0, x2, x1]
	]

# [1, 1, 1] 是未知数的初值
def testFsolve():
	# rst = optimize.fsolve(f, [1, 1, 1]) # 不适用雅可比矩阵
	rst = optimize.fsolve(f, [1, 1, 1], fprime=j)
	print (rst)
	print (f(rst))



# 最小二乘拟合
def testLeastsq():
	X = np.array([8.19, 2.72, 6.39, 8.71, 4.7, 2.66, 3.78])
	Y = np.array([7.01, 2.78, 6.47, 6.71, 4.1, 4.23, 4.05])
	# 计算以 p 为参数的直线和原始数据之间的误差
	def res(p):
		(k, b) = p
		return Y - (k * X) - b
	# leastsq 使得 res() 的输出数组的平方和最小，参数的初始值为[1,0]
	rst = optimize.leastsq(res, [1, 0])
	(k, b) = rst[0]
	print("k =", k, "b =", b)
	fig, ax = plt.subplots()
	ax.plot(X, Y, "o")
	X0 = np.linspace(2, 10, 3)
	Y0 = k * X0 + b
	ax.plot(X0, Y0)
	for (x, y) in zip(X, Y):
		y2 = k * x + b
		rect = Rect((x, y), abs(y - y2), (y2 - y), facecolor="red", alpha=0.2)
		ax.add_patch(rect)
	ax.set_aspect("equal")
	# 误差曲面
	sk = 1.0
	sb = 10.0
	se = 1000.0 # scale_error
	# 计算直线 y = k * x + b 和原始数据 X Y 的误差的平方和
	def S(k, b):
		error = np.zeros(k.shape)
		for (x, y) in zip(X, Y):
			error += (y - k * x - b) ** 2
		return error
	(ks, bs) = np.mgrid[k - sk: k + sk: 40j, b - sb: b + sb: 40j]
	error = S(ks, bs) / se
	from mpl_toolkits.mplot3d import Axes3D
	fig2 = plt.figure(2)
	ax2 = fig2.add_subplot(111, projection="3d")
	ax2.plot_surface(ks, bs / sb, error, rstride=3, cstride=3, cmap="jet", alpha=0.5)
	ax2.scatter([k], [b / sb], [S(k, b) / se], c="r", s=20)
	plt.show()

# 拟合正线波
def testSin():
	# 数据拟合所用函数
	def func(x, p):
		(A, k, theta) = p
		return A * np.sin(2 * np.pi * k * x + theta)
	# 实验数据 x y 和拟合函数之间的差，p 为拟合需要找到的系数
	def res(p, y, x):
		return y - func(x, p)
	x = np.linspace(0, 2 * np.pi, 100)
	(A, k, theta) = (10, 0.34, np.pi / 6) # 真实数据
	y0 = func(x, (A, k, theta)) # 真实数据
	np.random.seed(0)
	y1 = y0 + 2 * np.random.randn(len(x))
	p0 = (7, 0.40, 0) # 第一次猜测的函数拟合参数
	# 调用leastsq进行数据拟合
	plsq = optimize.leastsq(res, p0, args=(y1, x))
	print(u"真实参数：", (A, k, theta))
	print(u"拟合参数：", plsq[0])
	plt.figure(1)
	plt.plot(x, y1, "o", label=u"带噪声的实验数据")
	plt.plot(x, y0, label=u"实验数据")
	plt.plot(x, func(x, plsq[0]), label=u"拟合数据")
	plt.legend(loc="best")
	plt.show()


# 计算区域极小值
# Rosenbrock 函数 f(x) = (1-x)^2 + 100(y-x^2)^2
# 最小值为 0，在 (1, 1) 处
def tgtFunc(x, y):
		return (1 - x)**2 + 100 * (y - x**2)**2
class TargetFunc(object):
	def __init__(self):
		self.f_points = list()
		self.fprime_points = list()
	
	def f(self, p):
		(x, y) = p.tolist()
		z = tgtFunc(x, y)
		self.f_points.append((x, y))
		return z

	# 导数
	def fprime(self, p):
		(x, y) = p.tolist()
		self.fprime_points.append((x, y))
		dx = -2 * (1 - x) - 400 * x * (y - x**2)
		dy = 200 * (y - x**2)
		return np.array([dx, dy])

	# 海森矩阵
	def fhess(self, p):
		(x, y) = p.tolist()
		return np.array([
			[2 * (600 * x**2 - 200 * y + 1), -400 * x],
			[-400 * x, 200]
		])

def fMin(method):
	tgt = TargetFunc()
	initPoint = (-2, -2)
	optimize.minimize(tgt.f, initPoint, method=method, jac=tgt.fprime, hess=tgt.fhess)
	return (np.array(tgt.f_points), np.array(tgt.fprime_points))

def drawFMin(fPoints, fprimePoints, ax):
	(xmin, xmax) = (np.min(fPoints[:, 0]) - 1, np.max(fPoints[:, 0]) + 1)
	(ymin, ymax) = (np.min(fPoints[:, 1]) - 1, np.max(fPoints[:, 1]) + 1)
	(Y, X) = np.ogrid[ymin:ymax:500j, xmin:xmax:500j]
	Z = np.log10(tgtFunc(X, Y))
	# zmin = np.min(Z); zmax = np.max(Z)
	ax.imshow(Z, extent=(xmin, xmax, ymin, ymax), origin="bottom", aspect="auto", cmap="gray")
	ax.plot(fPoints[:, 0], fPoints[:, 1], lw=1)
	ax.scatter(fPoints[:, 0], fPoints[:, 1], c=range(len(fPoints)), s=50, linewidths=0)
	if len(fprimePoints):
		ax.scatter(fprimePoints[:, 0], fprimePoints[:, 1], marker="x", color="white", alpha=0.5)
	ax.set_xlim(xmin, xmax)
	ax.set_ylim(ymin, ymax)

def testFmin():
	fig, axes = plt.subplots(3, 2, figsize=(6, 7))
	methods = ("Nelder-Mead", "Powell", "CG", "BFGS", "Newton-CG", "L-BFGS-B")
	for (ax, mtd) in zip(axes.ravel(), methods):
		(fPoints, fprimePoints) = fMin(mtd)
		drawFMin(fPoints, fprimePoints, ax)
		ax.set_title(mtd)
	plt.show()

# 求正弦函数最小值
def minSin():
	def func(x, p):
		(A, k, theta) = p
		return A * np.sin(2 * np.pi * k * x + theta)
	def funcError(p, x, y):
		return np.sum((y - func(x, p))**2)
	x = np.linspace(0, 2*np.pi, 100)
	(A, k, theta) = (10, 0.34, np.pi / 6)
	y0 = func(x, (A, k, theta))
	np.random.seed(0)
	y1 = y0 + 2 * np.random.randn(len(x))
	rst = optimize.basinhopping(funcError, (1, 1, 1), niter=10, minimizer_kwargs={"method":"L-BFGS-B", "args": (x, y1)})
	print (rst.x)
	fig = plt.figure(1)
	plt.plot(x, y1, "o", label=u"带噪声的实验数据")
	plt.plot(x, y0, label=u"真实数据")
	plt.plot(x, func(x, rst.x), label=u"拟合数据")
	plt.legend(loc="best")
	plt.show()


if (__name__ == "__main__"):
	# testFsolve()
	testLeastsq()
	# testSin()
	# testFmin()
	# minSin()
