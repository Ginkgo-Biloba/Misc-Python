# coding = utf_8
# 使用 Python 生成类似于下图中的字母验证码图片

import string, random
from PIL import Image, ImageFilter, ImageDraw, ImageFont

def genStr(length = 4):
	ss = string.ascii_uppercase + string.digits
	s = str()
	for i in range(length):
		s += random.choice(ss)
	return s

def genVrfImg(strs, size = (300, 70), mode = 'RGB', bgColor = 0xFFFFFF, fgColor = 0x0, fontSize = 40, fontFile = "seguisym.ttf", drawLine = True, nLine = 5, drawPoint = True, pointRatio = 70):
	w, h = size
	im = Image.new(mode, size, bgColor)
	dr = ImageDraw.Draw(im)
	if drawLine:
		for i in range(nLine):
			begin = (random.randint(0, w), random.randint(0, h))
			end = (random.randint(0, w), random.randint(0, h))
			lColor = random.randint(0, 0xFFFFFF)
			dr.line((begin, end), fill = lColor, width = 4)
	if drawPoint:
		for x in range(w):
			for y in range(h):
				prob = random.randint(0, 100) # 概率
				if prob > pointRatio:
					continue
				lColor = random.randint(0, 0xFFFFFF)
				dr.point((x, y), fill = lColor)
	font = ImageFont.truetype(font = fontFile, size = fontSize)
	fontW, fontH = font.getsize(text = strs)
	dr.text( (random.randint(0, w - fontW), random.randint(0, h - fontH)), text = strs, fill = fgColor, font = font)
	# params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 1 - float(random.randint(1, 10)) / 100, 0, 0, 0, 1 -  float(random.randint(1, 20)) / 100]
	# im = im.transform(size, Image.PERSPECTIVE, data = params, resample = Image.BICUBIC, fill = True)
	im = im.rotate(angle = random.randint(0, 30), resample = Image.BICUBIC, expand = True)
	im = im.filter(ImageFilter.EDGE_ENHANCE)
	im = im.filter(ImageFilter.BLUR)
	return im

if __name__ == "__main__":
	strs = genStr(4)
	imVrf = genVrfImg(strs)
	imVrf.show()
