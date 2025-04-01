# coding = utf-8
"""
导入 sample
Ref: http://python3-cookbook.readthedocs.io/zh_CN/latest/c15/p01_access_ccode_using_ctypes.html
"""
import ctypes
import ntpath

dllFile = ntpath.join(ntpath.abspath("."), r"..\x64\Release\CExt.dll")
dllFile = ntpath.normpath(dllFile)
dllSample = ctypes.cdll.LoadLibrary(dllFile)

# int gcd(int, int) ==============================
gcd = dllSample.gcd
gcd.argtypes = (ctypes.c_int, ctypes.c_int)
gcd.restype = ctypes.c_int

# int inMandelbrot(double, double, int) ==============================
inMandelbrot = dllSample.inMandelbrot
inMandelbrot.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_int)
inMandelbrot.restype = ctypes.c_int

# int divide(int, int, int*) ==============================
_divide = dllSample.divide
_divide.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
_divide.restype = ctypes.c_int

def divide(x, y):
	reminder = ctypes.c_int()
	quotient = _divide(x, y, reminder)
	return (quotient, reminder.value)

# double avg(double*, int) ==============================
# 定义一个 double* 类型
class DoubleArrayType:
	# 名字不能改
	def from_param(self, param):
		typeName = type(param).__name__
		if hasattr(self, "from_"+typeName):
			return getattr(self, "from_"+typeName)(param)
		elif isinstance(param, ctypes.Array):
			return param
		else:
			raise TypeError("不能转换 {s}".format(typeName))

	# array.array 情形
	def from_array(self, param):
		if (param.typecode != 'd'):
			raise TypeError("必须是双精度浮点数组")
		(ptr, _) = param.buffer_info()
		return ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double))

	# list 或 tuple 情形
	def from_list(self, param):
		value = ((ctypes.c_double) * len(param))(*param)
		return value

	from_tuple = from_list

	# numpy.array 情形
	def from_ndarray(self, param):
		return param.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

DoubleArray = DoubleArrayType()
_avg = dllSample.avg
_avg.argtypes = (DoubleArray, ctypes.c_int)
_avg.restype = ctypes.c_double

def avg(values):
	 return _avg(values, len(values))

# Point 结构体 ==============================
class Point(ctypes.Structure):
	_fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

# double distance(Point*, Point*) ==============================
distance = dllSample.distance
distance.argtypes = (ctypes.POINTER(Point), ctypes.POINTER(Point))
distance.restype = ctypes.c_double


# 直接在这里使用函数，或者在其他 .py 文件中 import sample
# 见 callcfuncUsage.py
