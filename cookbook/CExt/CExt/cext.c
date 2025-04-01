/* callcfunc.c */
#include <math.h>
#include "cext.h"

/* 计算最大公约数 */
int gcd(int x, int y)
{
	int g = y;
	while (x > 0)
	{
		g = x;
		x = y % x;
		y = g;
	}
	return g;
}

/* 测试复数 (x0 + iy0) 是否在 Mandelbrot 集合里面 */
int inMandelbrot(double x0, double y0, int n)
{
	double x = 0.0;
	double y = 0.0;
	double xtemp;
	while (n > 0)
	{
		xtemp = x * x - y * y + x0;
		y = 2 * x * y + y0;
		x = xtemp;
		n -= 1;
		if (x * x + y * y > 4)
		{ return 0; }
	}
	return 1;
}

/* 计算两个数的除法 */
int divide(int a, int b, int *remainder)
{
	int quotient = a / b;
	*remainder = a % b;
	return quotient;
}

/* 浮点数组的平均值 */
double avg(double *a, int n)
{
	int i;
	double total = 0.0;
	for (i = 0; i < n; i++)
	{
		total += a[i];
	}
	return (total / n);
}

/* 使用 C 结构体的函数 */
double distance(Point *p1, Point *p2)
{
	return hypot(p1->x - p2->x, p1->y - p2->y);
}
