import ctypes, ctypes.util
import os

# find CBLAS
cblas = ctypes.util.find_library('blas')
# load CBLAS
cblas_lib = ctypes.cdll.LoadLibrary(cblas)

# find LAPACK
lapack = ctypes.util.find_library('lapack')
lp_lib = ctypes.cdll.LoadLibrary(lapack)
print(lp_lib)


class MemOps:
    def __init__(self) -> None:
        pass

    
    
    def _dcopy(A, shape):
        B = (ctypes.c_double*(shape[0]*shape[1]))()
        B = ctypes.POINTER(ctypes.c_double)(B)
        cblas_lib.cblas_dcopy.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_dcopy.restype = None
        cblas_lib.cblas_dcopy(shape[0]*shape[1], A, 1, B, 1)
        return B

    def _scopy(A, shape):
        B = (ctypes.c_float*(shape[0]*shape[1]))()
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
        C = (ctypes.c_double*(out_dim[0]*out_dim[1]))()
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
        C = (ctypes.c_float*(out_dim[0]*out_dim[1]))()
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


#LAPACK routines
class LAPACK:
    def __init__(self) -> None:
        pass
    # convert to upper Hessenberg form
    def _dgehrd(A, shape):
        out = MemOps._dcopy(A, shape)
        tau = ctypes.POINTER(ctypes.c_double)((ctypes.c_double*(shape[0]-1))())
        lp_lib.LAPACKE_dgehrd.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]                                         
        info = lp_lib.LAPACKE_dgehrd(101, shape[0], 1, shape[0], out, shape[1], tau)
        if info != 0:
            raise Exception("LAPACKE_dgehrd failed with error code {}".format(info))
        return out, tau
    
    # generate orthogonal matrix from Hessenberg form
    def _dorghr(A, tau, shape):
        out = MemOps._dcopy(A, shape)
        lp_lib.LAPACKE_dorghr.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        info = lp_lib.LAPACKE_dorghr(101, shape[0], 1, shape[0], out, shape[1], tau)
        if info != 0:
            raise Exception("LAPACKE_dorghr failed with error code {}".format(info))
        return out
    
    # computes all eigenvalues of upper Hessenberg matrix
    def _dhseqr(A, tau, shape):
        out = MemOps._dcopy(A, shape)
        wr = (ctypes.c_double*(shape[0]))()
        wi = (ctypes.c_double*(shape[0]))()
        lp_lib.LAPACKE_dhseqr.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                                          ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
        info = lp_lib.LAPACKE_dhseqr(101, 111, 111, shape[0], out, shape[1], wr, wi, tau)
        if info != 0:
            raise Exception("LAPACKE_dhseqr failed with error code {}".format(info))
        return out, wr, wi
