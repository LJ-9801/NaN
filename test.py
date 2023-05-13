from NaN.lib import matGen as mg
from NaN.matrix import matrix
from colorama import Fore
import numpy as np
import time


# font colors
red = Fore.RED
green = Fore.GREEN
success = green + 'Success' + Fore.RESET
fail = red + 'Fail' + Fore.RESET


t1 = time.monotonic()
N = 1024
# perform square matrix multiplication verifications
# ===================================================================
print('-' * 50)
print('Performing matrix multiplication verifications')
print('-' * 50)
print('Generate random matrices and perform matrix multiplication and addition')
A = mg.randn((N, N), (0, 1), 'double')
B = mg.randn((N, N), (-5, 5), 'double')
D = A+B+A
C = A*B*A
C = np.ctypeslib.as_array(C.data, (N,N))
A = np.ctypeslib.as_array(A.data, (N,N))
B = np.ctypeslib.as_array(B.data, (N,N))
D = np.ctypeslib.as_array(D.data, (N,N))
An = np.array(A, dtype=np.float64)
Bn = np.array(B, dtype=np.float64)
Cn = An @ Bn @ An
Dn = An + Bn + An
print(success if np.allclose(C, Cn) else fail)
print(success if np.allclose(D, Dn) else fail)
#assert np.allclose(C.data, Cn)
print("Testing rotation matrix generation and operations")
r = mg.rot2(45)
i = mg.randn((2, 1), (0, 1), 'float')
out = r*i
Rn = np.ctypeslib.as_array(r.data, (2,2))
In = np.ctypeslib.as_array(i.data, (2,1))
out = np.ctypeslib.as_array(out.data, (2,1))
outn = Rn @ In
print(success if np.allclose(out, outn) else fail)
print('-' * 50)
# ===================================================================
print('Testing other matrix generation')
print('-' * 50)
# testing zeros
print('Testing zeros')
z = mg.zeros((N, N), 'double')
zn = np.ctypeslib.as_array(z.data, (N,N))
print(success if np.allclose(zn, np.zeros((N, N))) else fail)
print('Testing eye')
identity = mg.eye(N, 'double')
identity = np.ctypeslib.as_array(identity.data, (N,N))
print(success if identity.all()==np.eye(N).all() else fail)
print("Testing Non-Squared matrix multiplication")
N1 = 100
N2 = 200
a = mg.randn((N1,N2), (0,1), 'double')
b = mg.randn((N2,N1), (0,1), 'double')
c = a*b*a
a = np.ctypeslib.as_array(a.data, (N1,N2))
b = np.ctypeslib.as_array(b.data, (N2,N1))
c = np.ctypeslib.as_array(c.data, (N1,N2))
an = np.array(a)
bn = np.array(b)
cn = an @ bn @ an
print(success if np.allclose(c, cn) else fail)
print("Testing float type matrices operation")
a = mg.randn((N1,N2), (0,1), 'float')
b = mg.randn((N2,N1), (0,1), 'float')
c = a*b
a = np.ctypeslib.as_array(a.data, (N1,N2))
b = np.ctypeslib.as_array(b.data, (N2,N1))
c = np.ctypeslib.as_array(c.data, (N1,N1))
an = np.array(a)
bn = np.array(b)
cn = an @ bn
print(success if np.allclose(c, cn) else fail)

print('-' * 50)
print('Testing Rotation matrix')
print('-' * 50)
v = matrix([[1],[1]], 'float')
v2 = matrix([[1],[1],[1]], 'float')
v_test = matrix([0,1], 'float')
r2 = mg.rot2(60)
r3 = mg.rot3(60, 0)
v = r2*v
v2 = r3*v2

r2 = np.ctypeslib.as_array(r2.data, (2,2))
r3 = np.ctypeslib.as_array(r3.data, (3,3))
v = np.ctypeslib.as_array(v.data, (2,1))
v2 = np.ctypeslib.as_array(v2.data, (3,1))

print(success if np.allclose(v, v2[1:]) else fail)
r2 = mg.rot2(30, "double")
r3 = mg.rot3(30, 1, "double")
r2 = np.ctypeslib.as_array(r2.data, (2,2))
r3 = np.ctypeslib.as_array(r3.data, (3,3))

r3 = matrix([[r3[0][0], r3[2][0]],[r3[0][2],r3[2][2]]], 'double')
r3 = np.ctypeslib.as_array(r3.data, (2,2))
print(success if np.allclose(r3, r2) else fail)
print('-' * 50)
r4 = r3.copy()
r5 = np.ctypeslib.as_array(r4.data, (2,2))
print(success if np.allclose(r5, r4) else fail)

N2 = 100
A = mg.randn((N2, N2), (0, 1), 'double')
B = A[0:5, 0:5]
A = np.ctypeslib.as_array(A.data, (N2,N2))
B = np.ctypeslib.as_array(B.data)
Bn = A[0:5, 0:5]
print(success if B.all()==Bn.all() else fail)
t = time.monotonic() - t1
print(f"Test completed in {t:.2f} seconds")