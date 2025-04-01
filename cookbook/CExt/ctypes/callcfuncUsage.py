# coding = utf-8
"""
调用 callcfunc 示例
"""
import callcfunc
import numpy

print(callcfunc.gcd(35, 42)) #7

print(callcfunc.inMandelbrot(-1.0, 0.2, 500)) # 1
print(callcfunc.inMandelbrot(-2.0, 1.0, 500)) # 0 

print(callcfunc.divide(42, 8)) # (5, 2) 

print(callcfunc.avg([1, 2, 3])) # 2.0 
print(callcfunc.avg(numpy.linspace(1, 10, 10, endpoint=True, dtype=numpy.float))) # 5.5

p1 = callcfunc.Point(1, 2)
p2 = callcfunc.Point(4, 5)
print(callcfunc.distance(p1, p2)) # 3 \times \sqrt(2) ~= 4.243

print(callcfunc)
