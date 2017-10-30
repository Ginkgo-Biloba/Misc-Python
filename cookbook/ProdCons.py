# coding = utf-8
"""
简单的生产者消费者示例
Ref: http://blog.jobbole.com/52412/
Queue 自带锁，这里抄写 list 的例子在于学习条件变量和通知
"""

from threading import Thread, Condition
import time
import random

queue = list()
MAX_NUM = 10
cond = Condition()

class ProducerThread(Thread):
	def run(self):
		nums = list(range(5))
		global queue
		while True:
			cond.acquire() # 获得锁
			if len(queue) >= MAX_NUM:
				print("队列满，生产者开始等待")
				cond.wait() # 会自动释放锁
				print("队列有空闲，消费者通知生产者")
			num = random.choice(nums)
			queue.append(num)
			print("生产", num)
			cond.notify() # 通知消费者，消费者自动尝试调用 acquire() 获得锁
			cond.release() # 释放锁
			time.sleep(random.random())

class ConsumerThread(Thread):
	def run(self):
		global queue
		while True:
			cond.acquire()
			if len(queue) == 0:
				print("队列为空，等待生产者")
				cond.wait()
				print("生产者往队列里添加了东西并通知")
			num = queue.pop(0)
			print("消费", num)
			cond.notify()
			cond.release()
			time.sleep(random.random())

ProducerThread().start()
ConsumerThread().start()
