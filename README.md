# NaN
This is a linear algebra library like Numpy, it's not as fast, but it works.

## Requirement
you need to find out where blas and lapack shared library is installed in
your machine. If you had numpy installed, then these math kernals should exit in your OS. Simply locate the lapack and blas share library file and change the parameter in the ctypes find_library function in NaN/mkl.py and the requrement.py to the .so file or .dylib location specified in your machine.

If you are using this library in an X86 linux system, you will need to change 'kernals/build/mat_gen.dylib' in the NaN/core.py to 'kernals/build/mat_gen.so'. If you are using Darwin M1, you can just leave it as it is.

Note that this repository will be updated so that this step could be skipped in the near future

Once you have these directory changed, run "bash setup.sh" to setup the library. If every step is successful, you can now test the library using the test.py file.

## TODO
1. autofind blas and lapack kernals
2. matrix indexing is curretly not avaliable
3. matrix factorization to be implemented
4. dynamic typing


