# coding = utf-8
"""
显示一些字体
"""

import ntpath
from io import StringIO

fontString = """abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ
<br>αβγδεζηθικλμνξοπρστυφχψω ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ
<br>äæåàáâãçèéêëðìíîïöøòóôõœñùúûüýþ ÄÆÅÀÁÂÃÇÈÉÊËÐÌÍÎÏÖØÒÓÔÕÑÙÚÛÜÝÞ
<br>1234567890+-_=~`!@#$%^&*,./\()[]{} 我能吞下玻璃而不傷身體
<br>“微风迎客，软语伴茶。”「微風迎客，軟語伴茶。」我能吞下玻璃而不伤身体
"""

# 过滤字体文件
# def filterFont(font):
	# if not ntpath.isfile(font): return False
	# if not (font.endswith(".ttf") or font.endswith(".ttc") or font.endswith(".otf")): return False
	# if ntpath.getsize(font) < 2**20: return False
	# return True

# 选出大于 1M 的字体文件 BigFontList
# fontList = glob.glob(r"C:/Windows/Fonts/*.ttf")
# fontList += glob.glob(r"C:/Windows/Fonts/*.ttc")
# fontList += glob.glob(r"C:/Windows/Fonts/*.otf")
# bfl = filter(lambda x: (op.getsize(x) > 2**20), FontList) # 生成器
# bfl = list(bfl).sort()

bfl = [
	"FangSong",
	"Gulim",
	"KaiTi",
	"Malgun Gothic", 
	"Microsoft JhengHei UI",
	"Microsoft YaHei UI",
	"MingLiU",
	"mlfb",
	"mlkb",
	"mlsb",
	"msxma",
	"SimHei",
	"SimSun",
	"Source Han Sans",
	"Source Han Sans K",
	"Source Han Sans SC",
	"Source Han Sans TC",
	"STCaiyun",
	"STFangsong",
	"STHupo",
	"STKaiti",
	"STLiti",
	"STSong",
	"STXihei",
	"STXingkai",
	"STZhongsong",
	"sxa",
	"XHei Dongqing Mono",
	"XHei Microsoft",
	"XHei OSX",
	"XHei Solid",
	"XHei Traditional",
	"XHei WP",
	"XSung Classical",
	"XSung Sharp",
	"Yu Gothic UI",
	"Yu Mincho",
]

# 生成一个字体的显示文字
def genStr(FontName:str, String:str=None):
	if String is None:
		String = FontName
	return """
<p style="font-family: {FN}; font-size:20px">{FN:-^60s}</p>
<p style = "font-family: {FN}">{FS}</p>
""".format(FN=FontName, FS=String)

outs = StringIO()
outs.write("""
<html>
<head>
<meta http-equiv="Content-Type"; content="text/html"; charset="utf-8" />
</head>
<title>FontView</title>
<body style="font-weight:100; font-size:16px; line-height:1.4">
""")
for bf in bfl:
	outs.write(genStr(bf, fontString))
outs.write("""
</body>
</html>""")

with open("FontView.html", mode="wt", encoding="utf-8") as fv:
	fv.write(outs.getvalue())
