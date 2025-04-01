# coding: utf_8
# 将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。 类似于图中效果

from PIL import Image, ImageDraw, ImageFont

im = Image.open(r'plane.jpg')
w, h = im.size
fs = min(w, h) // 10
ft = ImageFont.truetype(r'seguisym.ttf', size = fs)

dr = ImageDraw.Draw(im)
dr.text((w- fs, 0), '1', font = ft, fill = 0x00FFFF)

im.show()
