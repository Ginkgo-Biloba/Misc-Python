# coding = utf-8
"""
2.5 LASSO (Least Absolute Shrinkage and Selection Operator, 最小绝对值收缩和选择算子) 正则化
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/2.md
"""

from sklearn.datasets import make_regression
(rdata, rtarget) = make_regression(n_samples=200, n_features=500, n_informative=5, noise=5)

from sklearn.linear_model import Lasso
lasso = Lasso()
lasso.fit(rdata, rtarget)
print(lasso)

import numpy as np
print("非 0 的相关系数个数：", np.count_nonzero(lasso.coef_))

# 交叉验证
from sklearn.linear_model import LassoCV
lcv = LassoCV()
lcv.fit(rdata, rtarget)
print(lcv)
print("确定最合适的 \alpha：", lcv.alpha_)
print("前 10 个相关系数：", lcv.coef_[:10])
print("非 0 的相关系数个数：", np.count_nonzero(lcv.coef_))

# 非 0 的相关系数可以用来选择特征
