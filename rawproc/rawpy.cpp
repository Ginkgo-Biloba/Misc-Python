#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <climits>
#include <cmath>
#include <cassert>

/* 
 * 需要 Python 保证传入尺寸正确并且数组内存连续
 * BGGR            GRBG           GBRG            RGGB
 * 0x16161616      0x61616161     0x49494949      0x94949494
 */

#if defined _WIN32
#  define CExport extern "C" __declspec(dllexport)
#elif defined __GNUC__ || defined __clang__
#  define CExport extern "C" __attribute__ ((visibility ("default")))
#else
#  error must export function for Python
#endif


using uchar = unsigned char;
using ushort = unsigned short;
using vec3w = ushort[3];
using vec3s = short[3];


static inline int min(int x, int y)
{
	return y < x ? y : x;
}

static inline int max(int x, int y)
{
	return y < x ? x : y;
}

static inline int clamp(int v, int lo, int hi)
{
	// assert(lo <= hi);
	return (v < lo) ? lo : (v > hi ? hi : v);
}

static inline int uclamp(int v, int lo, int hi)
{
	return lo < hi ? clamp(v, lo, hi) : clamp(v, hi, lo);
}

static inline int fcol(int r, int c, int f)
{
	return 3 & (f >> ((((r << 1) & 2) + (c & 1)) << 1));
}

static inline int square(int x)
{
	return x * x;
}


/* 估计白平衡。RGB 顺序 */
CExport void
est_wbgain(ushort const* byr, int height, int width, int pat, float* wbrgb)
{
	int const lo = 256, hi = 65535 - 256;
	assert(width <= SHRT_MAX && lo < hi);
	int i[4] =
	{
		fcol(0, 0, pat), fcol(0, 1, pat),
		fcol(1, 0, pat), fcol(1, 1, pat),
	};
	double SUM[3] = { 0, 0, 0 };
	int line[4];

	for (int h = 0; h < height; h += 2)
	{
		ushort const* S0 = byr + h * width;
		ushort const* S1 = S0 + width;
		line[0] = line[1] = line[2] = line[3] = 0;
		for (int w = 0; w < width; w += 2)
			if (lo <= S0[w] && S0[w] <= hi
				&& lo <= S0[w + 1] && S0[w + 1] <= hi
				&& lo <= S1[w] && S1[w] <= hi
				&& lo <= S1[w + 1] && S1[w + 1] <= hi)
			{
				line[0] += S0[w]; line[1] += S0[w + 1];
				line[2] += S1[w]; line[3] += S1[w + 1];
			}
		SUM[i[0]] += line[0]; SUM[i[1]] += line[1];
		SUM[i[2]] += line[2]; SUM[i[3]] += line[3];
	}

	if (SUM[0] <= lo || SUM[1] <= lo || SUM[2] <= lo)
		wbrgb[0] = wbrgb[1] = wbrgb[2] = 1.F;
	else
	{
		wbrgb[0] = static_cast<float>(0.5 * SUM[1] / SUM[0]);
		wbrgb[2] = static_cast<float>(0.5 * SUM[1] / SUM[2]);
		wbrgb[1] = 1.F;
	}
}


static void fill_bgr(ushort const* src, vec3w* dst,
	int height, int width, int pat)
{
	int i[4] =
	{
		fcol(0, 0, pat), fcol(0, 1, pat) + 3,
		fcol(1, 0, pat), fcol(1, 1, pat) + 3,
	};

	for (int h = 0; h < height; h += 2)
	{
		ushort const* S0 = src + h * width;
		ushort const* S1 = S0 + width;
		ushort* D0 = reinterpret_cast<ushort*>(dst + h * width);
		ushort* D1 = D0 + 3 * width;
		for (int w = 0; w < width; w += 2)
		{
			D0[i[0]] = S0[w]; D0[i[1]] = S0[w + 1];
			D1[i[2]] = S1[w]; D1[i[3]] = S1[w + 1];
			D0 += 6; D1 += 6;
		}
	}
}


