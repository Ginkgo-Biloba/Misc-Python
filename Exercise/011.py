# coding: utf_8
# 敏感词文本文件 filtered_words.txt，里面的内容为以下内容，当用户输入敏感词语时，则打印出 Freedom，否则打印出 Human Rights。

wL =[]

with open("filtered_words.txt", "rt", encoding="utf_8") as f:
	for line in f:
		word = line.strip('\n')
		if len(word) != 0:
			wL.append(word)

while True:
	inS = input("输入词语 (exit 退出)：\n")
	if inS in wL:
		print("Freedom")
	elif inS == "exit":
		break
	else:
		print("Human Right")

