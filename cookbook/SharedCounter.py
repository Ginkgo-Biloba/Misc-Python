# coding = utf-8
"""
多个线程共用的计数器对象
"""
import threading

class SharedCounter:
	def __init__(self, initVal):
		self._value = initVal # 初始值
		self._lock = threading.Lock()

	def inc(self, delta=1):
		# Lock 对象和 with 语句块一起使用可以保证互斥执行
		# 每次只有一个线程可以执行 with 语句包含的代码块
		# with 语句会在这个代码块执行前自动获取锁，在执行结束后自动释放锁
		with self._lock:
			self._value += delta

	def dec(self, delta=1):
		with self._lock:
			self._value -= delta

