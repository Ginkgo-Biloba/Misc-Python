# coding = utf-8
"""
各种加速
"""
from time import clock

#1: ~= 13.7s
#import math
#def calcRoot(nums):
#	rst = list()
#	for n in nums:
#		rst.append(math.sqrt(n))
#	return rst

#2: ~= 12.1s
#from math import sqrt # 消除属性访问
#def calcRoot(nums):
#	rst = list()
#	for n in nums:
#		rst.append(sqrt(n))
#	return rst

#3: ~= 9.3s
import math
def calcRoot(nums):
	rst = list()
	sqrt = math.sqrt # 局部变量
	rstApp = rst.append
	for n in nums:
		rstApp(sqrt(n))
	return rst

t1 = clock()
for n in range(500):
	r = calcRoot(range(100000))
t2 = clock()
print(t2 - t1, "s")
