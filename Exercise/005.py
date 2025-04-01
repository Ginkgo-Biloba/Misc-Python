# coding :utf_8
# 你有一个目录，装了很多照片，把它们的尺寸变成都不大于 iPhone5 分辨率的大小

import glob
from PIL import Image

w, h = 640, 1136
sc = "E:\\图片\\自定义"
exts = ["*.jpg", "*.png", "*.bmp"]

def proc(f):
	im =  Image.open(f)
	pm = im.resize((w, h), Image.LANCZOS)
	pm.save(f.split('\\')[-1])


for ext in exts:
	fs = glob.glob(sc + '\\' + ext, recursive = True)
	for f in fs:
		proc(f)
