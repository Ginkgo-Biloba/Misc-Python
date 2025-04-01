# coding: utf_8
"""
将第 015 题中的 city.xls 文件中的内容写到 city.xml 文件中，如下所示：

<?xmlversion="1.0" encoding="UTF-8"?>
<root>
<citys>
<!-- 
    城市信息
-->
{
    "1" : "上海",
    "2" : "北京",
    "3" : "成都"
}
</citys>
</root>
"""

from openpyxl import load_workbook
from lxml import etree

""" 读 xlsx """
wb = load_workbook("city.xlsx")
sheetName = "city"
if sheetName not in wb.get_sheet_names():
	print("没有工作表 number")
	exit(-1)
ws = wb[sheetName]
data = dict()
for row in ws.rows:
	k = row[0].value
	v = row[1].value
	data[k] = v

""" 写 xml """
root = etree.Element("root");
# root_doc = etree.ElementTree(root)
citys = etree.SubElement(root, "citys")
citys.append(etree.Comment("城市信息"))
citys.text = str(data)
with open("city.xml", "w", encoding = "utf_8") as of:
	of.write(etree.tounicode(root, pretty_print=True))
	print(data)
