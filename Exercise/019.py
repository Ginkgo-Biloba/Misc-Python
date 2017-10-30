# coding: utf_8
"""
 将第 016 题中的 numbers.xls 文件中的内容写到 numbers.xml 文件中，如下所示：

<?xml version="1.0" encoding="UTF-8"?>
<root>
<numbers>
<!-- 
	数字信息
-->
[
	[1, 82, 65535],
	[20, 90, 13],
	[26, 809, 1024]
]
</numbers>
</root>
"""

from openpyxl import load_workbook
from lxml import etree

""" 读 xlsx """
wb = load_workbook("number.xlsx")
sheetName = "number"
if sheetName not in wb.get_sheet_names():
	print("没有工作表 number")
	exit(-1)
ws = wb[sheetName]
data = list()
for row in ws.rows:
	data.append([x.value for x in row])

""" 写 xml """
root = etree.Element("root");
# root_doc = etree.ElementTree(root)
citys = etree.SubElement(root, "citys")
citys.append(etree.Comment("数字信息"))
citys.text = str(data)
with open("city.xml", "w", encoding = "utf_8") as of:
	s = etree.tounicode(root, pretty_print=True)
	of.write(s)
	print(s)

