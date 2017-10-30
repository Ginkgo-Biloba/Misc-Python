# coding=utf_8
import sys
import unicodedata as ud
import textwrap

s = 'pýtĥöñ\fis\tawesome\r\n'
print(s)

remap = { ord("\t"): " ", ord("\f") : " ", ord("\r") : None}
a = s.translate(remap)
print(a)

cmbChars = dict.fromkeys(c for c in range(sys.maxunicode) if ud.combining(chr(c)))
b = ud.normalize("NFD", a)
print(b)
c = b.translate(cmbChars)
print(c)

digitMap = {c: ord('0') + ud.digit(chr(c)) for c in range(sys.maxunicode) if ud.category(chr(c)) == "Nd"}
print(len(digitMap))
x = '\u0661\u0662\u0663'
print(x, "->", x.translate(digitMap))

text = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."
print(text)
print(textwrap.fill(text, 70))
print(textwrap.fill(text, 40))
print(textwrap.fill(text, 70, initial_indent="    "))
print(textwrap.fill(text, 70, subsequent_indent="    "))