static void border_interpolate(vec3w* img,
	unsigned height, unsigned width, unsigned border, int pat)
{
	unsigned S[8];
	unsigned h, w, y, x, f;

	for (h = 0; h < height; ++h)
	{
		vec3w* line = img + h * width;
		for (w = 0; w < width; ++w)
		{
			if (w == border && border <= h && (h + border) < height)
				w = width - border;
			memset(S, 0, sizeof(S));
			for (y = h - 1; y != h + 2; ++y)
			{
				for (x = w - 1; x != w + 2; ++x)
					if (y < height && x < width)
					{
						f = fcol(y, x, pat);
						S[f] += img[y * width + x][f];
						++(S[f + 4]);
					}
			}
			f = fcol(h, w, pat);
			for (y = 0; y < 3; ++y)
			{
				if (y != f && S[y + 4])
					line[w][y] = static_cast<ushort>((S[y] + S[y + 4] / 2) / S[y + 4]);
			}
		}
	}
}


static void cielab(ushort const* rgb, short* lab)
{
	float xyz[3];
	static float cbrt_tab[65536], xyz_cam[3][4];
	static float const xyz_rgb[3][3] = {
		{ 0.412453F, 0.357580F, 0.180423F },
		{ 0.212671F, 0.715160F, 0.072169F },
		{ 0.019334F, 0.119193F, 0.950227F },
	};
	static float const rgb_cam[3][3] = {
		{ +1.26195443F, -0.45776108F, +0.19580664F },
		{ -0.15059669F, +1.13350368F, +0.01709299F },
		{ -0.01468136F, -0.36106369F, +1.37574506F } };
	static float const d65_white[3] = { 0.950456F, 1, 1.088754F };

	if (!rgb)
	{
		for (int i = 0; i < 65536; ++i)
		{
			double r = i / 65535.0;
			r = r > 0.008856 ? std::cbrt(r) : (7.787 * r + 16 / 116.0);
			cbrt_tab[i] = static_cast<float>(r);
		}
		for (int i = 0; i < 3; ++i)
			for (int c = 0; c < 3; ++c)
			{
				double t = 0;
				for (int k = 0; k < 3; ++k)
					t += xyz_rgb[i][k] * rgb_cam[k][c] / d65_white[i];
				xyz_cam[i][c] = static_cast<float>(t);
			}
		return;
	}

	xyz[0] = xyz[1] = xyz[2] = 0.5;
	for (int c = 0; c < 3; ++c)
	{
		xyz[0] += xyz_cam[0][c] * rgb[c];
		xyz[1] += xyz_cam[1][c] * rgb[c];
		xyz[2] += xyz_cam[2][c] * rgb[c];
	}
	xyz[0] = cbrt_tab[clamp(static_cast<int>(xyz[0]), 0, 65535)];
	xyz[1] = cbrt_tab[clamp(static_cast<int>(xyz[1]), 0, 65535)];
	xyz[2] = cbrt_tab[clamp(static_cast<int>(xyz[2]), 0, 65535)];
	lab[0] = static_cast<short>(64 * (116 * xyz[1] - 16));
	lab[1] = static_cast<short>(64 * 500 * (xyz[0] - xyz[1]));
	lab[2] = static_cast<short>(64 * 200 * (xyz[1] - xyz[2]));
}


static void lin_interpolate(ushort(*img)[3], int height, int width, int pat)
{
	int const TS = 16;
	int const hstop = height - 1, wstop = width - 1;
	int code[TS][TS][32];
	int S[4];

	border_interpolate(img, height, width, 1, pat);

	for (int h = 0; h < TS; ++h)
		for (int w = 0; w < TS; ++w)
		{
			int* ip = code[h][w] + 1;
			int f = fcol(h, w, pat);
			memset(S, 0, sizeof(S));
			for (int y = -1; y <= 1; ++y)
				for (int x = -1; x <= 1; ++x)
				{
					int shift = (y == 0) + (x == 0);
					int c = fcol(h + y, w + x, pat);
					if (c == f) continue;
					*ip++ = (width * y + x) * 3 + c;
					*ip++ = shift;
					*ip++ = c;
					S[c] += 1 << (shift);
				}
			code[h][w][0] = static_cast<int>(ip - code[h][w]) / 3;
			for (int c = 0; c < 3; ++c)
				if (c != f)
				{
					*ip++ = c;
					*ip++ = 256 / S[c];
				}
		}

	for (int h = 1; h < hstop; ++h)
		for (int w = 1; w < wstop; ++w)
		{
			ushort* P = img[h * width + w];
			int const* ip = code[h % TS][w % TS];
			memset(S, 0, sizeof(S));
			for (int i = *ip++; i--; ip += 3)
				S[ip[2]] += (P[ip[0]] << ip[1]);
			for (int i = 3; --i; ip += 2)
				P[ip[0]] = static_cast<ushort>((S[ip[0]] * ip[1]) >> 8);
		}
}


