# coding = utf-8

def applyAsync(func, args, *, callback):
	rst = func(*args)
	callback(rst)


def printRst(rst):
	print("Got:", rst)


def add(x, y):
	return (x + y)


# 接受单个返回值
applyAsync(add, (2, 3), callback=printRst)
applyAsync(add, ("Hello", ", World"), callback=printRst)


""" 1. 使用绑定方法来赛题一个简单的函数 """

class ResultHandler:
	def __init__(self):
		self.seq = 0

	def handler(self, rst):
		self.seq += 1
		print("[{}] Got: {}".format(self.seq, rst))


# 创建一个示例，然后绑定它的 handler() 方法作为回调函数
r = ResultHandler()
applyAsync(add, (2, 3), callback=r.handler)
applyAsync(add, ("Hello", ", World"), callback=r.handler)


""" 2. 作为类的替代，使用一个闭包捕获状态值 """

def makeHandler():
	seq = 0
	def handler(rst):
		nonlocal seq
		seq += 1
		print("[{}] Got (Closure): {}".format(seq, rst))
	return handler

handler = makeHandler()
applyAsync(add, (2, 3), callback=handler)
applyAsync(add, ("Hello", ", World"), callback=handler)


# 3. 使用协程

def makeCoroutine():
	seq = 0
	while True:
		rst = yield
		seq += 1
		print("[{}] Got (Corouutine): {}".format(seq, rst))

# 对于协程，使用 send() 方法作为回调函数
handler = makeCoroutine()
next(handler) # 前进到 yield
applyAsync(add, (2, 3), callback=handler.send)
applyAsync(add, ("Hello", ", World"), callback=handler.send)


















