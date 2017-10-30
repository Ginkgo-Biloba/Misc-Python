# coding=utf-8
import numpy as np
from scipy.integrate import odeint
from sympy import *
from sympy.physics.mechanics import *

init_printing()

"""
http://hyry.dip.jp/tech/book/page.html/scipynew/sympy-900-mechanics.html
如图所示，滑动方块可以沿着参照系 I 的 X 轴自由运动，小球与滑块使用无质量连杆相连接，可以只有摆动。小球的的初始摆动角度为 \theta_0。我们希望模拟小球释放之后，系统的运动轨迹。
"""
I = ReferenceFrame("I") # 定义惯性参考系
O = Point("O") # 定义原点
O.set_vel(I, 0)
g = symbols("g") # 重力加速度

q = dynamicsymbols("q") # 方块在参考系 I 中的位置
u = dynamicsymbols("u") # 方块在参考系 I 中的速度
m1 = symbols("m1") # 方块的质量
P1 = Point("P1") # 方块所在位置
P1.set_pos(O, q * I.x) # 点 P1 的位置相对于点 O 沿着参照系 I 的 X 轴偏移 q
P1.set_vel(I, u * I.x) # 点 P1 在参照系 I 中的速度为 X 轴方向，大小为 u
box = Particle("box", P1, m1) # 在点 P1 处放置质量为 m1 的方块 box
"""
下面定义小球所在的参照系 B，B 为 I 绕 Z 轴旋转 \theta 而得，并设置 B 相对于 I 的角速度为 \omega，角速度围绕 I 的 Z 轴正方向旋转。角速度的正方向为右手法则，即大拇指指向围绕的轴，四指的方向为正方向。
"""
theta = dynamicsymbols("theta")
omega = dynamicsymbols("omega")
B = I.orientnew("B", "Axis", [theta, I.z]) # 将 I 围绕 Z 轴旋转 theta 得到参照系 B
B.set_ang_vel(I, omega * I.z) # B 的角速度为绕参照系 I 的 Z 轴旋转 omega 角度
"""
细杆的长度为 l，小球的质量为 m_2。点 P_2 的位置相对于点 P_1，沿着参照系 B 的 Y 轴负方向偏移 l。并通过 v2pt_theory() 设置 P_2 在参照系I中的速度。若 P_2 和 P_1 在参照系B中相对固定，当 P_1 在参照系 I 中的速度以及参照系 B与参照系 I 之间的关系都是确定的时候，可以通过 P2.v2pt_theory(P1, I, B) 计算 P_2 在 I 中的速度。下面显示 P_2 在 I 中的速度为 u I_x + l \omega B_x。最后在 P_2 处放置质量为 m_2 的小球。
"""
(l, m2) = symbols("l, m2")
P2 = P1.locatenew("P2", -l * B.y) # P2相对于P1沿着 B 的 Y 轴负方向偏移 l
P2.v2pt_theory(P1, I, B) # 使用二点理论设置 P2 在 I 中的速度
ball = Particle("ball", P2, m2) # 在 P2 处放置质量为 m2 的小球
# print(P2.vel(I)) # 显示 P2 在 I 中的速度
"""
到此位置各个惯性参照系、坐标点、质点之间的关系已经确定。下面使用KanesMethod自动计算系统的微分方程组。首先需要将方块的位移q和速度u、细杆的旋转角度\theta和旋转速度\omega之间的关系通过方程eqs联系起来。particles为系统中所包含的质点列表，forces是作用力的列表，每个作用力由作用点和一个矢量决定。
"""
# 下面的程序计算出fr和frstar中每两个对应的表达式之和为零
eqs = [q.diff() - u, theta.diff() - u]
ptcs = [box, ball]
forces = [(P1, -g * I.y), (P2, -g * I.y)]
kane = KanesMethod(I, q_ind=[q, theta], u_ind=[u, omega], kd_eqs=eqs)
(fr, frstar) = kane.kanes_equations(forces, ptcs)

# mass_matrix_full和forcing_full属性是求解整个系统的完整微分方程组，包含我们传递进去的eqs中的两个方程
status = Matrix([[q], [theta], [u], [omega]])
# print(kane.mass_matrix_full, status.diff, "=", kane.forcing_full)

# 将符号表达式转换为程序
M = kane.mass_matrix_full.row_join(kane.forcing_full)
seq = cse(M)
# print(seq)
from sympy.printing import StrPrinter

class CseExprPrinter(StrPrinter):
	def _print_Integer(self, expr):
		return (str(expr) + ".0")
	def _print_Rational(self, expr):
		return "{:s}.0 / {:s}".format(expr.p, expr.q)
	def _print_Function(self, expr):
		import math
		name = expr.func.__name__
		if hasattr(math, name):
			return StrPrinter._print_Function(self, expr)
		else:
			return name
	def _print_Pow(self, expr):
		exp = expr.exp
		if (exp.is_Rational) and (exp.q != 1) and (exp is not S.Half):
			return "complex({:s})**({:s})".format(self._print(expr.base), self._print(exp))
		else:
			return super(CseExprPrinter, self)._print_Pow(expr)

def cse2Func(funcname, precodes, seq, printerClass=CseExprPrinter):
	import textwrap
	prtr = printerClass()
	codes = ["def {:s}".format(funcname)]
	codes.extend(precodes.split("\n"))
	for (var, value) in seq[0]:
		codes.append("{} = {}".format(var, prtr._print(value)))
	rts = "return ({:s})".format(", ".join([prtr._print(value) for value in seq[1]]))
	# codes.append("\n".join(textwrap.warp(rts, 120)))
	code = "\n\t".join(codes)
	return code

precode = """
from math import sin, cos
import numpy as np
Matrix = np.array
"""
code = cse2Func("funcAb(m1, m2, l, g, u, theta, omega)", precode, seq)

def funcAb(m1, m2, l, g, u, theta, omega):
	from math import sin, cos
	Matrix = np.array
	x0 = omega; x1 = theta;
	x2 = sin(x1); x3 = l * m2; x4 = x3 * cos(x1)
	return (Matrix([[1.0, 0, 0, 0, u], [0, 1.0, 0, 0, x0], [0, 0, m1 + m2, x4, x0**2.0 * x2 * x3], [0, 0, x4, l*x3, -g * l * x2]]))

def diffStatus(status, t, m1, m2, l, g):
	(q, theta, u, omega) = status
	Ab = funcAb(m1, m2, l, g, u, theta, omega)
	return np.linalg.solve(Ab[:, :-1], Ab[:, -1])

initStatus = np.array([0, np.deg2rad(45), 0, 0])
args = (1.0, 2.0, 1.0, 9.8)
diffStatus(initStatus, 0, *args)

t = np.linspace(0, 10, 500)
rst = odeint(diffStatus, initStatus, t, args=args)

import matplotlib.pyplot as plt
(fig, (ax1, ax2)) = plt.subplots(2, 1)
ax1.plot(t, rst[:, 0], label=u"位移 $q$")
ax1.legend()
ax2.plot(t, rst[:, 1], label=u"角度 $\\theta$")
ax2.legend()
plt.show()