static void ppg_interpolate(ushort(*img)[3], int height, int width, int pat)
{
	int const dir[5] = { 1, width, -1, -width, 1 };
	int h_stop = height - 3;
	int w_stop = width - 3;
	int diff[2], guess[2];
	vec3w* P = nullptr;

	border_interpolate(img, height, width, 3, pat);

	/* 填充 green 层，使用梯度和图案模式识别 */
	for (int h = 3; h < h_stop; ++h)
	{
		// w 绿色是 1，其他色是 0 (0 & 1 或 2 & 1)
		int w = 3 + (fcol(h, 3, pat) & 1), c = fcol(h, w, pat);
		P = img + h * width + w;
		for (; w < w_stop; w += 2, P += 2)
		{
			int i, d, d2, d3;
			for (i = 0; i < 2; ++i)
			{
				d = dir[i]; d2 = d + d; d3 = d2 + d;
				guess[i] = 2 * (P[-d][1] + P[0][c] + P[d][1])
					- P[-d2][c] - P[d2][c];
				diff[i] = 3 * (std::abs(P[-d2][c] - P[0][c])
					+ std::abs(P[d2][c] - P[0][c])
					+ std::abs(P[-d][1] - P[d][1]))
					+ 2 * (std::abs(P[d3][1] - P[d][1])
						+ std::abs(P[-d3][1] - P[-d][1]));
			}
			i = diff[0] > diff[1]; d = dir[i];
			d = uclamp(guess[i] / 4, P[d][1], P[-d][1]);
			P[0][1] = static_cast<ushort>(d);
		}
	}

	/* 计算绿色像素上的红色和蓝色 */
	h_stop = height - 1;
	w_stop = width - 1;
	for (int h = 1; h < h_stop; ++h)
	{
		int w = 1 + (fcol(h, 2, pat) & 1), c = fcol(h, w + 1, pat);
		P = img + h * width + w;
		for (; w < w_stop; w += 2, P += 2)
		{
			int i, d;
			for (i = 0; i < 2; c = 2 - c, ++i)
			{
				d = dir[i];
				d = (P[-d][c] + P[d][c] + 2 * P[0][1] - P[-d][1] - P[d][1]) / 2;
				P[0][c] = static_cast<ushort>(clamp(d, 0, 65535));
			}
		}
	}

	/* 计算红色上的蓝色和蓝色上的红色 */
	for (int h = 1; h < h_stop; ++h)
	{
		int w = 1 + (fcol(h, 1, pat) & 1), c = 2 - fcol(h, w, pat);
		P = img + h * width + w;
		for (; w < w_stop; w += 2, P += 2)
		{
			int i, d;
			for (i = 0; i < 2; ++i)
			{
				d = dir[i] + dir[i + 1];
				diff[i] = std::abs(P[-d][c] - P[d][c])
					+ std::abs(P[-d][1] - P[0][1]) + std::abs(P[d][1] - P[0][1]);
				guess[i] = P[-d][c] + P[d][c] + 2 * P[0][1] - P[-d][1] - P[d][1];
			}
			if (diff[0] != diff[1])
				d = guess[diff[0] > diff[1]] / 2;
			else
				d = (guess[0] + guess[1]) / 4;
			P[0][c] = static_cast<ushort>(clamp(d, 0, 65535));
		}
	}
}


