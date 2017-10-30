# coding: utf_8
# 将 0001 题生成的 200 个激活码（或者优惠券）保存到 Redis 非关系型数据库中。 

import string, random, os, redis
ics = []
x = 0
ps = string.ascii_letters + string.digits + string.punctuation

# 200 个激活码 | 每个 24 位
while (x < 200):
	ic = ''
	for i in range(24):
		ic += random.choice(ps)
	if ic not in ics:
		ics.append(ic)
		x += 1

# 存入数据库
rds = redis.StrictRedis(host='localhost', port = 6739, db = 0)
x = 0
for ic in ics:
	x += 1
	rds.set(x, ic)
rds.save()

# 显示 20 个
rds = redis.StrictRedis(host='localhost', port = 6739, db = 0)
rs = cx.execute("select id, ic from ics where id < 21")
print("id\tic")
x = 0
for r in rs:
	x += 1 
	print(str(rds.get(x), encoding = 'utf-8'))
	if not(x % 4):
		print ('\n')

