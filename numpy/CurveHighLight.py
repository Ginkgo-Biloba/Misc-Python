# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jn

#  fig, ax = plt.subplots()
#  rect = plt.Rectangle((np.pi, -0.5), 1, 1, fc=np.random.random(3), picker=True)
#  ax.add_patch(rect)
#  x = np.linspace(0, np.pi*2, 100)
#  y = np.sin(x)
#  line, = plt.plot(x, y, picker=6.0)
#  
#  def onPick(event):
#  	art = event.artist
#  	if isinstance(art, plt.Line2D):
#  		lw = art.get_linewidth()
#  		art.set_linewidth(lw % 4 + 1)
#  	else:
#  		art.set_fc(np.random.random(3))
#  	fig.canvas.draw()
#  
#  fig.canvas.mpl_connect("pick_event", onPick)
#  plt.show()

# High Light one Curve
class CurveHL(object):
	def __init__(self, ax, alpha=0.4, linewidth=2):
		self.ax = ax
		self.alpha = alpha
		self.linewidth = linewidth
		ax.figure.canvas.mpl_connect("motion_notify_event", self.OnMove)

	def HL(self, target):
		needRedraw = False
		if target is None:
			for line in self.ax.lines:
				line.set_alpha(1.0)
				if (line.get_linewidth() != 1.0):
					line.set_linewidth(1.0)
					needRedraw = True
		else:
			for line in self.ax.lines:
				lw = self.linewidth if (line is target) else 1
				if (line.get_linewidth() != lw):
					line.set_linewidth(lw)
					needRedraw = True
				alpha = 1.0 if (lw == self.linewidth) else self.alpha
				line.set_alpha(alpha)
		if needRedraw:
			self.ax.figure.canvas.draw_idle()

	def OnMove(self, event):
		ax = self.ax
		for line in ax.lines:
			if (line.contains(event)[0]):
				self.HL(line)
				return
		self.HL(None)

fig, ax = plt.subplots()
x = np.linspace(0, 50, 300)
for i in range(1, 10):
	ax.plot(x, jn(i, x))

ch = CurveHL(ax)
plt.show()
