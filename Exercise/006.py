# coding = utf_8
# 你有一个目录，放了你一个月的日记，都是 txt，为了避免分词的问题，假设内容都是英文，请统计出你认为每篇日记最重要的词。

from collections import Counter
import re

c = Counter()
word = re.compile(r'[\w]+')
with open('Flipped.txt', mode = 'r', encoding = 'utf_8_sig') as f:
	s = f.read()
	l = re.findall(word, s)
	c.update(l)

print (c.most_common(1))
