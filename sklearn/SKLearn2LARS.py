# coding = utf-8
"""
2.6 LARS (Least Angle Regression, 最小角回归) 正则化
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/2.md
"""

from sklearn.datasets import make_regression
(rdata, rtarget) = make_regression(n_samples=200, n_features=500, n_informative=10, noise=2)

import numpy as np
from sklearn.linear_model import Lars
lars10 = Lars(n_nonzero_coefs=10) # 生成过程中的 10 个信息特征
lars10.fit(rdata, rtarget)
print(lars10)
print("非 0 相关系数：", np.count_nonzero(lars10.coef_))

# 尝试 12 个 (估计)，用一半数据来训练
tn = 100
lars12 = Lars(n_nonzero_coefs=12)
lars12.fit(rdata[:tn], rtarget[:tn])
print(lars12)
lars500 = Lars() # 默认值是 500
lars500.fit(rdata[:tn], rtarget[:tn])
print(lars500)

print("10 个特征：", np.mean(np.power(rtarget[tn:] - lars10.predict(rdata[tn:]), 2)))
print("12 个特征：", np.mean(np.power(rtarget[tn:] - lars12.predict(rdata[tn:]), 2)))
print("500 个特征：", np.mean(np.power(rtarget[tn:] - lars500.predict(rdata[tn:]), 2)))






