# coding = utf-8
"""
周期计时器，每当计时器超时的时候，其他线程都可以检测到
"""
import threading
import time

class PeriodicTimer:
	def __init__(self, interval):
		self._interval = interval
		self._flag = False;
		self._cv = threading.Condition()

	def run(self):
		"""运行计时器，在每个固定的间隔后通知等待的线程"""
		while True:
			time.sleep(self._interval)
			# 使用 with 语句，开始自动获得锁，结束自动释放
			with self._cv:
				self._flag = not self._flag
				self._cv.notify_all()

	def start(self):
		t = threading.Thread(target=self.run)
		t.daemon = True
		t.start()

	def waitTick(self):
		"""等待计时器消息"""
		with self._cv:
			lastFlag = self._flag
			while (lastFlag == self._flag):
				self._cv.wait()

# 用法示例
pTimer = PeriodicTimer(2)
pTimer.start()

# 两个与计时器同步的线程
def countDown(nTick):
	while(nTick > 0):
		pTimer.waitTick()
		print("T- Count", nTick)
		nTick -= 1

def countUp(nTick):
	n = 0;
	while (n < nTick):
		pTimer.waitTick()
		print("T+ Count", n)
		n += 1

threading.Thread(target=countDown, args=(10,)).start()
threading.Thread(target=countUp, args=(5,)).start()

