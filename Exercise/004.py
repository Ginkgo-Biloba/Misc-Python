# coding: utf_8
# 任一个英文的纯文本文件，统计其中的单词出现的个数。

import re

file = r".vscode/launch.json"
word1 = re.compile(r"[\w\-\_\.\']+")
word2 = re.compile(r"[\w]+")
with open(file, 'r') as f:
	c1 = re.findall(word1, f.read())
	f.seek(0, 0)
	c2 = re.findall(word2, f.read())

print(len(c1), len(c2))

# c2 和 notpda++ 里的一样 ……