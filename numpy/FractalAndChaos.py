# coding=utf-8
"""
分形与混沌绘图
"""

import numpy as np
import pylab as pl
import time
from matplotlib import cm, collections
from math import log2, sin, cos

"""
Mandelbrot 集合 f_c(z) = z^2 + c, c \in \doubleZ
Mandelbrot 集合就是使以上序列不发散的所有c点的集合。
用程序绘制 Mandelbrot 集合时不能进行无限次迭代，最简单的方法是使用逃逸时间 (迭代次数) 进行绘制，具体算法如下：
	判断每次调用函数 f_ c(z) 得到的结果是否在半径 R 之内，即复数的模小于 R
	记录下模大于 R 时的迭代次数
	迭代最多进行 N 次
	不同的迭代次数的点使用不同的颜色绘制
"""

def iterPoint(c):
	""" 计算逃逸所需的迭代次数 最多迭代 100 次 """
	z = c
	for i in range(1, 200): # 最多迭代 100 次
		if (abs(z) > 2): # 半径大于 2 认为是逃逸
			break
		z *= z; z += c
	return i # 返回迭代次数

def smoothIterPoint(c, iterN, escR):
	""""
	为了在不同的梯度之间进行渐变处理，使用下面的公式进行逃逸时间计算
	n - \log_2 \log_2 |z_n|
	z_n 是迭代n次之后的结果，通过在逃逸时间的计算中引入迭代结果的模值，结果将不再是整数，而是平滑渐变的。
	"""
	z = c
	for i in range(1, iterN):
		if (abs(z) > escR): break
		z *= z; z += c
	absz = abs(z)
	if (absz > 2.0):
		mu = i - log2(log2(absz))
	else:
		mu = i
	return mu

def drawMandelbrot(cx, cy, d):
	""" 绘制点 (cx, cy) 附近正负 d 范围的 Mandelbrot 集合"""
	(x0, x1, y0, y1) = (cx - d, cx + d, cy - d, cy + d)
	(y, x) = np.ogrid[y0:y1:400j, x0:x1:400j]
	c = x + y * 1j
	start = time.time()
	# mdb = np.frompyfunc(iterPoint, 1, 1)(c).astype(np.float)
	mdb = np.frompyfunc(smoothIterPoint, 3, 1)(c, 20, 10).astype(np.float)
	print ("time =", time.time() - start)
	pl.imshow(mdb, cmap=cm.Blues_r, extent=[x0, x1, y0, y1])
	pl.gca().set_axis_off()

def drawMdb(cx, cy, d, N=400):
	"""
	绘制点 (cx, cy) 附近正负 d 范围的 Mandelbrot 集合
	使用 NumPy 数组运算加速计算
	"""
	global mdb
	(x0, x1, y0, y1) = (cx - d, cx + d, cy - d, cy + d)
	(y, x) = np.ogrid[y0: y1: N*1j, x0: x1: N*1j]
	c = x + y * 1j
	# 创建 X Y 轴的坐标数组 用来保存没有逃逸的点的下标
	(ix, iy) = np.mgrid[0:N, 0:N]
	# 创建保存 Mandelbrot 图的二维数组 默认值为最大迭代次数 100
	mdb = np.ones(c.shape, dtype=np.int) * 100
	# 将数组都变成一维的
	ix.shape = -1; iy.shape = -1; c.shape = -1
	z = c.copy() # 从 c 开始迭代 因此开始的迭代次数为 1
	start = time.time()
	for i in range(1, 100):
		z *= z; z += c # 一次迭代
		tmp = np.abs(z) > 2.0 # 找到所有逃逸的点
		mdb[ix[tmp], iy[tmp]] = i # 将这些逃逸点的迭代次数赋值给 Mandelbrot 图
		np.logical_not(tmp, tmp) # 找到所有没有逃逸的点
		(ix, iy, c, z) = (ix[tmp], iy[tmp], c[tmp], z[tmp]) # 更新 ix iy c z 使其只包含没有逃逸的点
		if (len(z) == 0):
			break
	print ("time =", time.time() - start)
	pl.imshow(mdb, cmap=cm.Blues_r, extent=[x0, x1, y0, y1])
	pl.gca().set_axis_off()

