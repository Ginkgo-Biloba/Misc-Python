# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
import matplotlib.patches as mpch
import matplotlib.image as mimg

class ImageMaskDraw(object):
	def __init__(self, ax, img):
		self.ax = ax
		self.height, self.width, _ =img.get_array().shape
		self.rder = RendererAgg(self.width, self.height, 96)
		buf = self.rder.buffer_rgba()
		arr = np.frombuffer(buf, np.uint8)
		self.array = arr.reshape(self.width, self.height, 4)
		self.maskImg = mimg.AxesImage(self.ax, alpha=0.7, animated=True, zorder=1000)
		self.maskImg.set_data(self.array)
		self.ax.add_artist(self.maskImg)

		# 一堆事件函数
		self.canvas = ax.figure.canvas
		self.canvas.mpl_connect("motion_notify_event", self.on_move)
		self.canvas.mpl_connect("draw_event", self.on_draw)
		self.canvas.mpl_connect("button_press_event", self.on_press)
		self.canvas.mpl_connect("button_release_event", self.on_release)
		self.canvas.mpl_connect("scroll_event", self.on_scroll)

		self.circle = mpch.Circle((0, 0), 4, facecolor="red", alpha=0.5, animated=True)
		self.ax.add_patch(self.circle)

		self.maskCircle = mpch.Circle((0, 0), 10, facecolor="white", lw=0)
		self.maskLine = plt.Line2D((0, 0), (0, 0), lw=8, solid_capstyle="round", color="white")

		self.bkgd = None
		self.lastPos = None

	def _update(self):
		if (self.bkgd is not None):
			self.canvas.restore_region(self.bkgd)
		if self.maskImg.get_animated():
			self.ax.draw_artist(self.maskImg)
		self.ax.draw_artist(self.circle)

	def on_scroll(self, event):
		rd = self.circle.get_radius()
		rd += event.step
		rd = max(3, min(30, rd))
		self.circle.set_radius(rd)
		self.maskCircle.set_radius(rd)
		self.maskLine.set_linewidth(rd * 2 - 2)
		self._update()

	def on_press(self, event):
		if (event.button == 1) and (event.inaxes is self.ax):
			self.maskImg.set_animated(True)
			self.canvas.draw()
			self.lastPos = (event.xdata, self.height - event.ydata)
			self.maskCircle.center = self.lastPos
			self.maskCircle.draw(self.rder)
			self.maskImg.set_array(self.array)
			self._update()

	def on_release(self, event):
		self.maskImg.set_animated(False)
		self.lastPos = None
		self.canvas.draw()

	def on_draw(self, event):
		self.bkgd = self.canvas.copy_from_bbox(self.ax.bbox)

	def on_move(self, event):
		if (event.inaxes != self.ax):
			self.circle.set_visible(False)
			return
		self.circle.set_visible(True)
		self.circle.center = (event.xdata, event.ydata)
		if (self.lastPos is not None):
			pos = (event.xdata, self.height - event.ydata)
			self.maskLine.set_data((self.lastPos[0], pos[0]), (self.lastPos[1], pos[1]))
			self.maskLine.draw(self.rder)
			self.lastPos = pos
			self.maskImg.set_array(self.array)
		self._update()

if (__name__ == "__main__"):
	pic = plt.imread(r"../Images/dora.png")
	fig, ax = plt.subplots()
	img1 = ax.imshow(pic, origin="upper")
	im = ImageMaskDraw(ax, img1)
	fig.show()
		
# 又失败了