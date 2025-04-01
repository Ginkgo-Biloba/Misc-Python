# coding=utf-8
import sys
import numpy as np
from matplotlib import pylab as plt
# from matplotlib.backends.backend_agg import RendererAgg
# from matplotlib.path import Path
# from matplotlib import transforms
# from matplotlib.patches import Circle
# from matplotlib.text import Text
# 
# w, h = 250, 300
# rd = RendererAgg(w, h, 96)
# buf = rd.buffer_rgba()
# arr = np.frombuffer(buf, np.uint8)
# arr.shape = h, w, -1
# 
# path_data = [(Path.MOVETO, (179,1)),
# 	(Path.CURVE4, (117,75)), (Path.CURVE4, (12,230)), (Path.CURVE4, (118,230)),
# 	(Path.LINETO, (142, 187)),
# 	(Path.CURVE4, (210,290)), (Path.CURVE4, (250,132)), (Path.CURVE4, (200,105)),
# 	(Path.CLOSEPOLY, (179,1))]
# 
# code, points = zip(*path_data)
# path = Path(points, code)
# 
# gc = rd.new_gc()
# gc.set_linewidth(2)
# gc.set_foreground((1, 0, 0))
# rd.draw_path(gc, path, transforms.IdentityTransform(), (0, 1, 0))
# arr01 = arr.copy()
# 
# c = Circle((w/2, h/2), 50, edgecolor="blue", facecolor="yellow", linewidth=2, alpha=0.5)
# c.draw(rd)
# arr02 = arr.copy()
# 
# text = Text(w/2, h/2, "Circle", va="center", ha="center")
# text.figure=rd
# text.draw(rd)
# arr03 = arr.copy()
# 
# plt.subplot(1,3,1); plt.imshow(arr03, cmap="gray");
# plt.show()

fig, ax = plt.subplots()
x = np.linspace(0, 10, 1000)
line, = ax.plot(x, np.sin(x))
txt = ax.text(5, 0.5, "event", ha="center", va="center", fontdict={"size":12})

def onKeyPress(event):
	if event.key in "rgbcmyk":
		line.set_color(event.key)
	fig.canvas.draw()

def onMouse(event):
	global e
	e = event
	info = "{}\nButton: {}\nFig x,y: {}, {}\nData x,y: {:3.2f}, {:3.2f}".format(event.name, event.button, event.x, event.y, event.xdata, event.ydata)
	txt.set_text(info)
	fig.canvas.draw()

fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
fig.canvas.mpl_connect("key_press_event", onKeyPress)
fig.canvas.mpl_connect("button_press_event", onMouse)
fig.canvas.mpl_connect("button_release_event", onMouse)
fig.canvas.mpl_connect("motion_notify_event", onMouse)
plt.show()
