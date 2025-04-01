# coding = utf-8
"""
5.11 使用 joblib 保存模型
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/5.md
"""
# 首先训练一个模型
import numpy as np
from sklearn import datasets, tree, ensemble

(x, y) = datasets.make_classification()
dt = tree.DecisionTreeClassifier()
dt.fit(x, y)
print("\n========== Decision Tree ==========")
print(dt)
rf = ensemble.RandomForestClassifier()
rf.fit(x, y)
print("\n========== Random Forest ==========")
print(rf)

# 保存模型
from sklearn.externals import joblib
joblib.dump(dt, __file__.replace("Joblib.py", "dt.joblib"))
joblib.dump(rf, __file__.replace("Joblib.py", "rf.joblib"))




