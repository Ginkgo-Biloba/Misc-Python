# coding = utf-8
"""
Actor 任务？
Ref: http://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p10_defining_an_actor_task.html
"""
from queue import Queue
from threading import Thread, Event
import time

# 用来停止
class ActorExit(Exception):
	pass

class Actor:
	def __init__(self):
		self._mailbox = Queue()

	def send(self, msg):
		# 发送一条消息给执行器
		self._mailbox.put(msg)

	def receive(self):
		# 从执行器接收一条消息
		msg = self._mailbox.get()
		if msg is ActorExit:
			raise ActorExit()
		return msg

	def close(self):
		self.send(ActorExit)

	def run(self):
		# 在这里写下具体干的活
		while True:
			msg = self.receive()

	def join(self):
		self._terminated.wait()

	def _bootstrap(self):
		try:
			self.run()
		except ActorExit:
			pass
		finally:
			self._terminated.set()

	def start(self):
		self._terminated = Event()
		t = Thread(target=self._bootstrap)
		t.daemon = True # True 的话要手动调用 join
		t.start()


# 示例，重写 run
class PrintActor(Actor):
	def run(self):
		while True:
			msg = self.receive()
			time.sleep(1)
			print("Got", msg)

# 用法
p = PrintActor()
p.start()
p.send("Hello")
p.send("世界")
p.close()
p.join()


# 下面的 actor 允许在一个工作者中运行任意的函数， 并且通过一个特殊的 Result 对象返回结果
class Result:
	def __init__(self):
		self._evt = Event()
		self._rst = None

	def setResult(self, value):
		self._rst = value
		self._evt.set()

	def getResult(self):
		self._evt.wait()
		return self._rst

class Worker(Actor):
	def submit(self, func, *args, **kw):
		r = Result()
		self.send((func, args, kw, r))
		return r # 在此阻塞？

	def run(self):
		while True:
			func, args, kw, r = self.receive()
			r.setResult(func(*args, **kw))

# 用法
wk = Worker()
wk.start()
r = wk.submit(pow, 2, 4)
print(r.getResult())
