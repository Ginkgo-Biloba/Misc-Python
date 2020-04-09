# coding=utf-8
import ctypes
from ctypes import c_ubyte, c_ushort, c_int, c_float
from ctypes import ARRAY, POINTER
import math
import os
import os.path as osp
import numpy as np
from PIL import Image
import subprocess


class RawProc:
	"""
	将成员 dll 实现成类似于 C++ 的静态变量初始化？
	效率起见：
	- 为了可以多进程处理，类里面不包含任何与图像有关的数据。
	- 最好只构造化一个实例，函数都在它上面调用。
	- 和 Numpy 里面函数类似，如果有参数 out，类型和大小需要满足要求。
	"""

	def __init__(self):
		self.rd5 = np.array([0.5], dtype=np.float32)
		##### 函数接口 #####
		dllpath = osp.join(osp.dirname(__file__), "rawpy.dll")
		# print(dllpath)
		self.dll = ctypes.CDLL(dllpath)
		self.dll.est_wbgain.argtypes = [
			POINTER(c_ushort), c_int, c_int, c_int,
			POINTER(c_float)
		]
		self.dll.est_wbgain.restype = None
		self.dll.demosaic.argtypes = [
			POINTER(c_ushort),
			POINTER(ARRAY(c_ushort, 3)), c_int, c_int, c_int, c_int
		]
		self.dll.demosaic.restype = None
		self.dll.raw_read.argtypes = [
			POINTER(c_ubyte),
			POINTER(c_ushort), c_int, c_int, c_int, c_int, c_int
		]
		self.dll.raw_read.restype = None
		self.dll.rgb2bgr.argtypes = [
			POINTER(c_ubyte), POINTER(c_ubyte), c_int, c_int
		]
		self.dll.rgb2bgr.restype = None
		##### Gamma Table #####
		xs = np.linspace(0, 1, 65536)
		# MATLAB
		# https://www.mathworks.com/help/images/ref/lin2rgb.html
		(a, b, c, d, g) = (1.055, -0.055, 12.92, 0.0031308, 1 / 2.4)
		ys = np.where(xs < d, c * xs, a * np.power(xs, g) + b)
		self.gtab24 = (ys * 65535 + 0.5).astype(np.uint16)
		self.gtab24_8 = (self.gtab24 >> 8).astype(np.uint8)
		# libpng NTSC
		# http://libpng.org/pub/png/spec/1.2/PNG-GammaAppendix.html
		(a, b, c, d, g) = (1.099, -0.099, 4.5, 0.018, 0.45)
		ys = np.where(xs < d, c * xs, a * np.power(xs, g) + b)
		self.gtab22 = (ys * 65535 + 0.5).astype(np.uint16)
		self.gtab22_8 = (self.gtab22 >> 8).astype(np.uint8)
		##### Color Correction Matrix #####
		# 来自 dcraw
		self.rgb_cam = np.array([
			[+1.26195443, -0.45776108, +0.19580664],
			[-0.15059669, +1.13350368, +0.01709299],
			[-0.01468136, -0.36106369, +1.37574506],
		],
			dtype=np.float32)
		# 来自 Google HDR+ 的素材
		self.rgb_cam = np.array([
			[+1.65625, -0.71875, +0.0625],
			[-0.15625, +1.2890625, -0.1328125],
			[+0.109375, -0.7265625, +1.6171875],
		],
			dtype=np.float32)

	def fcol(self, r, c, pat):
		return 3 & (pat >> (2 * (2 * (r & 1) + (c & 1))))

	def scale(self, byr, depth, dark, sat=0, *, out=None):
		if (sat <= dark):
			sat = 2**depth - 1
		fdark = np.array([dark], dtype=np.float32)
		frate = np.array([65535.0 / (sat - dark)], dtype=np.float32)
		if (out is None):
			out = np.empty_like(byr)
		assert out.shape == byr.shape and out.dtype == byr.dtype
		np.clip((byr - fdark) * frate + self.rd5, 0, 65535, out=out)
		return out

	def estgain(self, byr, pat, *, out=None):
		" 这里的 out 是为了可以更改外面的数据 "
		height = byr.shape[0]
		width = byr.shape[1]
		if (out is None):
			out = np.ones(3, dtype=np.float32)
		assert out.shape == (3,) and out.dtype == np.float32
		assert out.flags['C_CONTIGUOUS'] and byr.flags['ALIGNED']
		assert byr.ndim == 2 and byr.dtype == np.uint16
		assert (width | height) % 2 == 0
		assert byr.flags['C_CONTIGUOUS'] and byr.flags['ALIGNED']
		src = byr.ctypes.data_as(POINTER(c_ushort))
		dst = out.ctypes.data_as(POINTER(c_float))
		self.dll.est_wbgain(src, c_int(height), c_int(width), c_int(pat), dst)
		return out

	def wbgain(self, byr, gain, pat, *, out=None):
		"gain 是三个数的 np.float32，RGB 顺序"
		w2 = byr.shape[1] // 2
		assert gain.shape[0] == 3 and gain.dtype == np.float32
		if (out is None):
			out = np.empty_like(byr)
		assert out.shape == byr.shape and out.dtype == byr.dtype
		mul4 = np.array([
			[gain[self.fcol(0, 0, pat)], gain[self.fcol(0, 1, pat)]],
			[gain[self.fcol(1, 0, pat)], gain[self.fcol(1, 1, pat)]],
		], np.float32)
		mul = np.repeat(mul4, w2, 0).reshape((1, -1))
		b2 = byr.reshape((-1, 4 * w2))
		o2 = out.reshape((-1, 4 * w2))
		np.clip(np.multiply(b2, mul) + self.rd5, 0, 65535, out=o2)
		return out

	def demosaic(self, byr, pat, method=3, *, out=None):
		" method: 0 LIN, 2 PPG, 3 AHD"
		assert method in (0, 2, 3)
		height = byr.shape[0]
		width = byr.shape[1]
		assert byr.ndim == 2 and byr.dtype == np.uint16 and ((width | height) %
			2 == 0)
		assert byr.flags['C_CONTIGUOUS'] and byr.flags['ALIGNED']
		if (out is None):
			out = np.empty((height, width, 3), dtype=np.uint16)
		assert out.ndim == 3 and out.shape == (height, width, 3)
		assert out.dtype == np.uint16
		assert out.flags['C_CONTIGUOUS'] and out.flags['ALIGNED']
		src = byr.ctypes.data_as(POINTER(c_ushort))
		dst = out.ctypes.data_as(POINTER(ARRAY(c_ushort, 3)))
		self.dll.demosaic(src, dst, c_int(height), c_int(width), c_int(pat),
			c_int(method))
		return out

	def cam2linear(self, rgb, rgb_cam=None, *, out=None):
		" ccm 是 rgb from cam 顺序 "
		assert rgb.shape[2] == 3 and rgb.dtype == np.uint16
		if (out is None):
			out = np.empty_like(rgb)
		assert out.shape == rgb.shape and out.dtype == rgb.dtype
		if (rgb_cam is None):
			rgb_cam = self.rgb_cam
		assert rgb_cam.shape == (3, 3) and rgb_cam.dtype == np.float32
		rmul = rgb_cam.T
		src = rgb.reshape((-1, 3))
		dst = out.reshape((-1, 3))
		np.clip(np.matmul(src, rmul) + self.rd5, 0, 65535, out=dst)
		return out

	def rgb2bgr(self, rgb, *, out=None):
		assert rgb.ndim == 3 and rgb.dtype == np.uint8
		assert rgb.flags['C_CONTIGUOUS'] and out.flags['ALIGNED']
		if (out is None):
			out = np.empty_like(rgb)
		assert out.ndim == 3 and out.dtype == np.uint8 and out.shape == rgb.shape
		assert out.flags['C_CONTIGUOUS'] and out.flags['ALIGNED']
		self.dll.rgb2bgr(rgb.ctypes.data_as(POINTER(c_ubyte)),
			out.ctypes.data_as(POINTER(c_ubyte)), c_int(rgb.shape[0]),
			c_int(rgb.shape[1]))
		return out

	def guess_size(self, fsz, size, wr, hr):
		mul = wr * hr
		if (fsz // mul * mul != fsz):
			return False
		fsz = fsz // mul
		mul = int(math.sqrt(float(fsz)))
		if (mul * mul != fsz):
			return False
		size[0] = wr * mul
		size[1] = hr * mul
		return True

	def read(self, fname, height, width, depth, pack, *, out=None):
		" pack: 0 不打包，1 交错存储，2 连续存储 "
		if not osp.isfile(fname):
			return None
		if (pack == 0):
			out = np.fromfile(fname, dtype=np.uint16)
			fsz = out.shape[0]
			if (height < 2 or width < 2):
				size = [-1, -1]
				(self.guess_size(fsz, size, 4, 3) or self.guess_size(fsz, size, 16, 9)
					or self.guess_size(fsz, size, 1, 1))
				width = size[0]
				height = size[1]
				if (width > 0 and height > 0):
					print("guessed {:d}x{:d} from fsz {:d}".format(width, height, fsz))
				else:
					print("cannot guess size from fsz {:d}".format(fsz))
					return None
			out = out.reshape((height, width))
			return out
		shape = (height, width)
		if (out is None):
			out = np.empty(shape, dtype=np.uint16)
		assert out.shape == shape and ((width | height) % 2 == 0)
		assert out.flags['C_CONTIGUOUS'] and out.flags['ALIGNED']
		buf = np.fromfile(fname, dtype=np.uint8)
		buflen = buf.shape[0]
		self.dll.raw_read(buf.ctypes.data_as(POINTER(c_ubyte)),
			out.ctypes.data_as(POINTER(c_ushort)), c_int(buflen),
			c_int(height), c_int(width), c_int(depth), c_int(pack))
		return out


RPC = RawProc()

RawPattern = {
	"RG/GB": 0x94949494,
	"BG/GR": 0x16161616,
	"GR/BG": 0x61616161,
	"GB/RG": 0x49494949,
}

RawDemosaic = ["LIN", "WRONG", "PPG", "AHD"]

############################################################


class RawHead:
	""" 其实没啥用，就是当结构体用 """

	def __init__(self):
		self.name = ""
		self.rows = 0
		self.cols = 0
		self.pack = 0
		self.depth = 10
		self.dark = 63
		self.sat = 0
		self.patt = None
		self.gain = np.zeros(3, np.float32)
		self.dq = 3


def dngRead(h: RawHead):
	p = subprocess.run([r"G:\Sample\cvtraw\dcraw.exe", "-i", "-v", h.name],
		stdout=subprocess.PIPE)
	outs = p.stdout.decode("utf-8").split("\n")
	for line in outs:
		kv = line.split(":")
		if (len(kv) != 2):
			continue
		kv[0] = kv[0].strip()
		kv[1] = kv[1].strip()
		if (kv[0] == "Full size"):
			wh = kv[1].split("x")
			h.cols = int(wh[0])
			h.rows = int(wh[1])
		elif (kv[0] == "Filter pattern"):
			h.patt = kv[1]
		elif (kv[0] == "Camera multipliers"):
			cammul = kv[1].split(" ")
			cammul = list(map(float, cammul))
			h.gain = np.array(cammul[:-1], np.float32)
	if ((h.rows < 2) or (h.cols < 2) or ((h.rows | h.cols) % 2)):
		return None
	szexp = h.rows * h.cols * 2
	fid = open(h.name, "rb")
	if (not fid.readable()):
		return
	szfile = fid.seek(0, 2)
	if (szfile < szexp):
		fid.close()
		return None
	fid.seek(szfile - szexp, 0)
	raw = np.fromfile(fid, np.uint16, h.rows * h.cols)
	raw = raw.reshape((h.rows, h.cols))
	return raw


def txtRead(h: RawHead):
	(h.cols, h.rows) = (4000, 3000)
	h.pack = 1
	h.depth = 10
	h.dark = 64
	h.patt = "RG/GB"
	txt = h.name[:3] + ".txt"
	# txt = h.name[:13] + "_{:d}x{:d}.txt".format(h.cols, h.rows)
	# 上面设置 raw 的属性和 txt 的名字
	if not (osp.isfile(txt)):
		return
	fid = open(txt, "r")
	if (not fid.readable()):
		return
	for line in fid:
		kv = line.split(":")
		if (len(kv) != 2):
			continue
		kv[0] = kv[0].strip()
		kv[1] = kv[1].strip()
		if (kv[0] == "redGain"):
			h.gain[0] = float(kv[1])
		elif (kv[0] == "blueGain"):
			h.gain[2] = float(kv[1])
		elif (kv[0] == "blackLevel[0]"):
			h.dark = int(kv[1])
	if (1 < h.gain[0] or 1 < h.gain[2]):
		h.gain[1] = 1
	fid.close()


def cvtHead(h: RawHead):
	"""
	在主函数里面把所有数据（图像和属性）预处理，按组构成列表。
	使得有这么一个函数，它可以处理这一个或一组 Raw。
	然后使用进程池，在每一组图像上应用函数。
	"""
	raw = None
	# if ((h.rows < 0) or (h.cols < 0) or ((h.rows | h.cols) % 2 != 0)):
	# 	return False
	if (h.name.lower().endswith(".dng")):
		raw = dngRead(h)
	else:  #(h.name.lower().endswith(".raw")):
		txtRead(h)
		raw = RPC.read(h.name, h.rows, h.cols, h.depth, h.pack)
	if (raw is None):
		print("{:s} | read failed".format(h.name))
		return False
	if (h.sat <= h.dark and 0 < h.depth):
		h.sat = 2**h.depth - 1
	hrpat = RawPattern[h.patt]
	RPC.scale(raw, h.depth, h.dark, h.sat, out=raw)
	if (h.gain is None or h.gain[0] < 0.1):
		RPC.estgain(raw, hrpat, out=h.gain)
		print(h.name, "  -> estimated gain", h.gain)
	RPC.wbgain(raw, h.gain, hrpat, out=raw)
	rgb = RPC.demosaic(raw, hrpat, h.dq)
	RPC.cam2linear(rgb, out=rgb)
	img = Image.fromarray(RPC.gtab22_8[rgb], "RGB")
	pre, ext = osp.splitext(h.name)
	img.save(pre + ".bmp")
	info = h.name
	info += "  {:d}×{:d}".format(h.cols, h.rows)
	info += "  {:s}  [{:d}, {:d}]".format(h.patt, h.dark, h.sat)
	info += "  [{:.3f}, {:.3f}, {:.3f}]".format(h.gain[0], h.gain[1], h.gain[2])
	info += "  {:s}".format(RawDemosaic[h.dq])
	print(info)
	return True


############################################################

if (__name__ == "__main__"):
	import sys
	import time
	from multiprocessing import pool
	tick = time.time()
	EXTS = (".dng", ".rawmipi")
	olddir = os.getcwd()
	if (len(sys.argv) > 1):
		os.chdir(sys.argv[1])
		print("change directory to", sys.argv[1])
	os.chdir(r"..\video")
	names = os.listdir(".")
	rawhs = list()
	for x in names:
		_, ext = osp.splitext(x)
		ext = ext.lower()
		if not (ext in EXTS):
			continue
		h = RawHead()
		h.name = x
		rawhs.append(h)
	ret = [0]
	pp = pool.Pool()
	# ret = pp.map(cvtHead, rawhs)
	cvtHead(rawhs[2])
	ret = sum(ret)
	os.chdir(olddir)
	tick = time.time() - tick
	print("=" * 60)
	print("{:d} success(es), {:d} failure(s), {:.3f} seconds".format(
		ret,
		len(rawhs) - ret, tick))
