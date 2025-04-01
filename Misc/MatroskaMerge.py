# coding = utf-8
import os
import time
import sys
import subprocess

def fileList(dirRoot):
	for (parent, dirNames, fileNames) in os.walk(dirRoot):
		for filename in fileNames:
			yield (os.path.join(dirRoot, parent, filename))

def convertMKV(filename):
	sptExts = set([".rmvb", ".avi", ".ogv", ".rm"])
	fn, extn = os.path.splitext(filename)
	newfn =  fn + ".mkv"
	if os.path.exists(newfn):
		return -2
	if (not extn in sptExts):
		return -3
	cmdstr = ["\"C:\\Intel\MKVToolNix\\mkvmerge.exe\""]
	cmdstr.append(" \"--ui-language\" \"zh_CN\"")
	cmdstr.append(" \"--output\"")
	cmdstr.append("\"" + newfn + "\"")
	# cmdstr.append(" --no-chapters --no-global-tags") # 不要章节不要全局标签
	cmdstr.append("\"" + filename + "\"")
	# cmdstr.append(" & pause")
	cmdstr = " ".join(cmdstr)
	# print(cmdstr)
	# mkvcmd = subprocess.Popen(cmdstr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	mkvcmd = subprocess.Popen(cmdstr)
	rt = mkvcmd.wait()
	# print(mkvcmd.stdout.read())
	return rt


if(__name__ == "__main__"):
	dirRoot = """G:\下载"""
	if (len(sys.argv) > 1):
		dirRoot = sys.argv[1]
	c = 0; sc = 0
	for filen in fileList(dirRoot):
		c += 1
		print("\n处理：{}".format(filen))
		startT = time.clock()
		rt = convertMKV(filen)
		endT = time.clock()
		if (rt == 0):
			print("成功：用时", endT - startT, "秒")
			# os.rename(filen, filen + ".converted")
			sc += 1
		elif (rt == -2):
			print("错误：已经存在相同名字的 .mkv 文件")
		elif (rt == -3):
			print("错误：不支持该文件")
		else:
			print("出错：mkvmerge.exe 返回代码", rt)
	print("\n目录：{}".format(dirRoot))
	print(c, "个文件，合并成功", sc, "个")

