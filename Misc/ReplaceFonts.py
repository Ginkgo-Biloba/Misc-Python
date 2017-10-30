from io import StringIO;

def str_gen (sr, uni_rg, font_weight, font_style, dis, ost) :
	ost.write ('@font-face {' + '\n');
	ost.write ('\tfont-family: "' + sr + '";\n');
	ost.write ('\tunicode-range: ' + uni_rg + ';\n');
	if (font_weight != '') :
		ost.write('\tfont-weight: ' + font_weight + ';\n'); 
	if (font_style != '') :
		ost.write ('\tfont-style: ' + font_style + ';\n');
	ost.write ('\tsrc: local("' + dis + '")' + ';\n');
	ost.write ('}\n');

sr_sans = [
	"sans-serif",
	"Arial",
	"Calibri",
	"Constantia",
	"Helvetica",
	"Lucida Grande",
	"Mceinline",
	"Tahoma",
	"Trebuchet MS",
	"Verdana",
	"STXiHei",
	"Heiti SC",
	"STHeiti-SC",
	"Microsoft YaHei",
	"Microsoft YaHei UI",
	"NSimSun",
	"SimSun",
	"Source Han Sans CN",
	"WenQuanYi Zen Hei",
	"Noto Sans",
	"宋体",
	"新宋体",
	"隶书",
	"黑体",
	"华文细黑",
	"华文黑体",
	"微软雅黑",
	"微软雅黑 UI",
];

sr_sans_TC = [
	"MingLiu",
	"MingLiu-ExtB",
	"MingLiu_HKSCS",
	"MingLiu_HKSCS-ExtB",
	"PMingLiu",
	"PMingLiu-ExtB",
	"Microsoft Jhenghei",
	"Microsoft Jhenghei UI",
	"細明體",
	"新細明體",
	"微軟正黑體",
	"微軟正黑體 UI",
]

sr_serif = [
	"serif",
	"Times CY",
	"Times",
	"Arial SimSun",
	"SimSun Arial",
	"Kaiti",
	"楷体",
	"仿宋",
];

sr_mono = [
	"monospace",
	"Andale Mono",
	"Courier",
	"Courier New",
	"Lucida Console",
	"Menlo",
	"Monaco",
	"mono",
	"Source Code Pro",
];

outs = StringIO();

# sans-serif
outs.write ('/*--------------------sans-serif--------------------*/');
outs.write ('\n\n');
for sr in sr_sans :
	str_gen (sr, "U+0000-2E7F", "400", "Normal", "Segoe UI", outs);
	str_gen (sr, "U+0000-2E7F", "700", "Normal", 'Segoe UI Bold', outs);
	str_gen (sr, "U+0000-2E7F", "400", "Italic", "Segoe UI Italic", outs);
	str_gen (sr, "U+0000-2E7F", "700", "Italic", "Segoe UI Bold Italic", outs);
	str_gen (sr, "U+2E80-FFFF", "400", "", "XHei-OSX", outs);
	str_gen (sr, "U+2E80-FFFF", "700", "", "XHei-OSX-Bold", outs);
	outs.write ('\n');
	
# sans-serif-TC
outs.write ('/*--------------------sans-serif-TC--------------------*/');
outs.write ('\n\n');
for sr in sr_sans_TC :
	str_gen (sr, "U+0000-2E7F", "400", "Normal", "Segoe UI", outs);
	str_gen (sr, "U+0000-2E7F", "700", "Normal", 'Segoe UI Bold', outs);
	str_gen (sr, "U+0000-2E7F", "400", "Italic", "Segoe UI Italic", outs);
	str_gen (sr, "U+0000-2E7F", "700", "Italic", "Segoe UI Bold Italic", outs);
	str_gen (sr, "U+2E80-FFFF", "400", "", "XHei-Traditional", outs);
	str_gen (sr, "U+2E80-FFFF", "700", "", "XHei-Traditional-Bold", outs);
	outs.write ('\n');

# serif
outs.write ('/*--------------------serif--------------------*/');
outs.write ('\n\n');
for sr in sr_serif :
	str_gen (sr, "U+0000-2E7F", "400", "Normal", "Linux Libertine", outs);
	str_gen (sr, "U+0000-2E7F", "700", "Normal", "Linux Libertine Bold", outs);
	str_gen (sr, "U+0000-2E7F", "400", "Italic", "Linux Libertine Italic", outs);
	str_gen (sr, "U+0000-2E7F", "700", "Italic", "Linux Libertine Bold Italic", outs);
	str_gen (sr, "U+2E80-FFFF", "400", "", "STKaiti", outs);
	# str_gen (sr, "U+2E80-FFFF", "", "", "STKaiti", outs);
	outs.write ('\n');	

# mono
outs.write ('/*--------------------monospace--------------------*/');
outs.write ('\n\n');
for  sr in sr_mono :
	str_gen (sr, "U+0000-2E7F", "400", "Normal", "Consolas", outs);
	str_gen (sr, "U+0000-2E7F", "700", "Normal", "Consolas Bold", outs);
	str_gen (sr, "U+0000-2E7F", "400", "Italic", "Consolas Italic", outs);
	str_gen (sr, "U+0000-2E7F", "700", "Italic", "Consolas Bold Italic", outs);
	str_gen (sr, "U+2E80-FFFF", "400", "", "XHei-OSX", outs);
	str_gen (sr, "U+2E80-FFFF", "700", "", "XHei-OSX-Bold", outs);
	outs.write ('\n');

with open("Stylish-字体替换.css", 'w', encoding = 'utf-8') as outf:
	outf.write ('''body {
	font-family: Myriad Pro, Segoe UI, EmojiOne Color, Segoe UI Emoji, XHei Solid, SimHei, Yu Gothic UI, Malgun Gothic, Arial Unicode MS, Segoe UI Symbol;
}
h1, h2, h3 {
	font-family: Minion Pro, Linux Libertine, EmojiOne Color, Segoe UI Emoji, STKaiti, Kaiti, XSung Sharp, Batang, Segoe UI Symbol; 
}
pre, code {
	font-family: Consolas, EmojiOne Color, Segoe UI Emoji, XHei OSX, SimHei, Yu Gothic UI, Malgun Gothic, Arial Unicode MS, Segoe UI Symbol;
}''');
	outf.write ("\n\n");
	outf.write (outs.getvalue());
	outf.close();
