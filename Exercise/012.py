# coding: utf_8
# 敏感词文本文件 filtered_words.txt，里面的内容 和 0011题一样，当用户输入敏感词语，则用 星号 * 替换，例如当用户输入「北京是个好城市」，则变成「**是个好城市」。

wL =[]

with open("filtered_words.txt", "rt", encoding="utf_8") as f:
	for line in f:
		word = line.strip('\n')
		if len(word) != 0:
			wL.append(word)

print("Filtred Words:\n" + "\n".join(wL) + "\n")
while True:
	inS = input("输入词语 (exit 退出)：\n")
	if inS == "exit":
		break
	for word in wL:
		inS = inS.replace(word, "*" * len(word))
	print(inS)
