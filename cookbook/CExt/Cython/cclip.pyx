# coding = utf-8
# cclip.pyx (Cython)
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef clip(double[:] a, double minVal, double maxVal, double[:] out):
	""" 截断值 """
	if (minVal > maxVal):
		raise ValueError("minVal 不能大于 maxVal")
	if (a.shape[0] != out.shape[0]):
		raise ValueError("输入输出数组尺寸不同")
	for i in range(a.shape[0]):
		out[i] = (a[i] if a[i] < maxVal else maxVal) if a[i] > minVal else minVal
		# 多重 if 稍微慢点儿，鬼知道为啥
		# if (a[i] < minVal): out[i] = minVal
		# elif (a[i] > maxVal): out[i] = maxVal
		# else: out[i] = a[i]

# 命令行下使用 python .\setup.py build_ext --inplace 编译
