# coding = utf-8
"""
数字路线迷宫

按照下面的规则，找到从开始方格（红色）到目标方格（绿色）的路径。
	同一个方格不能经过两次。
	行走方向只能为横竖方向，斜对角方向不能行走。
	上方和右方的数字表示那一行或者列中，所经过的方格的个数。

下图是一个例子，左图为迷宫，右图为解。
从解可以看出，每一行所经过的方格数等于右侧对应的数字，而每一列所经过的方格数等于上方对应的数字。

解这种题目最简单的方法就是回溯法，回溯法最简单的实现就是用递归。
http://blog.chinaunix.net/uid-23100982-id-3080999.html
"""

class Maze(object):
	def __init__(self, tx, ty, n):
		self.tx = tx
		self.ty = ty
		self.maze = set() # 记录方格
		self.sx = [0] * n # 记录某行所经过的方格数
		self.sy = [0] * n # 记录某列所经过的方格数
		self.n = n

	def add(self, pos):
		self.maze.add(pos)
		self.sx[pos[0]] += 1
		self.sy[pos[1]] += 1

	def remove(self, pos):
		self.maze.remove(pos)
		self.sx[pos[0]] -= 1
		self.sy[pos[1]] -= 1

	def check(self, pos):
		(x, y) = pos
		(sx, sy) = (self.sx, self.sy)
		(tx, ty) = (self.tx, self.ty)
		if (sx[x] > tx[x]) or (sy[y] > ty[y]):
			return False # 剪枝 (1)
		if (sx[x] == tx[x]):
			for i in range(x):
				if (sx[i] != tx[i]): return False # 剪枝 (2)
		if (sy[y] == ty[y]):
			for i in range(y):
				if (sy[i] != ty[i]): return False
		return True
 
	def printOut(self):
		outs = "  ".join(str(v) for v in self.tx)
		outs += "\n"
		for i in range(self.n):
			for j in range(self.n):
				if (j, i) in self.maze: outs += "*" # 路径
				else: outs += " " # 非路径
				outs += "  "
			outs += str(self.ty[i])
			outs += "\n"
		print(outs)
		
	def nearPos(self, pos):
		(x, y) = pos
		if (x - 1 >= 0): yield (x - 1, y)
		if (x + 1 <= self.n - 1): yield (x + 1, y)
		if (y - 1 >= 0): yield (x, y - 1)
		if (y + 1 <= self.n - 1): yield (x, y + 1)

	def solve(self, startPos, endPos):
		stt = time.clock()
		self.add(startPos)
		if self.check(startPos):
			if (startPos == endPos):
				self.printOut()
				stt = time.clock() - stt
				print (stt, "秒")
				return
			for npos in self.nearPos(startPos):
				if npos not in self.maze:
					self.solve(npos, endPos)
		self.remove(startPos)

"""
剪枝：由于入口在左上，而出口在右下，因此一旦某一行或者列的方格数等于了规则所给出的方格数，那么它左边的列或者上面的行就必须也符合规定的数目。因为如果要走回的话，那么就必须再经过一次已经当前方格所在的行和列，这样就不能满足条件了。这也就是说，当走到某个方格时，那行的方格数已经等于了指定的值时，我们就不能再走那行上方的方格了。列方向上也是同样的道理。这个条件很关键，它能够裁剪掉大量的后续选路径，如果去除掉这个条件检测，那么等几个小时可能都出不来结果。
"""


if (__name__ == "__main__"):
	import time
	X = [4, 1, 9, 4, 6, 5, 3, 3, 4, 8]
	Y = [4, 6, 7, 4, 4, 3, 3, 7, 1, 8]
	maze = Maze(X, Y, 10)
	maze.solve((0,0), (9, 9))