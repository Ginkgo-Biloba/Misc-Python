# coding: utf_8
# 将 0001 题生成的 200 个激活码（或者优惠券）保存到 MySQL (SQLite) 关系型数据库中。

import string, random, sqlite3, os
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
dbf = r"\002.db"
if os.path.exists(dbf):
	os.remove(dbf)
cx = sqlite3.connect(dbf)
cx.execute("create table ics (id INT primary key, ic varchar(25) UNIQUE)")
x = 0
while (x < 200):
	cx.execute("insert into ics values(?, ?)", (x+1, ics[x]))
	x += 1
cx.commit()
cx.close()

# 显示
cx = sqlite3.connect(dbf)
rs = cx.execute("select id, ic from ics where id < 21")
print("id\tic")
x = 0
for r in rs:
	x += 1 
	print ("{id} -> {ic}".format(id= r[0], ic = r[1]), end='\t')
	if not(x % 4):
		print ('\n')
cx.close()
