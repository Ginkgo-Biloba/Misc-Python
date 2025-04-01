# coding=utf-8
import numpy as np
from scipy import integrate as intgrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt

# 计算半球的体积
def ballVolume():
	def halfBall(x, y):
		return sqrt(1 - x**2 - y**2)
	def halfCircle(x):
		return sqrt(1 - x**2)
	(vol, error) = intgrt.dblquad(halfBall, -1, 1, lambda x: -halfCircle(x), lambda x: halfCircle(x))
	print ("vol =", vol)

# 对常微分方程组积分
# 计算洛伦茨吸引子的轨迹
def LorenzAttactor():
	# 给出位置矢量 w 和三个参数 sigma rho beta 计算出速度矢量 dx dy dz
	def lorenz(w, t, sigma, rho, beta):
		 (x, y, z) = w.tolist()
		 return (sigma * (y - x), x * (rho - z), x * y - beta * z)
	t = np.arange(0, 20, 0.01) # 创建时间点
	# 调用 ode 对 lorenz 进行求解 用两个不同的初始值
	track1 = intgrt.odeint(lorenz, (0.0, 1.0, 0.0), t, args=(10.0, 28.0, 2.7))
	track2 = intgrt.odeint(lorenz, (0.0, 1.01, 0.0), t, args=(10.0, 28.0, 2.7))
	# 绘图
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.plot(track1[:, 0], track1[:, 1], track1[:, 2], label="$y=1.0$")
	ax.plot(track2[:, 0], track2[:, 1], track2[:, 2], label="$y=1.01$")
	plt.legend(loc="best")
	plt.show()

# 质量-弹簧-阻尼系统
# Mx'' + bx' + kx = F
def msd(xu, t, M, k, b, F):
	(x, u) = xu.tolist()
	dx = u
	du = (F - k * x - b * u) / M
	return (dx, du)

def msdDemo():
	# 初始滑块在位移 x = -1.0 处 起始速度为 0 外部控制力恒为 1.0
	initxu = (-1.0, 0.0)
	(M, k, b, F) = (1.0, 0.5, 0.2, 1.0)
	t = np.arange(0, 40, 0.02)
	rst = intgrt.odeint(msd, initxu, t, args=(M, k, b, F))
	(fig, (ax1, ax2)) = plt.subplots(2, 1)
	ax1.plot(t, rst[:, 0], label=u"位移 x")
	ax2.plot(t, rst[:, 1], label=u"速度 u")
	ax1.legend(); ax2.legend()
	plt.show()


# 质量-弹簧-阻尼系统
class MassSpringDamper(object):
	def __init__(self, M, k, b, F):
		(self.M, self.k, self.b, self.F) = (M, k, b, F)

	# 求导函数
	def dee(self, t, xu):
		(x, u) = xu.tolist()
		dx = u
		du = (self.F - self.k * x - self.b * u) / self.M
		return [dx, du] # 要求返回列表而不是元组

# 采用 PID 控制器
class PID(object):
	def __init__(self, kp, ki, kd, dt):
		(self.kp, self.ki, self.kd, self.dt) = (kp, ki, kd, dt)
		self.lastErr = None
		self.x = 0.0
	def update(self, err):
		p = self.kp * err
		i = self.ki * self.x
		if self.lastErr is None:
			d = 0.0
		else:
			d = self.kd * (err - self.lastErr) / self.dt
		self.x += err * self.dt
		self.lastErr = err
		return p + i + d

# 控制外力 F 使滑块更迅速地停止在位移 2.0 处
def msdPID(kp, ki, kd, dt):
	stm = MassSpringDamper(M=1.0, k=0.5, b=0.2, F=1.0)
	initxu = (-1.0, 0.0)
	pid = PID(kp, ki, kd, dt)
	r = intgrt.ode(stm.dee)
	r.set_integrator("vode", method="bdf")
	r.set_initial_value(initxu, 0)
	t = list(); rst = list(); FArr = list()
	while (r.successful() and (r.t + dt < 3)):
		r.integrate(r.t + dt)
		t.append(r.t)
		rst.append(r.y)
		err = 2.0 - r.y[0]
		F = pid.update(err)
		stm.F = F
		FArr.append(F)
	rst = np.array(rst)
	t = np.array(t)
	FArr = np.array(FArr)
	(fig, (ax1, ax2, ax3)) = plt.subplots(3, 1)
	ax1.plot(t, rst[:, 0], label=u"位移 x")
	ax2.plot(t, rst[:, 1], label=u"速度 u")
	ax3.plot(t, FArr, label=u"控制力 F")
	ax1.legend(); ax2.legend(); ax3.legend()
	plt.show()

if (__name__ == "__main__"):
	# ballVolume()
	LorenzAttactor()
	# msdDemo()
	# msdPID(19.29, 1.41, 6.25, 0.02) # 最优的一组数

