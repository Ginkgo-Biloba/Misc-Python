# coding = utf-8
import numpy as np
import pandas as pd

def demo1():
	s = pd.Series([1, 2, 3, 4, 5], index=["a", "b", "c", "d", "e"])
	print(s.index)
	print(s.values)
	print(s[2], s["d"])
	print("切片")
	print(s[1:3]) # 包括起始位置，但不包括结束位置
	print(s["b":"d"]) # 标签切片则同时包括起始标签和结束标签
	print("字典方法")
	print(list(s.iteritems()))
	print("--------------------------------------------------")
	print("按标签对齐进行运算")
	s2 = pd.Series([20,30,40,50,60], index=["b","c","d","e","f"])
	print("s"), print(s)
	print("s2"), print(s2)
	print("s + s2"), print(s + s2)
	print("对于标签不存在的元素指定一个缺省值进行运算")
	print(s.add(s2, fill_value=0)) # add 方法
	print(s.combine(s2, np.add, fill_value=111)) # combine 方法
	print("--------------------------------------------------")
	print("Index")
	idx = s.index
	for cls in idx.__class__.mro():
		print(cls)
	print(idx.values)
	print("Index 可以当作一维数组，支持所有的数组下标操作")
	print(idx[1::2])
	print(idx[[1, 3]])
	print(idx[idx > 'c'])
	print("c at", idx.get_loc("c")) # 获得单个值value的下标
	print("a, c, z at", idx.get_indexer(["a", "d", "z"])) # 获得一组值values的下标，当值不存在时，得到-1
	print("Index 对象的字典功能由其中的 Engine 对象提供")
	e = s.index._engine
	print("a at", e.get_loc("a"))
	print("a, d, e, z at", e.get_indexer(np.array(["a", "d", "e", "z"], "O")))
	print("Engine 对象的字典功能由 mapping (hashTable) 提供")
	ht = e.mapping
	print("Hash Table:", ht)
	print("d at", ht.get_item("d"))
	print(ht.lookup(np.array(["a", "d", "e", "z"], "O")))

print("值不唯一的 Index")
N = 10000
uniqueKeys = np.array(list(set(pd.core.common.rands(5) for i in range(N))), 'O') # 值唯一时
dupKeys = uniqueKeys.copy()
dupKeys[-1] = dupKeys[0] # 值不唯一，无序
sortedKeys = np.sort(dupKeys) # 值不唯一，有序
uniqueIndex = pd.Index(uniqueKeys)
sortedIndex = pd.Index(sortedKeys)
dupIndex = pd.Index(dupKeys)
toSearch = uniqueKeys[N-2]
from itertools import product
def dataFrameFunc(func, indices, cols):
	return pd.DataFrame([[func(index, col) for col in cols] for index in indices], index=indices, columns=cols)
predicates = ["is_unique", "is_monotonic"]
index = ["unique_index", "sorted_index", "duplicate_index"]
dataFrameFunc(lambda idx, pred: getattr(globals()[idx], pred), index, predicates)
print(uniqueIndex.get_loc(uniqueKeys[0]))
print(sortedIndex.get_loc(uniqueKeys[0]))
print(dupIndex.get_loc(uniqueKeys[0]))
