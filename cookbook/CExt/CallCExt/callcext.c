#include <Python.h>
#include "cext.h"

/* int gcd(int x, int y); */
static PyObject* py_gcd(PyObject* self, PyObject* args)
{
	int x, y, result;
	if (!PyArg_ParseTuple(args, "ii", &x, &y))
		return NULL;
	result = gcd(x, y);
	return Py_BuildValue("i", result);
}

/* int inMandelbrot(double x0, double y0, int n); */
static PyObject* py_in_mandelbrot(PyObject* self, PyObject* args)
{
	double x0, y0;
	int n, result;
	if (!PyArg_ParseTuple(args, "ddi", &x0, &y0, &n))
		return NULL;
	result = inMandelbrot(x0, y0, n);
	return Py_BuildValue("i", result);
}

/* int divide(int a, int b, int *remainder); */
static PyObject* py_divide(PyObject* self, PyObject* args)
{
	int a, b, quotient, remainder;
	if (!PyArg_ParseTuple(args, "ii", &a, &b))
		return NULL;
	quotient = divide(a, b, &remainder);
	return Py_BuildValue("(ii)", quotient, remainder);
}

/* 模块方法列表 */
static PyMethodDef methodTable[] =
{
	{"gcd", py_gcd, METH_VARARGS, "最大公约数"},
	{"in_mandelbrot", py_in_mandelbrot, METH_VARARGS, "Mandelbrot 集合测试"},
	{"divide", py_divide, METH_VARARGS, "整数除法"},
	{NULL, NULL, 0x0, NULL},
};

/* 模块结构 */
static PyModuleDef callcextModule =
{
	PyModuleDef_HEAD_INIT,
	"callcext", /* 模块名 */
	"Call C Extension", /* 模块描述 */
	-1, /* 预解释器状态尺寸 */
	methodTable, /* 方法列表 */
};

/* 模块初始化函数 */
PyMODINIT_FUNC PyInit_callcext(void)
{
	return PyModule_Create(&callcextModule);
}
