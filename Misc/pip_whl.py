#coding=utf-8
"""使用 python pip 安装同文件夹下的 *.whl 文件"""
import os
import sys
import subprocess

def cmd_pip(file):
	return ("pip install --retries 0 " + file)


def cmd_ins_dir(root):
	rst = 0
	dir_bak = os.getcwd() # 记住原来的工作目录
	os.chdir(root) # 更改工作目录
	fail_list = list()
	for file in os.listdir(root):
		if (file.endswith(".whl")):
			pip_proc = subprocess.Popen(cmd_pip(file))
			rt = pip_proc.wait()
			if (rt == 0):
				"安装成功或已经存在"
				os.rename(file, file+".ed")
			else:
				"打印失败包，并计数"
				fail_list.append(file)
				rst += 1
	os.chdir(dir_bak) # 返回之前的工作目录
	print("\n")
	print("\n".join(fail_list))
	return rst

	
def del_ext(root):
	dir_bak = os.getcwd()
	os.chdir(root)
	rst = 0
	for file in os.listdir(root):
		if (file.endswith(".whl.ed")):
			os.rename(file, file[0:-3])
			rst += 1
		os.chdir(dir_bak)
	return rst
	
	
if (__name__ == "__main__"):
	root = os.path.abspath("")
	if (len(sys.argv) > 1):
		root = os.path.abspath(sys.argv[1])
	for i in range(1, 21):
		"使劲装 20 次，再装不好就弃疗"
		print("\n---------- 第 {:d} 次---------- \n".format(i))
		rst = cmd_ins_dir(root)
		if (rst == 0):
			rst = del_ext(root)
			print("\n尝试 {:d} 次，成功安装 {:d} 个 .whl 文件\n".format(i, rst))
			break
		elif (i == 20):
			print("\n---------- 弃疗----------")
			print("\n看看那些扩展名依旧是 .whl 的顽固分子吧 ~_~\n")
		else:
			print("\n---------- 失败 {:d} 个 ----------\n".format(rst))
	
