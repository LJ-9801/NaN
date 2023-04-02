from NaN.lib import ops as op
from NaN.lib import matGen as mg
from NaN.matrix import matrix
from NaN.matrix import utils


N = 2048
A = mg.randn((N, N), (0, 1), 'double')
B = mg.randn((N, N), (0, 1), 'double')
for i in range(10000):
    A = A*B*A


