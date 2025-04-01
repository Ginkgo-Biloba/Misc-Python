# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack

# 取 FFT 计算的结果 freqs 中的前 n 项进行合成，返回合成结果，计算 loops 个周期的波形
def fftCombine(freqs, n, loops=1):
	length = len(freqs) * loops
	data = np.zeros(length)
	idx = loops * np.arange(0, length, 1) / length * 2 * np.pi
	for (k, p) in enumerate(freqs[:n]):
		if (k != 0): p *=2 # 除去直流成分之外，其余的系数都 *2
		data += np.real(p) * np.cos(k * idx) # 余弦成分的系数为实数部
		data -= np.imag(p) * np.sin(k * idx) # 正弦成分的系数为负的虚数部
	return (idx, data)

# 产生 size 点取样的三角波，其周期为 1
def triWave(size):
	x = np.arange(0, 1, 1 / size)
	y = np.where(x < 0.5, x , 0)
	y = np.where(x >= 0.5, 1 - x, y)
	return (x, y)

# 方波
def sqWave(size):
	x = np.arange(0, 1, 1 / size)
	y = np.where(x < 0.5, 1, 0)
	return (x, y)

def FFTDemo1():
	fftSize = 256

	# 计算三角波和其 FFT
	(x, y) = triWave(fftSize)
	fy = np.fft.fft(y) / fftSize

	# 绘制三角波的 FFT 的前 20 项的振幅，由于不含下标为偶数的值均为 0， 因此取 log 之后无穷小，无法绘图，用 np.clip 函数设置数组值的上下限，保证绘图正确
	plt.figure()
	plt.plot(np.clip(20*np.log10(np.abs(fy[:20])), -120, 120), "o")
	plt.xlabel(u"频率"); plt.ylabel(u"能量 (dB)")
	plt.title(u"三角波的 FFT 结果")

	# 绘制原始的三角波和用正弦波逐级合成的结果，使用取样点为x轴坐标
	plt.figure()
	plt.plot(y, label=u"原始三角波", linewidth=2)
	for i in [0, 1, 3, 5, 7, 9]:
		(idx, data) = fftCombine(fy, i + 1, 2) # 计算两个周期的合成波形
		plt.plot(data, label=u"$N={}$".format(i))
	plt.legend()
	plt.title(u"部分傅里叶级数的三角波")
	plt.show()

def FFTDemo2():
	sampling_rate = 8000
	fft_size = 512
	t = np.arange(0, 1, 1 / sampling_rate)
	x = np.sin(2 * np.pi * 156.25 * t)  + 2 * np.sin(2 * np.pi * 234.375 * t)
	xs = x[:fft_size]
	xf = np.fft.rfft(xs) / fft_size
	freqs = np.linspace(0, sampling_rate / 2, fft_size / 2 + 1)
	xfp = 20 * np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
	plt.figure(figsize=(8, 4))
	plt.subplot(211)
	plt.plot(t[:fft_size], xs)
	plt.xlabel(u"时间 $\\rm s$")
	plt.title(u"$\\rm 156.25Hz$ 和 $\\rm 234.375 Hz$ 的波形和频谱")
	plt.subplot(212)
	plt.plot(freqs, xfp)
	plt.xlabel(u"频率 $\\rm Hz$")
	plt.subplots_adjust(hspace=0.4)
	plt.show()


# 用 hann 窗降低频谱泄漏
def hannDemo():
	sampling_rate = 8000
	fft_size = 512
	t = np.arange(0, 1.0, 1.0 / sampling_rate)
	x = np.sin(2 * np.pi * 200 * t)  + 2 * np.sin(2 * np.pi * 300 * t)
	xs = x[:fft_size] 
	ys = xs * signal.hann(fft_size, sym=0)

	xf = np.fft.rfft(xs) / fft_size
	yf = np.fft.rfft(ys) / fft_size
	freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
	xfp = 20 * np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
	yfp = 20 * np.log10(np.clip(np.abs(yf), 1e-20, 1e100))
	plt.figure(figsize=(8, 4))
	plt.title(u"$\\rm 200Hz$ 和 $\\rm 300Hz$ 的波形和频谱")
	plt.plot(freqs, xfp, label=u"矩形窗")
	plt.plot(freqs, yfp, label=u"hann窗")
	plt.legend()
	plt.xlabel(u"频率(Hz)")

	a = plt.axes([.4, .2, .4, .4])
	a.plot(freqs, xfp, label=u"矩形窗")
	a.plot(freqs, yfp, label=u"hann窗")
	a.set_xlim(100, 400); a.set_ylim(-40, 0)
	plt.show()

"""
快速卷积
由于 FFT 运算可以高效地将时域信号转换为频域信号，其运算的复杂度为 O(N*log(N))，因此三次 FFT 运算加一次乘积运算的总复杂度仍然为 O(N*log(N)) 级别，而卷积运算的复杂度为 O(N*N)，显然通过 FFT 计算卷积要比直接计算快速得多。这里假设需要卷积的两个信号的长度都为 N。
FFT 运算假设其所计算的信号为周期信号，因此通过上述方法计算出的结果实际上是两个信号的循环卷积，而不是线性卷积。为了用 FFT 计算线性卷积，需要对信号进行补零扩展，使得其长度长于线性卷积结果的长度。
例如，如果我们要计算数组 a 和 b 的卷积，a 和 b 的长度都为 128，那么它们的卷积结果的长度为 len(a) + len(b) - 1 = 257。为了用 FFT 能够计算其线性卷积，需要将 a 和 b 都扩展到 256。
"""
def FFTConvolve(a, b):
	n = len(a) + len(b) - 1
	N = 2**(int(np.log2(n)) + 1)
	A = np.fft.fft(a, N)
	B = np.fft.fft(b, N)
	c = np.fft.ifft(A * B)
	return c[:n]

def FFTCDemo():
	a = np.random.rand(128)
	b = np.random.rand(128)
	c = np.convolve(a, b)
	print(np.sum(np.abs(c - FFTConvolve(a, b))))


"""
Hilbert 变换
Hilbert 变换能在振幅保持不变的情况下将输入信号的相角偏移 90 度，简单地说就是能将正弦波形转换为余弦波形
此处将相角偏移 +90 度成为 Hilbert 正变换。有的文献书籍正好将定义倒转过来：将偏移 +90 度称为 Hilbert 负变换，而偏移 -90 度称为 Hilbert 正变换。
Hilbert 变换可以用作包络检波。具体算法：envelope = \sqrt{H(x)^2 + x^2}
其中 x 为原始载波波形，H(x) 为 x 的 Hilbert 变换之后的波形，envelope 为信号 x 的包络。其原理很容易理解：假设 x 为正弦波，那么 H(x) 为余弦波，根据公式 \sin^2(t) + \cos^2(t) = 1 可知 envelope 恒等于 1，为 sin(t) 信号的包络。
"""
def HilbertEvelope():
	t = np.arange(0, 0.3, 1/10000)
	x = np.sin(2 * np.pi * 1000 * t) * (np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 7 * t) + 3)
	hx = fftpack.hilbert(x)
	plt.plot(x, label=u"载波信号")
	plt.plot(np.sqrt(x**2 + hx**2), label=u"计算的包络线")
	plt.title(u"使用 Hibert 变换计算包络线")
	plt.legend()
	plt.show()


FFTDemo1()
# FFTDemo2()
# hannDemo()
# FFTCDemo()
# HilbertEvelope()
