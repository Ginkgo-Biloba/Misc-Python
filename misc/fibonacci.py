# coding = utf-8

def fibonacci(n):
	fkm1 = 1; fk = 0;
	while (n):
		fkp1 = fkm1 + fk;
		fkm1 = fk; fk = fkp1;
		n -= 1;
	return fk;


def fibMatrix(n):
	A = [1, 1, 1, 0]
	B = [1, 0, 0, 1]
	C = [0, 0, 0, 0]
	while (n):
		if (n & 1): # r *= x;
			C[0] = B[0] * A[0] + B[1] * A[2];
			C[1] = B[0] * A[1] + B[1] * A[3];
			C[2] = B[2] * A[0] + B[3] * A[2];
			C[3] = B[2] * A[1] + B[3] * A[3];
			B[0] = C[0]; B[1] = C[1]; B[2] = C[2]; B[3] = C[3];
		# x *= x
		C[0] = A[0] * A[0] + A[1] * A[2];
		C[1] = A[0] * A[1] + A[1] * A[3];
		C[2] = A[2] * A[0] + A[3] * A[2];
		C[3] = A[2] * A[1] + A[3] * A[3];
		A[0] = C[0]; A[1] = C[1]; A[2] = C[2]; A[3] = C[3];
		n = n >> 1
	return B[1]


def fibShift(n):
	# 其实应该减 1，但 0 的结果是 0，不能左移 -1 位
	mask = 1 << n.bit_length() 
	mask = mask >> 1
	fkm1 = 1; fk = 0
	while (mask):
		f2km1 = fk * fk + fkm1 * fkm1
		f2k = (fkm1 + fkm1 + fk) * fk
		if (mask & n):
			fkm1 = f2k
			fk = f2k + f2km1
		else:
			fkm1 = f2km1
			fk = f2k
		mask = mask >> 1
	return fk


for i in range(16): print(fibonacci(i), end=", ")
print()
for i in range(16): print(fibShift(i), end=", ")
print()
for i in range(16): print(fibMatrix(i), end=", ")

