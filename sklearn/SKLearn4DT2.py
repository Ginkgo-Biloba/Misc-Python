# coding = utf-8
"""
4.2 调整决策树模型
http://git.oschina.net/wizardforcel/sklearn-cb/blob/master/4.md
"""
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

(x, y) = make_classification(1000, 20, 3)
dt = DecisionTreeClassifier()
dt.fit(x, y)

# 可视化决策树
from io import StringIO
from sklearn import tree
import pydot
dot = r"C:\_Settings\graphviz-2.38\bin\dot.exe" # Graphviz 的路径

def plotDT(model, filename):
	strBuffer = StringIO()
	tree.export_graphviz(model, out_file=strBuffer)
	graph = pydot.graph_from_dot_data(strBuffer.getvalue())
	graph[0].write(filename, prog=dot, format="png")

plotDT(dt, __file__.replace(".py", "-Gini_None.png"))

# 限制深度
dt5 = DecisionTreeClassifier(max_depth=5)
dt5.fit(x, y)
plotDT(dt5, __file__.replace(".py", "-Gini_5.png"))

# 用熵做分割标准，默认是基尼系数
dtEntropy = DecisionTreeClassifier(criterion="entropy", min_samples_leaf=10, max_depth=5)
dtEntropy.fit(x, y)
plotDT(dtEntropy, __file__.replace(".py", "-Entropy_5.png"))

