# coding = utf-8
"""
矩形数字谜题
谜题如图所示，每个数字 N 表示一个矩形区域 R， R 所包含的小方格数正好为 N。要求计算出所有数字对应的矩形区域，使得它们之间不互相覆盖，并且正好包含所有的方块。
http://blog.chinaunix.net/uid-23100982-id-3082755.html
"""


from copy import deepcopy

WIDTH = 12
HEIGHT = 12
# blocks 列表是一个 3 个元素的的元组：横坐标、纵坐标、此坐标上的数字。
blocks = [
(0, 8, 10),
(8, 4, 9),
(7, 0, 8),
(3, 1, 8),
(5, 6, 8),
(7, 7, 8),
(8, 9, 5),
(11,9, 6),
(4, 10,6),
(3, 11,6),
(9, 11,4),
(9,1, 6),
(0, 3, 6),
(6, 3, 6),
(3, 4, 6),
(11,4, 6),
(0, 6, 6),
(10,6, 6),
(2, 7, 6),
(9, 8, 6),
(2, 9, 6),
(6, 9, 6),
]

# possible_block2() 计算出所有包含坐标 (x, y)、长宽为 (w, h) 的矩形区域。它返回的是 4 个元素的元组，其意义分别为（矩形区域的左上点横坐标， 矩形区域的左上点纵坐标， 矩形区域的宽， 矩形区域的高）
def possible_block2(x, y, w, h):
	for i in range(-w+1, 1):
		for j in range(-h+1, 1):
			if (x + i >= 0 and 
				y + j >= 0 and 
				x + i + w <= WIDTH and 
				y + j + h <= HEIGHT):
				yield (x + i, y + j, w, h)

				
