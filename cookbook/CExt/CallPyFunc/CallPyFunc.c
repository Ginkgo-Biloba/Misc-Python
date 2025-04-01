#include <Python.h>

/** 在 Python 解释器中执行函数 func(x, y) */
/* 参数和返回值必须是 Python float 类型 */
double callFunc(PyObject* func, double x, double y)
{
	PyObject* args;
	PyObject* kw;
	PyObject* result = NULL;
	double retVal;

	/* 确保我们拥有 GIL */
	PyGILState_STATE GILState = PyGILState_Ensure();

	/* 验证函数 func 可调用 */
	if (!PyCallable_Check(func))
	{
		fprintf(stderr, "\n不可调用的函数");
		goto lableFail;
	}

	/* 构建参数 */
	args = Py_BuildValue("(dd)", x, y);
	kw = NULL;

	/* 调用函数 */
	result = PyObject_Call(func, args, kw);
	Py_DECREF(args);
	Py_XDECREF(kw); /* 允许传递 NULL 指针 */

	/* 检查是否有异常发生 */
	if (PyErr_Occurred() != NULL)
	{
		PyErr_Print();
		goto lableFail;
	}

	/* 验证结果是浮点对象 */
	if (!PyFloat_Check(result))
		fprintf(stderr, "\n函数并不返回一个 Python float 对象");

	/* 拿到返回值 */
	retVal = PyFloat_AsDouble(result);
	Py_DECREF(result);

	/* 返回先前的 GIL 状态，并返回值 */
	PyGILState_Release(GILState);
	return retVal;

lableFail:
	Py_XDECREF(result);
	PyGILState_Release(GILState);
	abort(); // 先这么干吧
}

/* 从模块中加载符号 */
PyObject* importName(char const* moduleName, char const* symbol)
{
	PyObject* unitName = PyUnicode_FromString(moduleName);
	PyObject* moudle = PyImport_Import(unitName);
	Py_DECREF(unitName);
	return PyObject_GetAttrString(moudle, symbol);
}

/* 简单的示例 */
int main()
{
	PyObject* powFunc;
	double x;
	Py_Initialize();

	/* 获取函数 math.pow 的引用*/
	powFunc = importName("math", "pow");

	/* 使用 callFunc 调用函数 */
	for (x = 0.0; x < 5.0; x += 0.3)
		printf("\n%.2lf -> %.2lf", x, callFunc(powFunc, x, 1.5));

	/* 结束，清理 */
	Py_DECREF(powFunc);
	Py_Finalize();
	printf("\n");
	return 0;
}