static void ahd_interpolate(ushort(*img)[3], int height, int width, int pat)
{
	int const TS = 256; // 128K 一级缓存
	int const TS6 = TS - 6;
	int const dir[4] = { -1, 1, -TS, TS };
	int ldiff[2][4], abdiff[2][4], leps, abeps, hm[2];
	int wth2 = width + width;

	vec3w(*rgb)[TS][TS], *rix, *P;
	vec3s(*lab)[TS][TS], *lix;
	char(*homo)[TS][TS], *buffer;
	buffer = static_cast<char*>(malloc(26 * TS * TS));

	cielab(nullptr, nullptr);
	border_interpolate(img, height, width, 5, pat);

	rgb = reinterpret_cast<vec3w(*)[TS][TS]>(buffer);
	lab = reinterpret_cast<vec3s(*)[TS][TS]>(buffer + 12 * TS * TS);
	homo = reinterpret_cast<char(*)[TS][TS]>(buffer + 24 * TS * TS);

	/* 切出 TS6×TS6 的块，然后往外 3×3 以得到 TS×TS 的取样区域 */
	for (int h_start = 5; h_start < height - 5; h_start += TS6)
		for (int w_start = 5; w_start < width - 5; w_start += TS6)
		{
			/* 插值水平和竖直方向的绿色 */
			int const h_border = min(height - 5, h_start + TS6);
			int const h_stop[4] = { h_border, h_border + 1, h_border + 2, h_border + 3 };
			int const w_border = min(width - 5, w_start + TS6);
			int const w_stop[4] = { w_border, w_border + 1, w_border + 2, w_border + 3 };
			int const top = h_start - 3, left = w_start - 3;

			for (int h = top; h < h_stop[3]; ++h)
			{
				int tr = h - top, tc, val;
				int w = left + (fcol(h, left, pat) & 1);
				int c = fcol(h, w, pat);
				P = img + h * width + w;
				for (; w < w_stop[3]; w += 2, P += 2)
				{
					tc = w - left;
					val = (2 * (P[-1][1] + P[0][c] + P[1][1])
						- P[-2][c] - P[2][c]) / 4;
					rgb[0][tr][tc][1] = static_cast<ushort>
						(uclamp(val, P[-1][1], P[1][1]));
					val = (2 * (P[-width][1] + P[0][c] + P[width][1])
						- P[-wth2][c] - P[wth2][c]) / 4;
					rgb[1][tr][tc][1] = static_cast<ushort>
						(uclamp(val, P[-width][1], P[width][1]));
				}
			}

			/* 插值红色和蓝色，同时转换到 Lab */
			for (int d = 0; d < 2; ++d)
				for (int h = top + 1; h < h_stop[2]; ++h)
				{
					int tr = h - top, w = left + 1, tc, val;
					P = img + h * width + w;
					for (; w < w_stop[2]; ++w, ++P)
					{
						tc = w - left;
						rix = &(rgb[d][tr][tc]);
						lix = &(lab[d][tr][tc]);
						int c = 2 - fcol(h, w, pat);
						if (c == 1)
						{
							c = fcol(h + 1, w, pat);
							val = P[0][1] + ((P[-1][2 - c] + P[1][2 - c]
								- rix[-1][1] - rix[1][1]) / 2);
							rix[0][2 - c] = static_cast<ushort>(clamp(val, 0, 65535));
							val = P[0][1] + ((P[-width][c] + P[width][c]
								- rix[-TS][1] - rix[TS][1]) / 2);
						}
						else
						{
							val = rix[0][1] + ((1
								+ P[-1 - width][c] + P[1 - width][c]
								+ P[-1 + width][c] + P[1 + width][c]
								- rix[-1 - TS][1] - rix[1 - TS][1]
								- rix[-1 + TS][1] - rix[1 + TS][1]) / 4);
						}
						rix[0][c] = static_cast<ushort>(clamp(val, 0, 65535));
						c = fcol(h, w, pat);
						rix[0][c] = P[0][c];
						cielab(rix[0], lix[0]);
					}
				}

			/* 构建 Lab 相似映射 */
			memset(homo, 0, 2 * TS * TS);
			for (int h = top + 2; h < h_stop[1]; ++h)
			{
				int w = left + 2, tr = h - top, tc;
				for (; w < w_stop[1]; ++w)
				{
					tc = w - left;
					for (int d = 0; d < 2; ++d)
					{
						lix = &(lab[d][tr][tc]);
						for (int i = 0; i < 4; ++i)
						{
							ldiff[d][i] = std::abs(lix[0][0] - lix[dir[i]][0]);
							abdiff[d][i] = square(lix[0][1] - lix[dir[i]][1])
								+ square(lix[0][2] - lix[dir[i]][2]);
						}
					}
					leps = min(max(ldiff[0][0], ldiff[0][1]), max(ldiff[1][2], ldiff[1][3]));
					abeps = min(max(abdiff[0][0], abdiff[0][1]), max(abdiff[1][2], abdiff[1][3]));
					for (int d = 0; d < 2; ++d)
						for (int i = 0; i < 4; ++i)
						{
							if (ldiff[d][i] <= leps && abdiff[d][i] <= abeps)
								++(homo[d][tr][tc]);
						}
				}
			}

			/* 结合最相似的像素，得到结果 */
			for (int h = top + 3; h < h_stop[0]; ++h)
			{
				int w = left + 3, tr = h - top, tc;
				P = img + h * width;
				for (; w < w_stop[0]; ++w)
				{
					tc = w - left;
					for (int d = 0; d < 2; ++d)
					{
						hm[d] = 0;
						for (int dy = tr - 1; dy <= tr + 1; ++dy)
							for (int dx = tc - 1; dx <= tc + 1; ++dx)
								hm[d] += homo[d][dy][dx];
					}
					if (hm[0] != hm[1])
						for (int c = 0; c < 3; ++c)
							P[w][c] = rgb[hm[1] > hm[0]][tr][tc][c];
					else
						for (int c = 0; c < 3; ++c)
							P[w][c] = (rgb[0][tr][tc][c] + rgb[1][tr][tc][c] + 1) / 2;
				}
			}
		}
	free(buffer);
}


