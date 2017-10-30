# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
import wave
from scipy import signal

def readWav():
	fpth = r"E:\Sounds\Windows Media\bin5080.wav"

	f = wave.open(fpth, "rb")

	# 读取格式信息
	# 通道，量化位(字节)数，采样频率，采样点数
	params = f.getparams()
	(nc, spw, fmrt, fms) = params[:4]
	print(nc, spw, fmrt, fms)

	# 读取波形数据
	strdata = f.readframes(fms)
	f.close

	# 波形数据转换为数组
	wavedata = np.fromstring(strdata, dtype=np.int16)
	wavedata.shape = (-1, 2)
	wavedata = wavedata.T
	t = np.arange(0, fms) / fmrt

	# 绘制波形
	plt.subplot(211)
	plt.plot(t, wavedata[0], color="blue")
	plt.subplot(212)
	plt.plot(t, wavedata[1], color="green")
	plt.xlabel("Time ($s$)")
	plt.show()


def writeWav():
	fmrt = 44100 # 采样率
	tt = 10 # 时长

	# 产生 10 秒 44.11kHZ 的 100 - 1kHz 的频率扫描波
	t = np.arange(0, tt, 1.0 / fmrt)
	wavedata = signal.chirp(t, 100, tt, 1000, method='linear') * 1e4
	wavedata = wavedata.astype(np.int16)

	# 配置参数并写入
	f = wave.open(__file__.replace(".py", ".wav"), "wb")
	f.setnchannels(1)
	f.setsampwidth(2)
	f.setframerate(fmrt)
	f.writeframes(wavedata.tostring())
	f.close


writeWav()
