# coding = utf-8
"""
@Ref: http://python3-cookbook.readthedocs.io/zh_CN/latest/c07/p11_inline_callback_functions.html
"""

def applyAsync(func, args, *, callback):
	rst = func(*args)
	callback(rst)


"""
这一小节的核心就在 inline_async() 装饰器函数中了。
关键点就是，装饰器会逐步遍历生成器函数的所有 yield 语句，每一次一个。
为了这样做，刚开始的时候创建了一个 result 队列并向里面放入一个 None 值。
然后开始一个循环操作，从队列中取出结果值并发送给生成器，它会持续到下一个 yield 语句， 在这里一个 Async 的实例被接受到。
然后循环开始检查函数和参数，并开始进行异步计算 apply_async() 。
然而，这个计算有个最诡异部分是它并没有使用一个普通的回调函数，而是用队列的 put() 方法来回调。
这时候，是时候详细解释下到底发生了什么了。主循环立即返回顶部并在队列上执行 get() 操作。
如果数据存在，它一定是 put() 回调存放的结果。如果没有数据，那么先暂停操作并等待结果的到来。
这个具体怎样实现是由 apply_async() 函数来决定的。
"""

from queue import Queue
from functools import wraps

class Async:
	def __init__(self, func, args):
		self.func = func
		self.args = args


def inlinedAsync(func):
	@wraps(func)
	def wrapper(*args):
		f = func(*args)
		rstQueue = Queue()
		rstQueue.put(None)
		while True:
			rst = rstQueue.get()
			try:
				a = f.send(rst)
				applyAsync(a.func, a.args, callback=rstQueue.put)
			except StopIteration:
				break
	return wrapper


""" 使用 yield 语句内联回调函数 """

def add(x, y):
	return (x + y)

@inlinedAsync
def test():
	r = yield Async(add, (2, 3))
	print(r)
	r = yield Async(add, ("Hello", ", World"))
	print(r)
	for n in range(10):
		r = yield Async(add, (n, 1.5*n))
		print(r)
	print("Goodbye")

test()
