# coding = utf-8
"""
3.7 使用高斯混合模型的概率聚类
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/3.md
"""
import numpy as np
N = 1000
in_m = 72
in_w = 66
s_m = 2
s_w = 4
m = np.random.normal(in_m, s_m, N)
w = np.random.normal(in_w, s_w, N)

from matplotlib import pyplot as plt
plt.style.use("ggplot")
(fig, ax) = plt.subplots(figsize=(6, 4))
ax.hist(m, bins=20, label="男", alpha=0.6)
ax.hist(w, bins=20, label="女", alpha=0.6)
ax.legend()
ax.set_title("高度直方图")
fig.tight_layout()
fig.show()

# 对分组二次抽样，训练分布，之后预测剩余分组
randomSample = np.random.choice(np.array([True, False], dtype=np.bool), size=m.size)
mTest = m[randomSample]
mTrain = m[np.logical_not(randomSample)]
wTest = w[randomSample]
wTrain = w[np.logical_not(randomSample)]

# 需要男女性的高度的经验分布，基于训练集
from scipy import stats
mpdf = stats.norm(mTrain.mean(), mTrain.std())
wpdf = stats.norm(wTrain.mean(), wTrain.std())

# 假设当男性的概率更高时，设为 1；如果女性的概率更高，设为
guessM = np.where(mpdf.pdf(mTest) > wpdf.pdf(mTest), 1, 0)
print("男性概率测试", guessM.mean())
# 对女性分组做同样的测试
guessW = np.where(wpdf.pdf(wTest) > mpdf.pdf(wTest), 1, 0)
print("女性概率测试", guessW.mean())


