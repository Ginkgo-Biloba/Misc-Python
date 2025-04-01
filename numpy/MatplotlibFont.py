# coding=utf-8
from matplotlib.font_manager import fontManager
import matplotlib.pyplot as plt
import os

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111)
plt.subplots_adjust(0, 0, 1, 1, 0, 0)
plt.xticks([]); plt.yticks([])
x = 0.05; y = 0.1

fonts = [ft.name for ft in fontManager.ttflist \
	if os.path.exists(ft.fname) and (os.stat(ft.fname).st_size > 1e6)]
fonts = set(fonts)
dy = (1.0 - y) / ((3 + len(fonts)) / 4)
for ft in fonts:
	t = ax.text(x, y, u"中文字体 Chinese Fonts", {"fontname":ft, "fontsize":12}, transform=ax.transAxes)
	ax.text(x, y - dy /2, ft, transform=ax.transAxes)
	x += 0.25
	if x > 1.0:
		y += dy
		x = 0.05

plt.savefig(__file__ .replace(".py", ".png"))
