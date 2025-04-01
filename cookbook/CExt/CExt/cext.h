#ifndef SAMPLE_H_INCLUDED
#define SAMPLE_H_INCLUDED

/* sample.c */

/* Compute the greatest common divisor */
_declspec(dllexport) int gcd(int x, int y);

/* Test if (x0, y0) is in the Mandelbrot set or not */
_declspec(dllexport) int inMandelbrot(double x0, double y0, int n);

/* Divide two numbers */
_declspec(dllexport) int divide(int a, int b, int *remainder);

/* Average values in an array */
_declspec(dllexport) double avg(double *a, int n);

/* A C data structure */
_declspec(dllexport) typedef struct SPoint
{
	double x;
	double y;
} Point;

/* Function involving a C data structure */
_declspec(dllexport) double distance(Point *p1, Point *p2);

#endif // SAMPLE_H_INCLUDED
