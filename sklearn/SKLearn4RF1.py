# coding = utf-8
"""
4.3 使用许多决策树：随机森林
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/4.md
"""
from sklearn.datasets import make_classification
(x, y) = make_classification(1000)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(x, y)
print("精度 {:f}".format((y == rf.predict(x)).mean()))

# 预测的准确率
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use("ggplot")
(fig, ax) = plt.subplots(figsize=(6, 5))
prob = rf.predict_proba(x)
df = pd.DataFrame(prob, columns=['0', '1'])
df['was_correct'] = (rf.predict(x) == y)
dfc = df.groupby('0').was_correct.mean()
dfc.plot(kind='bar', ax=ax)
ax.set_ylabel("正确率 (%)")
ax.set_xlabel("预测为第 0 类的概率")
ax.set_title("预测为 0 类的概率的正确率")
fig.tight_layout()
fig.show()

# 特征的重要程度
(fig, ax) = plt.subplots(figsize=(6, 5))
idx = np.arange(0, x.shape[1])
ax.bar(idx, rf.feature_importances_)
ax.set_title("特征的重要性")
fig.tight_layout()
fig.show()





