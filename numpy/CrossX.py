# coding=utf-8
import numpy as np
from matplotlib import widgets
from matplotlib import pyplot as plt

np.random.seed(0)
fig, ax = plt.subplots(1,1)
ax.plot(np.random.randn(100), color="green")
cursor = widgets.Cursor(ax, useblit=True, linestyle=":")
plt.show()