def MandelbrotDemo():
	""" 展示 Mandelbrot 集合 """
	(x, y) = (0.27322626, 0.595153338)
	pl.subplot(231)
	# drawMandelbrot(-0.5, 0, 1.5)
	drawMdb(-0.5, 0, 1.5)
	for i in range(2, 7):
		pl.subplot(230 + i)
		# drawMandelbrot(x, y, 0.2**(i - 1))
		drawMdb(x, y, 0.2**(i - 1))
	pl.subplots_adjust(0.02, 0, 0.98, 1, 0.02, 0)
	# pl.savefig("FractalAndChaos-2.png")
	pl.show()


"""
迭代函数系统是一种用来创建分形图案的算法，它所创建的分形图永远是绝对自相似的。下面我们直接通过绘制一种蕨类植物的叶子来说明迭代函数系统的算法：
有下面4个线性函数将二维平面上的坐标进行线性映射变换：
1.
	x(n+1）= 0
	y(n+1) = 0.16 * y(n)
2.
	x(n+1) = 0.2 * x(n) − 0.26 * y(n)
	y(n+1) = 0.23 * x(n) + 0.22 * y(n) + 1.6
3.
	x(n+1) = −0.15 * x(n) + 0.28 * y(n)
	y(n+1) = 0.26 * x(n) + 0.24 * y(n) + 0.44
4.
	x(n+1) = 0.85 * x(n) + 0.04 * y(n)
	y(n+1) = −0.04 * x(n) + 0.85 * y(n) + 1.6

现在的问题是有 4 个迭代函数，迭代时选择哪个函数进行计算呢？我们为每个函数指定一个概率值，它们依次为1%, 7%, 7%和85%。选择迭代函数时使用通过每个函数的概率随机选择一个函数进行迭代。上面的例子中，第四个函数被选择迭代的概率最高。
最后我们从坐标原点(0,0)开始迭代，将每次迭代所得到的坐标绘制成图，就得到了叶子的分形图案。下面的程序演示这一计算过程：
"""

def IFS(p, eq, init, n):
	"""
	p: 每个函数的选择概率列表
	eq: 迭代函数列表
	init: 迭代初始点
	n: 迭代次数
	返回值： 每次迭代所得的X坐标数组， Y坐标数组， 计算所用的函数下标  
	"""
	# 迭代向量的初始化
	pos = np.ones(3, dtype=np.float)
	pos[:2] = init
	# 通过函数概率，计算函数的选择序列
	p = np.add.accumulate(p)
	rands = np.random.rand(n)
	select = np.ones(n, dtype=np.int) * (n - 1)
	for (i, x) in enumerate(p[::-1]):
		select[rands < x] = len(p) - i - 1
	# 结果的初始化
	rst = np.zeros((n, 2), dtype=np.float)
	c = np.zeros(n, dtype=np.float)
	for i in range(n):
		eqidx = select[i] # 所选函数的下标
		tmp = np.dot(eq[eqidx], pos) # 进行迭代
		pos[:2] = tmp # 更新迭代向量
		rst[i] = tmp; c[i] = eqidx # 保存结果
	return (rst[:, 0], rst[:, 1], c)

def IFSDemo():
	""" 使用迭代函数系统绘制蕨类植物叶子 """
	eq1 = np.array([[0,0,0],[0,0.16,0]])
	p1 = 0.01
	eq2 = np.array([[0.2,-0.26,0],[0.23,0.22,1.6]])
	p2 = 0.07
	eq3 = np.array([[-0.15, 0.28, 0],[0.26,0.24,0.44]])
	p3 = 0.07
	eq4 = np.array([[0.85, 0.04, 0],[-0.04, 0.85, 1.6]])
	p4 = 0.85
	start = time.time()
	(x, y, c) = IFS([p1, p2, p3, p4], [eq1, eq2, eq3, eq4], [0, 0], 100000)
	print ("time =", time.time() - start)
	pl.figure(figsize=(7, 7))
	pl.subplot(121)
	pl.scatter(x, y, s=1, c="g", marker="s", linewidths=0)
	pl.axis("equal"); pl.axis("off")
	pl.subplot(122)
	pl.scatter(x, y, s=1, c=c, marker="s", linewidths=0)
	pl.axis("equal"); pl.axis("off")
	pl.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
	pl.gcf().patch.set_facecolor("white")
	# pl.savefig("FractalAndChaos-2.png")
	pl.show()

