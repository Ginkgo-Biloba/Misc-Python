# coding=utf_8

a = 4.2
b = 2.1
print (a + b)
print((a + b) == 6.3)

from decimal import Decimal
da = Decimal("4.2")
db = Decimal("2.1")
print(da + db)
print((da + db) == Decimal("6.3"))

# 控制精度格式
from decimal import localcontext
dc = Decimal("1.3")
dd = Decimal("1.7")
print(dc / dd)
with localcontext() as ctx:
	ctx.prec = 70
	print(dc / dd)

# 浮点运算
nums = [1.23e+18, 1.0, -1.23e+18]
print(sum(nums))
import math
print(math.fsum(nums))

# 分数
from fractions import Fraction
fa = Fraction(5, 4)
fb = Fraction(7, 16)
print(fa + fb)
print(fa * fb)
# 获得分子分母
fc = fa * fb
print(fc.numerator, ", ", fc.denominator)
# 转换为 float
print(float(fc))
# 限制分母大小
print(fc.limit_denominator(8))
#转换浮点数到分数
fx = 3.75
fy = Fraction(*fx.as_integer_ratio())
print(fy)
