# coding: utf_8
# 纯文本文件 number.txt，请将上述内容写到 number.xls 文件中

import json, os
from openpyxl import Workbook

def txt2xlsx(txtFile, xlsxFile = None):
	y = -1 # 成功插入数据的行数
	if os.path.exists(txtFile):
		y = 0
	else:
		return y
	with open(txtFile, "rt", encoding="utf_8") as txt:
		data = json.load(txt)
		print (data)
		xlsx = Workbook()
		sheet1 = xlsx.active
		sheet1.title = os.path.splitext(txtFile)[0]
		for i in data:
			sheet1.append(i)
			y += 1
		if xlsxFile == None:
			xlsxFile = sheet1.title + ".xlsx"
		xlsx.save(xlsxFile)
	return y

if __name__ == "__main__":
	y = txt2xlsx("number.txt")
	print(y, "行数据")
