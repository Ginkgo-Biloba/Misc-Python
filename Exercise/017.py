# coding: utf_8
"""
将第 014 题中的 student.xls 文件中的内容写到 student.xml 文件中，如下所示：
<?xml version="1.0" encoding="UTF-8"?>
<root>
<students>
<!--
	学生信息表
	"id" : [名字, 数学, 语文, 英文]
-->
{
	"1" : ["张三", 150, 120, 100],
	"2" : ["李四", 90, 99, 95],
	"3" : ["王五", 60, 66, 68]
}
</students>
</root>
"""

import xml.dom.minidom as MD
from openpyxl import load_workbook

""" 读 xlsx """
wb = load_workbook("student.xlsx")
sheetName = "student"
if sheetName not in wb.get_sheet_names():
	print("没有工作表 student")
	exit(-1)
ws = wb[sheetName]
data = dict()
for row in ws.rows:
	k = row[0].value
	v = [x.value for x in row[1:]]
	data[k] = v

"""写 xml """
doc = MD.Document()
root = doc.createElement("root")
doc.appendChild(root)
stus = doc.createElement("students")
root.appendChild(stus)
stus.appendChild(doc.createComment("\n\
\t\t学生信息表\n\
\t\t\"id\" : [名字, 数学, 语文, 英语]\n\
"))
stu = "{"
for i in range(0, len(data)):
	stu += "\n\t\t\"{}\" : ".format(i) + str(data[i+1]) +","
stu += "\n\t\t}"
content = doc.createTextNode(stu)
stus.appendChild(content)
with open("student.xml", "w", encoding = "utf-8") as f:
	doc.writexml(f, indent="", addindent="\t", newl="\n", encoding="utf-8")
	# 这个 encoding 就是往文件头写一下，对实际编码没半点儿影响
