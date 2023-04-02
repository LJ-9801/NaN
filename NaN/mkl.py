import ctypes, ctypes.util
import os

# find CBLAS and LAPACK
cblas = ctypes.util.find_library('cblas')
lapack = ctypes.util.find_library('lapack')

# load CBLAS and LAPACK
lapack_lib = ctypes.cdll.LoadLibrary(lapack)
cblas_lib = ctypes.cdll.LoadLibrary(cblas)


# LEVEL1 BLAS
# matrix to matrix
class CBLAS:
    def _dgemm(A, B, Ashape, Bshape):
        out_dim = (Ashape[0], Bshape[1])
        C = (ctypes.c_double*out_dim[0]*out_dim[1])()
        C = ctypes.POINTER(ctypes.c_double)(C)
        cblas_lib.cblas_dgemm.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, 
                                        ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double),
                                         ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double,
                                           ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_dgemm.restype = None  
        cblas_lib.cblas_dgemm(101, 111, 111, Ashape[0], Bshape[1], Bshape[0], 1.0, A, Ashape[1], B, Bshape[1], 0.0, C, out_dim[1])
        return C

    def _sgemm(A, B, Ashape, Bshape):
        out_dim = (Ashape[0], Bshape[1])
        C = (ctypes.c_float*out_dim[0]*out_dim[1])()
        C = ctypes.POINTER(ctypes.c_float)(C)
        cblas_lib.cblas_sgemm.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, 
                                        ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float),
                                         ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_float,
                                           ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        cblas_lib.cblas_sgemm.restype = None  
        cblas_lib.cblas_sgemm(101, 111, 111, Ashape[0], Bshape[1], Bshape[0], 1.0, A, Ashape[1], B, Bshape[1], 0.0, C, out_dim[1])
        return C

# LEVEL2 BLAS

# LEVEL3 BLAS
