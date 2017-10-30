# coding = utf-8
"""
2.8 贝叶斯岭回归
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/2.md
"""
from sklearn.datasets import make_regression
(x, y) = make_regression(1000, 10, n_informative=2, noise=20)

from sklearn.linear_model import BayesianRidge
br = BayesianRidge()
br.fit(x, y)
print("===== br =====")
print(br.coef_)

# 调整超参数
brAlpha = BayesianRidge(alpha_1=10, lambda_1=10)
brAlpha.fit(x, y)
print("===== brAlpha =====")
print(brAlpha.coef_)

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
plt.style.use("ggplot")
form = lambda x, y: "loc={}, scale={}".format(x, y)
g1 = lambda x, y=1e-6, z=1e-6: stats.gamma.pdf(x, y, z)
g2 = lambda x, y=1e-6, z=1: stats.gamma.pdf(x, y, z)
g3 = lambda x, y=1e-6, z=2: stats.gamma.pdf(x, y, z)
rng = np.linspace(0, 5, 300)
(fig, ax) = plt.subplots(figsize=(7, 5))
ax.plot(rng, list(map(g1, rng)), label=form(1e-6, 1e-6))
ax.plot(rng, list(map(g2, rng)), label=form(1e-6, 1))
ax.plot(rng, list(map(g3, rng)), label=form(1e-6, 2))
ax.set_title("不同形状的 Gamma 分布")
ax.legend()
fig.tight_layout()
fig.show()

g4 = lambda x: stats.laplace.pdf(x)
rng = np.linspace(-5, 5, 300)
(fig, ax) = plt.subplots(figsize=(6, 4))
ax.plot(rng, list(map(g4, rng)))
ax.set_title("双边指数分布示例")
fig.tight_layout()
fig.show()