# coding = utf-8
import inspect

def print_caller(func):
	def f(*args, **kws):
		stacks = inspect.stack();
		index = 1;
		stack = stacks[index]
		while (stack[1] == "<string>"):
			++index
			stack = stacks[index]
		print("In file:", stack[1])
		print("Line:", stack[2])
		print("Code:", "".join(stack[4]))
		return func(*args, **kws)
	return f

@print_caller
def f(a, b):
	return (a+b)

f(1, 2)
tmp = f
tmp(4, 5)
eval("f(5, 6)")
eval("eval('f(5, 6)')")