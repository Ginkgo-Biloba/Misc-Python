# coding = utf_8
# 一个HTML文件，找出里面的链接。

from html.parser import HTMLParser
import urllib

class MyParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links = list()
	
	def handle_starttag(self, tag, attrs):
		# print("遇到标签", tag)
		if (tag == "a"):
			if (len(attrs) == 0):
				pass
			else:
				for (variable, value)  in attrs:
						if variable == "href":
							self.links.append(value)

	def close(self):
		self.links.clear()
		HTMLParser.close(self)

if __name__ == "__main__":
	with open('Python 练习册.htm', 'r', encoding="utf_8") as html:
		parser = MyParser()
		parser.feed(html.read())
		print('\t'.join(parser.links))
		parser.close()