"""
前面所绘制的分形图案都是都是使用数学函数的迭代产生，而L-System分形则是采用符号的递归迭代产生。首先如下定义几个有含义的符号：
	F : 向前走固定单位
	+ : 正方向旋转固定单位
	- : 负方向旋转固定单位
使用这三个符号我们很容易描述下图中由 4 条线段构成的图案：
F+F--F+F

如果将此符号串中的所有F都替换为F+F--F+F，就能得到如下的新字符串：
F+F--F+F+F+F--F+F--F+F--F+F+F+F--F+F
如此替换迭代下去，并根据字串进行绘图(符号+和-分别正负旋转60度)，可得到如下的分形图案：...

除了 F, +, - 之外我们再定义如下几个符号：
	f : 向前走固定单位，为了定义不同的迭代公式
	[ : 将当前的位置入堆栈
	] : 从堆栈中读取坐标，修改当前位置
	S : 初始迭代符号
所有的符号 (包括上面未定义的) 都可以用来定义迭代，通过引入两个方括号符号，使得我们能够描述分岔的图案。

例如下面的符号迭代能够绘制出一棵植物：
S -> X
X -> F-[[X]+X]+F[+FX]-X
F -> FF

我们用一个字典定义所有的迭代公式和其它的一些绘图信息：
{
	"X":"F-[[X]+X]+F[+FX]-X", "F":"FF", "S":"X",
	"direct":-45,
	"angle":25,
	"iter":6,
	"title":"Plant"
}
其中：
	direct : 是绘图的初始角度，通过指定不同的值可以旋转整个图案
	angle : 定义符号+,-旋转时的角度，不同的值能产生完全不同的图案
	iter : 迭代次数
下面的程序将上述字典转换为需要绘制的线段坐标：
"""

class LSystem(object):
	def __init__(self, rule):
		info = rule["S"]
		for i in range(rule["iter"]):
			ninfo = list()
			for c in info:
				if c in rule:
					ninfo.append(rule[c])
				else:
					ninfo.append(c)
			info = "".join(ninfo) # 迭代一次完成
		self.rule = rule
		self.info = info
	
	def getLines(self):
		d = self.rule["direct"]
		a = self.rule["angle"]
		p = (0, 0) # 初始坐标
		l = 1.0 # 步长
		lines = list()
		stack = list()
		for c in self.info:
			if c in "Ff": #前进
				r = d * np.pi / 180
				t = (p[0] + l * cos(r), p[1] + l * sin(r))
				lines.append((p, t))
				p = t
			elif (c == "+"): # 逆时针旋转
				d += a
			elif (c == "-"): # 顺时针旋转
				d -= a
			elif (c == "["):
				stack.append((p, d))
			elif (c == "]"):
				(p, d) = stack[-1]
				del stack[-1]
		return lines

def drawLSys(ax, rule, iter=None):
	""" 画图 """
	if iter is not None:
		rule["iter"] = iter
	lines = LSystem(rule).getLines()
	lineCll = collections.LineCollection(lines)
	ax.add_collection(lineCll, autolim=True)
	# if "title" in rule.keys(): pl.title(rule["title"])
	ax.axis("equal"); ax.axis("off")
	ax.set_xlim(ax.dataLim.xmin, ax.dataLim.xmax)
	ax.invert_yaxis()
	

def LSysDemo():
	""" 演示分形绘制 """
	rules = [
		{
			"F":"F+F--F+F", "S":"F",
			"direct":180,
			"angle":60,
			"iter":5,
			"title":"Koch"
		},
		{
			"X":"X+YF+", "Y":"-FX-Y", "S":"FX",
			"direct":0,
			"angle":90,
			"iter":13,
			"title":"Dragon"
		},
		{
			"f":"F-f-F", "F":"f+F+f", "S":"f",
			"direct":0,
			"angle":60,
			"iter":7,
			"title":"Triangle"
		},
		{
			"X":"F-[[X]+X]+F[+FX]-X", "F":"FF", "S":"X",
			"direct":-45,
			"angle":25,
			"iter":6,
			"title":"Plant"
		},
		{
			"S":"X", "X":"-YF+XFX+FY-", "Y":"+XF-YFY-FX+",
			"direct":0,
			"angle":90,
			"iter":6,
			"title":"Hilbert"
		},
		{
			"S":"L--F--L--F", "L":"+R-F-R+", "R":"-L+F+L-",
			"direct":0,
			"angle":45,
			"iter":10,
			"title":"Sierpinski"
		},
	]

	fig = pl.figure(figsize = (7, 5))
	fig.patch.set_facecolor("white")
	for i in range(6):
		ax = fig.add_subplot(231 + i)
		drawLSys(ax, rules[i])
	fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
	# pl.savefig("FractalAndChaos-3.png")
	pl.show()


if (__name__ == "__main__"):
	# MandelbrotDemo()
	IFSDemo()
	# LSysDemo()
