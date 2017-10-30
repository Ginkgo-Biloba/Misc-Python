# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

# 使用缓存快速重绘图表
def Ani1():
	fig, ax = plt.subplots()
	x = np.linspace(0, 10, 500)
	line, = plt.plot(x, np.sin(x), lw=2, animated=True)
	fig.canvas.draw()
	bg = fig.canvas.copy_from_bbox(ax.bbox)
	
	def udData(line, fig):
		x[:] += 0.1
		line.set_ydata(np.sin(x))
		# line.set_color(np.random.random(3))
		fig.canvas.restore_region(bg)
		ax.draw_artist(line)
		fig.canvas.blit(ax.bbox)
	
	tmr = fig.canvas.new_timer(interval=50)
	tmr.add_callback(udData, line, fig)
	tmr.start()
	plt.show()

# animation 模块
def Ani2():
	from matplotlib.animation import FuncAnimation
	fig, ax = plt.subplots()
	x = np.linspace(0, 4*np.pi, 200)
	y = np.sin(x)
	line, = ax.plot(x, y, lw=2, animated=True)

	def updateLine(i):
		y = np.sin(x + 2* i * np.pi / 100)
		line.set_ydata(y)
		return [line]

	ani = FuncAnimation(fig, updateLine, interval=25, frames=100 ,blit=True)
	ani.save("SinWave.avi", fps=25, dpi=96)

if __name__ == "__main__":
	Ani2()
