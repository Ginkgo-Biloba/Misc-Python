# coding: utf_8
# 用 Python 写一个爬图片的程序，爬 链接里的图片 :-)


def imgGet1(pageURL):
	import requests, os
	from lxml import html
	imgDir = "img"
	if os.path.exists(imgDir) and os.path.isfile(imgDir):
		os.remove(imgDir)
		os.mkdir(imgDir)
	page = requests.get(pageURL)
	doc = html.fromstring(page.text)
	for (idx, el) in enumerate(doc.cssselect("img.BDE_Image")):
		with open("img" + os.sep + "{:03d}".format(idx), "wb") as f:
			f.write(requests.get(el.attrib["src"]).content)

def imgGet2(pageURL):
	import re, os
	from urllib import request, parse
	imgDir = "img"
	values = {"word": "清新美女", "width": 800, "height": 600}
	values = parse.urlencode(values)
	data = None
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
	req = request.Request(pageURL+values, data, headers)
	page = request.urlopen(req)
	html = page.read().decode("utf_8")
	imgList = re.findall(r'"objURL":"([^\s]+?\.jpg)"', html)
	i = 0
	for imgURL in imgList:
		req = request.Request(imgURL, data, headers)
		try:
			img = request.urlopen(req).read()
			f = open(imgDir + os.sep + "{:03d}.jpg".format(i), "wb")
			f.write(img)
			i += 1
		except:
			pass
	with open(imgDir + os.sep + "page.html", "wt") as hf:
		hf.write(html)

if __name__ == "__main__":
	pageURL = "https://image.baidu.com/search/index?tn=baiduimage&"
	# pageURL = r"http://tieba.baidu.com/p/2166231880"
	# imgGet1(pageURL)
	imgGet2(pageURL)
	
