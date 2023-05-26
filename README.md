# NaN
## Discription
This is a linear algebra library like Numpy, with less utilities kernels such as
a lot of the array manipulation functionalities. The goal of this libarary is to 
run matrix calculation on both CPU and GPU, so more functions will be implemented
in the near future. Rigth now the following kernels are available.
### matrix generation kernels
1. eye
2. zeros
3. randn(normal distribution)
4. rand(uniform distribution)
5. rot2
6. rot3

### matrix math kernels
1. add/substract
2. matmul
3. eigenvalue decomposition
4. SVD
5. LU Decomposition
6. matrix inverse
7. pseudo-inverse for non-square matrix

## Some Example
```python
from NaN.lib import matGen as mg
from NaN.lib import ops
from NaN.matrix import matrix

# to create a matrix
a = matrix([[1,2,3],[2,3,4],[5,6,7]], 'double')
# to generate a matrix with normal distribution value
# with mean of 0 and std of 1
a = mg.randn((2, 3), (0, 1), 'double')
# to generate a matrix with uniform distribution value
# from 0 to 5
b = mg.rand((3, 2), (0, 5), 'double')
# do a matmul
c = a*b

# do a Singlar Value Decomposition
u,s,vt = ops.svd(c)
```

## Requirements
Installation of BLAS in pip is very slow and the performance is not great
either, so we recommand using a conda environment for optimal performance(see BLAS Recommandation)

## Installation
1. run "pip install ." to install the library

## TODO
1. QR and Chol decomposition
2. solvers
3. outter/inner/dot/kron product
4. GPU support

## BLAS Recommandation
It is highly recommanded that you use a conda environment for this
library since it provides a much faster BLAS compared to pip. To install
BLAS from conda, type in: 
```console
foo@whoami:~$ conda install -c anaconda openblas
```
before you pip install this library



