import ctypes, ctypes.util
import os

# find CBLAS
cblas = ctypes.util.find_library('openblas')
# load CBLAS
cblas_lib = ctypes.cdll.LoadLibrary(cblas)


class MemOps:
    def __init__(self) -> None:
        pass
    
    def _dcopy(A, shape):
        B = (ctypes.c_double*shape[0]*shape[1])()
        B = ctypes.POINTER(ctypes.c_double)(B)
        cblas_lib.cblas_dcopy.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_dcopy.restype = None
        cblas_lib.cblas_dcopy(shape[0]*shape[1], A, 1, B, 1)
        return B

    def _scopy(A, shape):
        B = (ctypes.c_float*shape[0]*shape[1])()
        B = ctypes.POINTER(ctypes.c_float)(B)
        cblas_lib.cblas_scopy.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        cblas_lib.cblas_scopy.restype = None
        cblas_lib.cblas_scopy(shape[0]*shape[1], A, 1, B, 1)
        return B


#BLAS routines
# matrix to matrix
class CBLAS:
    def __init__(self) -> None:
        pass

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
    
    def _dadd(A, B, shape):
        C = MemOps._dcopy(B, shape)
        cblas_lib.cblas_daxpy.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_daxpy.restype = None
        cblas_lib.cblas_daxpy(shape[0]*shape[1], 1.0, A, 1, C, 1)
        return C
    
    def _sadd(A, B, shape):
        C = MemOps._scopy(B, shape)
        cblas_lib.cblas_saxpy.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        cblas_lib.cblas_saxpy.restype = None
        cblas_lib.cblas_saxpy(shape[0]*shape[1], 1.0, A, 1, C, 1)
        return C
    
    def _ssub(A, B, shape):
        C = MemOps._scopy(B, shape)
        cblas_lib.cblas_saxpy.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        cblas_lib.cblas_saxpy.restype = None
        cblas_lib.cblas_saxpy(shape[0]*shape[1], -1.0, A, 1, C, 1)
        return C

    def _dsub(A, B, shape):
        C = MemOps._dcopy(B, shape)
        cblas_lib.cblas_daxpy.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_daxpy.restype = None
        cblas_lib.cblas_daxpy(shape[0]*shape[1], -1.0, A, 1, C, 1)
        return C


# LEVEL2 BLAS

# LEVEL3 BLAS