# possible_block() 计算出坐标为 (x, y) 的数字 c 所对应的所有可能的矩形区域
def possible_block(x, y, c):
	for i in range(1, c+1):
		if c%i == 0: # 高为整数
			for p in possible_block2(x, y, i, c//i):
				yield p

				
# make_init_status() 通过收集所有的数字对应的所有可能的矩形区域，返回本问题的初始解空间 status。status[i]为 blocks[i] 对应的所有可能的解
def make_init_status(blocks):
	status = []
	for x, y, b in blocks:
		status.append( list(possible_block(x,y,b)) )
	return status

	
"""
传播和分配的基本思想是通过传播操作，尽量缩小解空间的取值范围，在无法缩小的情况下，进行解空间的分配操作，也就是把解空间分解成两个子空间，然后分别对其进行传播和分配操作，直到找到解为止。

我们先来看看传播操作。对于本问题，传播操作就是剔除掉所有相互重叠的矩形。具体地说，就是当某个矩形R与某个数字N对应的所有的矩形都重叠的时候，从解空间中删除矩形R，下文称这种矩形为无效矩形。下面是这部分代码的说明。
"""

# rectangle_overlap() 判断矩形 rect1 和矩形 rect2 是否有重叠部分，有则返回 True，无则返回 False
def rectangle_overlap(rect1, rect2):
	x1, y1, w1, h1 = rect1
	x2, y2, w2, h2 = rect2
	if y1 + h1 - 1 < y2: return False
	if y1 > y2 + h2 - 1: return False
	if x1 + w1 - 1 < x2: return False
	if x1 > x2 + w2 - 1: return False
	return True
	
	
# rectangle_overlap_all() 判断矩形 rect 和矩形列表 rectlist 中的所有矩形是否都重叠，都重叠时返回 True
def rectangle_overlap_all(rect, rectlist):
	for rect1 in rectlist:
		if not rectangle_overlap(rect, rect1):
			return False
	return True

	
# remove_overlap_rectangles() 从矩形列表 rectlist1 中删除掉与矩形列表 rectlist2 中所有矩形重叠的矩形，如果删除了某个矩形的话，返回 True，否则返回 False
def remove_overlap_rectangles(rectlist1, rectlist2):
	flag = False
	for i, x in enumerate(rectlist1):
		if rectangle_overlap_all(x, rectlist2):
			rectlist1[i] = 0
			flag = True
	while 0 in rectlist1:
		rectlist1.remove(0)
	return flag

	
# del_impossible_choice() 完成对解空间 status 的传播操作，从解空间 status 中删除掉所有无效矩形，直到找不到更多的无效矩形。
# tocheck 是一个待检查的集合，它的元素为一个 2 元元组 (x, y)，表示要删除 status[x] 中所有与 status[y] 重叠的矩形。当 remove_overlap_rectangles() 返回Ture 时，表示 status[x] 发生了变化，因此需要重新检查 (i, x)，i 为除了 x 之外的所有下标。
# 当 tocheck 为空时，则表示无法继续进行传播操作了。此时的解空间的大小将明显的减少。
# 例如本问题的初始解空间中共有个 345 矩形元素，经过一次传播操作之后剩下 156 个矩形元素
def del_impossible_choice(status):
	tocheck = set()
	for i in range(len(status)):
		for j in range(len(status)):
			if i!=j: tocheck.add((i,j))
	
	while len(tocheck) > 0:
		x, y = tocheck.pop()
		r = remove_overlap_rectangles(status[x], status[y])
		if r:
			for i in range(len(status)):
				if i!=x:
					tocheck.add((i,x))


"""
当传播操作无法继续时，进行分配操作，通过分配算法将当前的解空间分解为两个子解空间，然后再递归执行传播分配操作。

分配的算法有很多种，这里采用的具体算法如下：
	当某个数所对应的矩形列表长度为 1 时表示这个数所对应的矩形已经有解。
	当长度大于 1 时表示还多个候选解，找到候选解最少的下标 index，然后把这组候选解 [x0, x1, x2，...，xn] 分为两部分：[x0], [x1, x2, ... , xn]。

程序中的 status1 和 status2 是分解后的子解空间，显然 status1 和 status2 的集合就是 status
"""

# divide_status() 对解空间 status 进行分配，得到两个子解空间 status1 和 status2
def divide_status(status):
	# 发现最短的选择
	m = 100
	index = -1
	for i, x in enumerate(status):
		if len(x) > 1 and m > len(x):
			m = len(x)
			index = i
	
	status1 = deepcopy(status)
	status2 = deepcopy(status)
	status1[index] = [status[index][0]]
	status2[index] = status[index][1:]
	return status1, status2
	

# is_solved_status() 判断 status 是否是最终解
# 当解空间status中所有的候选矩形数都为1时，则找到了最终解
def is_solved_status(status):
	for x in status:
		if len(x)!= 1:
			return False
	return True


# is_impossible_status() 判断 status 是否是无解解空间
# 当解空间 status 中某组候选矩形数为 0 时，表示此空间无解
def is_impossible_status(status):
	for x in status:
		if len(x) == 0:
			return True
	return False


# solve_puzzle() 递归调用自己来实现传播分配操作，直到找到解
def solve_puzzle(status):
	del_impossible_choice(status) # 分配操作，尽可能地缩小解空间
	if is_solved_status(status):  # 判断解空间是否为最终解
		print_solve_status(status)
		return
	if is_impossible_status(status):  # 判断解空间是否无解
		return
	# 对解空间status进行分配操作，得到子解空间status1和status2    
	status1, status2 = divide_status(status)
	solve_puzzle(status1) # 递归调用 solvePuzzle 搜索解空间 status1 中的解
	solve_puzzle(status2) # 递归调用 solvePuzzle 搜索解空间 status2 中的解

	
def print_solve_status(status):
	chars = "abcdefghijklmnopqrstuvwxyz"
	board = []
	for i in range(HEIGHT):
		board.append([" "]*WIDTH)
	for cnt, rect in enumerate(status):
		x, y, w, h = rect[0]
		for i in range(x, x+w):
			for j in range(y, y+h):
				board[j][i] = chars[cnt]
	for line in board:
		print (" ".join(line))


status = make_init_status(blocks)
solve_puzzle(status)
