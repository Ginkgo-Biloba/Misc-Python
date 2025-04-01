#coding = utf-8

# 使用 csv 读取，这里，row 是一个列表
print("\n")
print("=" * 20, "Using csv", "=" * 20)

import csv
with open(r".\csvstocks.csv") as csvf:
	cf = csv.reader(csvf)
	headers = next(cf)
	print(headers)
	for row in cf:
		print(row)


# 使用命名元组，只有在列名是合法的 Python 标识符的时候才生效
print("\n")
print("=" * 20, "Using namedtuple", "=" * 20)

from collections import namedtuple
with open(r".\csvstocks.csv") as csvf:
	cf = csv.reader(csvf)
	headers = next(cf)
	RowTuple = namedtuple("RowTuple", headers)
	for r in cf:
		row = RowTuple(*r)
		print(row)


# 使用 csv 模块写文件，先创建一个 writer 对象
print("\n")
print("=" * 20, "Using csv to write", "=" * 20)
print(r"To see file .\csvstocks-w.csv")

headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
		('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
		('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
		]
with open(r".\csvstocks-w.csv", "w") as csvf:
	cf = csv.writer(csvf)
	cf.writerow(headers)
	cf.writerows(rows)


# 写入字典数据
print("\n")
print("=" * 20, "Using csv to write dict data", "=" * 20)
print(r"To see file .\csvstocks-dict.csv")

headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol': 'AA', 'Price': 39.48, 'Date': '6/11/2007', 'Time': '9:36am', 'Change': -0.18, 'Volume': 181800},
		{'Symbol': 'AIG', 'Price': 71.38, 'Date': '6/11/2007', 'Time': '9:36am', 'Change': -0.15, 'Volume': 195500},
		{'Symbol': 'AXP', 'Price': 62.58, 'Date': '6/11/2007', 'Time': '9:36am', 'Change': -0.46, 'Volume': 935000},
		]
with open(r".\csvstocks-dict.csv", "w") as csvf:
	cf = csv.DictWriter(csvf, headers)
	cf.writeheader()
	cf.writerows(rows)
