import ctypes
from ctypes import c_ubyte, c_ushort, c_int, c_float
from ctypes import ARRAY, POINTER
from enum import IntEnum
import math
import os
import os.path as osp
import sys
import time
import subprocess
import numpy as np
from PIL import Image


class RawProc:
	"""
	和 Numpy 类似，如果有参数 out，类型和大小需要满足要求
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
		##### Gamma Table #####
		xs = np.linspace(0, 1, 65536)
		# libpng NTSC
		# http://libpng.org/pub/png/spec/1.2/PNG-GammaAppendix.html
		(a, b, c, d, g) = (1.099, -0.099, 4.5, 0.018, 0.45)
		ys = np.where(xs < d, c * xs, a * np.power(xs, g) + b)
		self.gtab = (ys * 255).astype(np.uint8)
		##### Color Correction Matrix #####
		# 来自 Google HDR+ 的素材
		self.rgb_cam = np.array([
			[+1.65625, -0.71875, +0.0625],
			[-0.15625, +1.2890625, -0.1328125],
			[+0.109375, -0.7265625, +1.6171875],
		],
			dtype=np.float32)

	def fcol(self, r, c, pat):
		return 3 & (pat >> (2 * (2 * (r & 1) + (c & 1))))

	def scale(self, byr, rbit, darkness, saturate=0, *, out=None):
		if (saturate <= darkness):
			saturate = 2**rbit - 1
		assert (darkness < saturate)
		fdark = np.array([darkness], dtype=np.float32)
		frate = np.array([65535.0 / (saturate - darkness)], dtype=np.float32)
		if (out is None):
			out = np.empty_like(byr)
		assert out.shape == byr.shape and out.dtype == byr.dtype
		np.clip((byr - fdark) * frate + self.rd5, 0, 65535, out=out)
		return out

	def estgain(self, byr, pat, *, out=None):
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

	def wbgain(self, byr, wb, pat, *, out=None):
		"wb 是三个数的 np.float32，RGB 顺序"
		w2 = byr.shape[1] // 2
		assert wb.shape[0] == 3 and wb.dtype == np.float32
		if (out is None):
			out = np.empty_like(byr)
		assert out.shape == byr.shape and out.dtype == byr.dtype
		mul4 = np.array([
			[wb[self.fcol(0, 0, pat)], wb[self.fcol(0, 1, pat)]],
			[wb[self.fcol(1, 0, pat)], wb[self.fcol(1, 1, pat)]],
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

	def guess(self, fsz, size, wr, hr):
		if (size[0] <= 2 or size[1] <= 2):
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

	def read(self, fname, height, width, rbit, pack, *, out=None):
		" pack: 0 不打包，1 交错存储，2 连续存储 "
		if not osp.isfile(fname):
			return None
		if (pack == 0):
			out = np.fromfile(fname, dtype=np.uint16)
			fsz = out.shape[0]
			if (height < 2 or width < 2):
				size = [-1, -1]
				self.guess(fsz, size, 4, 3)
				self.guess(fsz, size, 16, 9)
				self.guess(fsz, size, 5, 4)
				self.guess(fsz, size, 1, 1)
				width = size[0]
				height = size[1]
				if (width > 0 and height > 0):
					print("guessed {:d}x{:d} from fsz {:d}".format(width, height, fsz))
				else:
					print("cannot guess size from fsz {:d}".format(fsz))
					return None
			if (out.shape[0] != height * width):
				out = None
			else:
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
			c_int(height), c_int(width), c_int(rbit), c_int(pack))
		return out


RPC = RawProc()

RawPattern = {
	"rggb": 0x94949494,
	"bggr": 0x16161616,
	"grbg": 0x61616161,
	"gbrg": 0x49494949,
}

RawPack = ["none", "mipi", "cont"]

RawDemosaic = ["lin", "xxx", "ppg", "ahd"]

############################################################


class Phone(IntEnum):
	" 预定义一些手机格式 "
	OnePlusIMX586 = 101
	SamsungC1LSI = 201
	SamsungC2LSI = 202
	SamsungZ3LSI = 203
	SamsungC2QC = 204
	VivoSample = 301
	VivoPreview = 302
	MeizuIMX686 = 401


DefaultPhone = Phone.SamsungC2QC


class RawHead:

	def __init__(self):
		self.name = None
		self.text = ""
		self.pack = "none"
		self.patt = "bggr"
		self.rbit = 10
		self.darkness, self.saturate = 64, 0
		self.cols, self.rows = 4000, 3000
		self.isp = 2.0
		self.wb = np.ones(3, np.float32)
		self.demq = "ahd"

	def loadphone(self):
		phone = DefaultPhone
		if phone is None:
			self.text, _ = osp.splitext(self.name)
		elif (phone == Phone.OnePlusIMX586):
			self.text = self.name[:21]
			self.patt = "rggb"
		elif (phone == Phone.SamsungC1LSI) or (phone == Phone.SamsungZ3LSI):
			self.text = self.name[:-17]
			self.patt = "grbg"
			self.rbit = 12
			self.darkness = 0
			self.cols, self.rows = 4032, 3024
		elif (phone == Phone.SamsungC2LSI):
			self.text = self.name[:-17]
			self.patt = "grbg"
			self.rbit = 12
			self.darkness = 0
		elif (phone == Phone.SamsungC2QC):
			self.text = self.name[:-4]
			self.patt = "grbg"
		elif (phone == Phone.VivoSample):
			self.text = self.name[:24] + "_fn0_in_0_10bit"
			self.pack = "mipi"
			self.cols, self.rows = 4080, 3060
		elif (phone == Phone.VivoPreview):
			self.text = self.name[:24] + "_fn0_in_0_10bit"
			self.patt = "gbrg"
			self.wb = np.ones(3, np.float32)
			self.rbit = 14
			self.darkness = 0
			self.cols, self.rows = 4080, 3060
		elif (phone == Phone.MeizuIMX686):
			self.text = self.name[:-6]
			self.patt = "rggb"
			self.rbit = 14
			self.darkness = 1024
			self.cols, self.rows = 4624, 3472
		else:
			pass
		self.text += ".txt"


def dngRead(h: RawHead):
	p = r"G:\Sample\cvtraw\dcraw.exe"
	p = subprocess.run([p, "-i", "-v", h.name], stdout=subprocess.PIPE)
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
			h.wb = np.array(cammul[:-1], np.float32)
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
	h.loadphone()
	# txt = h.name[:13] + "_{:d}x{:d}.txt".format(h.cols, h.rows)
	# 上面设置 raw 的属性和 txt 的名字
	if not (osp.isfile(h.text)):
		return
	fid = open(h.text, "r")
	if (not fid.readable()):
		return
	for line in fid:
		kv = line.split(":")
		if (len(kv) != 2):
			continue
		kv[0] = kv[0].strip()
		kv[1] = kv[1].strip()
		if (kv[0] == "redGain"):
			h.wb[0] = float(kv[1])
		elif (kv[0] == "blueGain"):
			h.wb[2] = float(kv[1])
		elif (kv[0] == "wbbgr"):
			swb = kv[1].split(",")
			swb = list(map(float, swb))
			h.wb = np.array(swb, np.float32)
		elif (kv[0] == "rawformat"):
			h.patt = kv[1]
		elif (kv[0] == "rawdepth"):
			h.rbit = int(kv[1])
		elif (kv[0] == "blacklevel"):
			h.darkness = int(kv[1])
		elif (kv[0] == "whitelevel"):
			h.saturate = int(kv[1])
		elif (kv[0] == "rawsize"):
			ssz = kv[1].split("x")
			ssz = list(map(int, ssz))
			h.cols, h.rows = ssz[0], ssz[1]
	if (0 < h.wb[0] and 0 < h.wb[2]):
		h.wb[1] = 1
	h.wb *= h.isp
	fid.close()


def cvtHead(h: RawHead):
	raw = None
	pack = RawPack.index(h.pack)
	if (h.name.lower().endswith(".dng")):
		raw = dngRead(h)
	else:
		txtRead(h)
		pack = RawPack.index(h.pack)
		raw = RPC.read(h.name, h.rows, h.cols, h.rbit, pack)
	patt = RawPattern[h.patt]
	if (raw is None):
		info = " ❌  {:s} -> read failed".format(h.name)
		print(info)
		return False
	if (h.saturate <= h.darkness and 0 < h.rbit):
		h.saturate = 2**h.rbit - 1
	assert (h.darkness < h.saturate)
	raw.astype(np.int16, copy=False).clip(0, None, out=raw)
	RPC.scale(raw, h.rbit, h.darkness, h.saturate, out=raw)
	if (h.wb is None or h.wb[0] < 0.1):
		RPC.estgain(raw, patt, out=h.wb)
		info = " ⚙️  {:s} -> estimated wb".format(h.name, h.wb)
		print(info)
	RPC.wbgain(raw, h.wb, patt, out=raw)
	rgb = RPC.demosaic(raw, patt, RawDemosaic.index(h.demq))
	RPC.cam2linear(rgb, out=rgb)
	img = Image.fromarray(RPC.gtab[rgb], "RGB")
	ext = osp.splitext(h.name)[0] + ".jpg"
	img.save(ext, subsampling=0, quality=90)
	info = " ✔  "
	info += " {:s} {:s} [{:d}, {:d}]".format(h.pack, h.patt, h.darkness,
		h.saturate)
	info += " {:d}×{:d}".format(h.cols, h.rows)
	info += " [{:.3f}, {:.3f}, {:.3f}]".format(h.wb[0], h.wb[1], h.wb[2])
	info += " {:s}".format(h.demq)
	info += " {:s}".format(ext)
	print(info)
	return True


############################################################

if (__name__ == "__main__"):
	from multiprocessing import pool
	tick = time.time()
	EXTS = (".dng", ".raw", ".rawmipi", ".raw14gbrg16")
	# os.system("chcp 65001")
	if (len(sys.argv) > 1):
		os.chdir(sys.argv[1])
		print("change directory to", sys.argv[1])
	names = os.listdir(".")
	rawhs = list()
	nsels = list(map("_{:02d}".format, range(14, 20)))
	for x in names:
		_, ext = osp.splitext(x)
		ext = ext.lower()
		if not (ext in EXTS):
			continue
		if (all(map(lambda s: x.find(s) == -1, nsels))):
			pass
		h = RawHead()
		h.name = x
		rawhs.append(h)
	ret = [0]
	pp = pool.Pool(min(os.cpu_count(), 6))
	ret = pp.map(cvtHead, rawhs)
	# cvtHead(rawhs[0])
	ret = sum(ret)
	tick = time.time() - tick
	info = "\n{:d} success(es), {:d} failure(s), {:.3f} seconds\n"
	info = info.format(ret, len(rawhs) - ret, tick)
	print("=" * 60 + info)
