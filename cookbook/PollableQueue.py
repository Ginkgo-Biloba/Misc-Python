# coding = utf-8
"""
多个线程队列轮询
Ref: http://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p13_polling_multiple_thread_queues.html
"""
import queue
import socket
import os

class PollableQueue(queue.Queue):
	def __init__(self):
		super().__init__()
		# 创建一对链接的套接口
		if os.name == "posix":
			self._putsocket, self._getsocket = socket.socketpair()
		else:
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server.bind(("127.0.0.1", 0))
			server.listen(1)
			self._putsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self._putsocket.connect(server.getsockname())
			(self._getsocket, _) = server.accept()
			server.close()

	def fileno(self):
		return self._getsocket.fileno()

	def put(self, item):
		super().put(item)
		self._putsocket.send(b'x')

	def get(self):
		self._getsocket.recv(1)
		return super().get()


# 例子
import select
import threading
import time

def consumer(queues):
	"""同时从多个队列中读取数据"""
	while True:
		(canRead, _, _) = select.select(queues, [], [])
		for r in canRead:
			item = r.get()
			print("Got:", item)

q1 = PollableQueue()
q2 = PollableQueue()
q3 = PollableQueue()
t = threading.Thread(target=consumer, args=([q1, q2, q3],))
t.daemon = True
t.start()
# 送数据到队列
q1.put(1)
q2.put(10)
q3.put("Hello")
q2.put(15)
# ...

