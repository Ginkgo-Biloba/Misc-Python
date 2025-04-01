# coding = utf-8
"""

"""

from functools import wraps, partial
import logging

# 装饰器，添加一个函数作为对象的属性
def attachWrapper(obj, func=None):
	if func is None:
		return partial(attachWrapper, obj)
	setattr(obj, func.__name__, func)
	return func

def logged(level, name=None, msg=None):
	"""
	给函数添加日志。
	logging 等级，名字是记录器的名字，信息是日志信息
	如果名字和信息未指定，它们默认是函数的模块和名字
	"""
	def decorate(func):
		logname = name if name else func.__name__
		log = logging.getLogger(logname)
		logmsg = msg if msg else func.__name__

		@wraps(func)
		def wrapper(*args, **kw):
			log.log(level, logmsg)
			return func(*args, **kw)

		# 设置日志级别
		@attachWrapper(wrapper)
		def setLevel(newlevel):
			nonlocal level
			level = newlevel

		# 设置日志附加信息
		@attachWrapper(wrapper)
		def setMsg(newmsg):
			nonlocal logmsg
			logmsg = newmsg

		return wrapper
	return decorate


# 示例函数
@logged(logging.DEBUG)
def add(x, y):
	return (x + y)

@logged(logging.CRITICAL, "example")
def spam():
	print("Spam!")

# 使用
logging.basicConfig(level=logging.DEBUG)
add(2, 3)
# 改变日志信息
add.setMsg('Add called')
add(3, 4)
# 改变日志级别
add.setLevel(logging.WARNING)
add(5, 6)