CExport void
demosaic(ushort const* byr, ushort(*img)[3], int height, int width, int pat,
	int method)
{
	fill_bgr(byr, img, height, width, pat);
	if (method == 0)
		lin_interpolate(img, height, width, pat);
	else if (method == 2)
		ppg_interpolate(img, height, width, pat);
	else if (method == 3)
		ahd_interpolate(img, height, width, pat);
	else
		assert(false && "unsupported method code");
}


CExport void
raw_read(uchar const* P, ushort* S, int buflen, int height, int width,
	int depth, int pack)
{
	int line = width * depth / 8;
	int step = (line + 15) & -16;
	assert((height | width) % 2 == 0);
	assert(!pack || (depth == 10 || depth == 12));
	assert(0 <= pack && pack <= 2);
	assert(step * height <= buflen);

	if (pack == 0)
		memcpy(S, P, sizeof(ushort) * height * width);
	else if (pack == 1)
		for (int h = 0; h < height; ++h)
		{
			// 5 -> 4
			if (depth == 10)
				for (int i = 0; i < width; i += 4)
				{
					S[i + 0] = (P[0] << 2) | ((P[4] >> 0) & 0x3);
					S[i + 1] = (P[1] << 2) | ((P[4] >> 2) & 0x3);
					S[i + 2] = (P[2] << 2) | ((P[4] >> 4) & 0x3);
					S[i + 3] = (P[3] << 2) | ((P[4] >> 6) & 0x3);
					P += 5;
				}
			// 3 -> 2
			else if (depth == 12)
				for (int i = 0; i < width; i += 2)
				{
					S[i + 0] = (P[0] << 4) | ((P[2] >> 0) & 0xf);
					S[i + 1] = (P[1] << 4) | ((P[2] >> 4) & 0xf);
					P += 3;
				}
			P += step - line;
			S += width;
		}
	else if (pack == 2)
		for (int h = 0; h < height; ++h)
		{
			// 8+2, 6+4, 4+6, 2+8
			if (depth == 10)
				for (int i = 0; i < width; i += 4)
				{
					S[i + 0] = ((P[0])) | ((P[1] & 0x03) << 8);
					S[i + 1] = ((P[1] >> 2) & 0x3f) | ((P[2] & 0x0f) << 6);
					S[i + 2] = ((P[2] >> 4) & 0x0f) | ((P[3] & 0x3f) << 4);
					S[i + 4] = ((P[3] >> 6) & 0x03) | ((P[4] << 2));
					P += 5;
				}
			// 8+4, 4+8
			else if (depth == 12)
				for (int i = 0; i < width; i += 2)
				{
					S[i + 0] = ((P[0])) | ((P[1] & 0xf) << 8);
					S[i + 1] = ((P[1] >> 4) & 0xf) | (P[2] << 4);
					P += 3;
				}
			P += step - line;
			S += width;
		}
}
