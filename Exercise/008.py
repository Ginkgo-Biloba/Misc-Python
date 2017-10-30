# coding = utf-8
# 一个HTML文件，找出里面的正文

from html.parser import HTMLParser
import os

def getFiles(root = os.curdir):
	root += os.sep
	for path, dirs, files in os.walk(root):
		for fileName in files:
			yield path, fileName

class myParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		tagStack.append(tag)

	def handle_endtag(self, tag, tag_flag = True):
		tagStack.pop()

	def handle_data(self, data):
		if data.strip() and ("body" in tagStack):
			bds.append(data.strip())

if __name__ == "__main__":
	root = os.curdir
	paths = getFiles(root)
	htmlExts = (".html", ".htm")
	tagStack = list()
	bds = list()
	parser = myParser()
	
	with open('Python 练习册.htm', 'r', encoding="utf_8") as file:
		parser.feed(file.read())

	print("".join(bds))
