import ctypes, ctypes.util
import os
from nan.core import MATGEN

# find CBLAS
cblas = ctypes.util.find_library('blas')
cblas_lib = ctypes.cdll.LoadLibrary(cblas)

# find LAPACK
lapack = ctypes.util.find_library('lapack')
lp_lib = ctypes.cdll.LoadLibrary(lapack)


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

    def _dscal(A, shape, alpha, N):
        cblas_lib.cblas_dscal.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_dscal.restype = None
        cblas_lib.cblas_dscal(shape[0]*shape[1], alpha, A, N)
        return A
    
    def _sscal(A, shape, alpha, N=1):
        cblas_lib.cblas_sscal.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        cblas_lib.cblas_sscal.restype = None
        cblas_lib.cblas_sscal(shape[0]*shape[1], alpha, A, N)
        return A

    def _dgemm(A, B, Ashape, Bshape, Alayout=111, Blayout =111):
        out_dim = (Ashape[0], Bshape[1])
        C = (ctypes.c_double*(out_dim[0]*out_dim[1]))()
        C = ctypes.POINTER(ctypes.c_double)(C)
        cblas_lib.cblas_dgemm.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, 
                                        ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double),
                                         ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double,
                                           ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_dgemm.restype = None  
        cblas_lib.cblas_dgemm(101, Alayout, Blayout, Ashape[0], Bshape[1], Ashape[1], 1.0, A, Ashape[1], B, Bshape[1], 0.0, C, out_dim[1])
        return C

    def _sgemm(A, B, Ashape, Bshape, Alayout=111, Blayout =111):
        out_dim = (Ashape[0], Bshape[1])
        C = (ctypes.c_float*(out_dim[0]*out_dim[1]))()
        C = ctypes.POINTER(ctypes.c_float)(C)
        cblas_lib.cblas_sgemm.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, 
                                        ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float),
                                         ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_float,
                                           ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        cblas_lib.cblas_sgemm.restype = None  
        cblas_lib.cblas_sgemm(101, Alayout, Blayout, Ashape[0], Bshape[1], Ashape[1], 1.0, A, Ashape[1], B, Bshape[1], 0.0, C, out_dim[1])
        return C
    
    def _dtranspose(A, shape):
        id = MATGEN._deye(shape[0]).data
        C = (ctypes.c_double*(shape[0]*shape[1]))()
        C = ctypes.POINTER(ctypes.c_double)(C)
        cblas_lib.cblas_dgemm.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, 
                                        ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double),
                                         ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double,
                                           ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_dgemm.restype = None  
        cblas_lib.cblas_dgemm(101, 112, 111, shape[1], shape[0], shape[0], 1.0, A, shape[1], id, shape[0], 0.0, C, shape[0])
        return C
    
    def _stranspose(A, shape):
        id = MATGEN._seye(shape[0]).data
        C = (ctypes.c_float*(shape[0]*shape[1]))()
        C = ctypes.POINTER(ctypes.c_float)(C)
        cblas_lib.cblas_sgemm.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, 
                                        ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float),
                                         ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_float,
                                           ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        cblas_lib.cblas_sgemm.restype = None
        cblas_lib.cblas_sgemm(101, 112, 111, shape[1], shape[0], shape[0], 1.0, A, shape[1], id, shape[0], 0.0, C, shape[0])
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
        C = MemOps._scopy(A, shape)
        cblas_lib.cblas_saxpy.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        cblas_lib.cblas_saxpy.restype = None
        cblas_lib.cblas_saxpy(shape[0]*shape[1], -1.0, B, 1, C, 1)
        return C

    def _dsub(A, B, shape):
        C = MemOps._dcopy(A, shape)
        cblas_lib.cblas_daxpy.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        cblas_lib.cblas_daxpy.restype = None
        cblas_lib.cblas_daxpy(shape[0]*shape[1], -1.0, B, 1, C, 1)
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
    
    def _deig(A, shape):
        out = MemOps._dcopy(A, shape)
        wr = (ctypes.c_double*(shape[0]))()
        wi = (ctypes.c_double*(shape[0]))()
        jobvl = ctypes.c_char(b'N')
        jobvr = ctypes.c_char(b'V')
        vl = (ctypes.c_double*(shape[0]*shape[0]))()
        vr = (ctypes.c_double*(shape[0]*shape[0]))()
        lp_lib.LAPACKE_dgeev.argtypes = [ctypes.c_int, ctypes.c_char, ctypes.c_char, ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                                         ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        info = lp_lib.LAPACKE_dgeev(101, jobvl, jobvr, shape[0], out, shape[1], wr, wi, vl, shape[0], vr, shape[0])
        if info != 0:
            raise Exception("LAPACKE_dgeev failed with error code {}".format(info))
        return wr, wi, vr
    
    def _seig(A, shape):
        out = MemOps._scopy(A, shape)
        wr = (ctypes.c_float*(shape[0]))()
        wi = (ctypes.c_float*(shape[0]))()
        jobvl = ctypes.c_char(b'N')
        jobvr = ctypes.c_char(b'V')
        vl = (ctypes.c_float*(shape[0]*shape[0]))()
        vr = (ctypes.c_float*(shape[0]*shape[0]))()
        lp_lib.LAPACKE_sgeev.argtypes = [ctypes.c_int, ctypes.c_char, ctypes.c_char, ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_float),
                                         ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_float), ctypes.c_int]
        info = lp_lib.LAPACKE_sgeev(101, jobvl, jobvr, shape[0], out, shape[1], wr, wi, vl, shape[0], vr, shape[0])
        if info != 0:
            raise Exception("LAPACKE_sgeev failed with error code {}".format(info))
        return wr, wi, vr
    
    def _dsvd(A, shape, routine = False):
        aout = MemOps._dcopy(A, shape)
        mind = min(shape[0], shape[1])
        s = (ctypes.c_double*(mind))()
        u = (ctypes.c_double*(shape[0]*shape[0]))()
        vt = (ctypes.c_double*(shape[1]*shape[1]))()
        superb = (ctypes.c_double*(mind-1))()
        lp_lib.LAPACKE_dgesvd.argtypes = [ctypes.c_int, ctypes.c_char, ctypes.c_char, ctypes.c_int, ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                                          ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                                          ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        info = lp_lib.LAPACKE_dgesvd(101, b'A', b'A', shape[0], shape[1], aout, shape[1], s, u, shape[0], vt, shape[1], shape[0], superb)
        if info != 0:
            raise Exception("LAPACKE_dgesvd failed with error code {}".format(info))
        if routine is True: return u, s, vt
        sout = (ctypes.c_double*(shape[0]*shape[1]))()
        for i in range(mind): sout[i*shape[1]+i] = s[i]
        return u, sout, vt
        
    
    def _ssvd(A, shape, routine = False):
        aout = MemOps._scopy(A, shape)
        mind = min(shape[0], shape[1])
        s = (ctypes.c_float*(mind))()
        u = (ctypes.c_float*(shape[0]*shape[0]))()
        vt = (ctypes.c_float*(shape[1]*shape[1]))()
        superb = (ctypes.c_float*(mind-1))()
        lp_lib.LAPACKE_sgesvd.argtypes = [ctypes.c_int, ctypes.c_char, ctypes.c_char, ctypes.c_int, ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_float),
                                          ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_float),
                                          ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
        info = lp_lib.LAPACKE_sgesvd(101, b'A', b'A', shape[0], shape[1], aout, shape[1], s, u, shape[0], vt, shape[1], shape[0], superb)
        if info != 0:
            raise Exception("LAPACKE_sgesvd failed with error code {}".format(info))
        if routine is True: return u, s, vt
        sout = (ctypes.c_float*(shape[0]*shape[1]))()
        for i in range(mind): sout[i*shape[1]+i] = s[i]
        return u, sout, vt
    
    # LU decomposition
    def _dgetrf(A, shape):
        out = MemOps._dcopy(A, shape)
        dmin = min(shape[0], shape[1])
        ipiv = (ctypes.c_int*dmin)()
        lp_lib.LAPACKE_dgetrf.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        info = lp_lib.LAPACKE_dgetrf(101, shape[0], shape[1], out, shape[1], ipiv)
        if info != 0:
            raise Exception("LAPACKE_dgetrf failed with error code {}".format(info))
        return out, ipiv
    
    def _sgetrf(A, shape):
        out = MemOps._scopy(A, shape)
        dmin = min(shape[0], shape[1])
        ipiv = (ctypes.c_int*dmin)()
        lp_lib.LAPACKE_sgetrf.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        info = lp_lib.LAPACKE_sgetrf(101, shape[0], shape[1], out, shape[1], ipiv)
        if info != 0:
            raise Exception("LAPACKE_sgetrf failed with error code {}".format(info))
        return out, ipiv
    
    def _dgetri(A, ipiv, shape):
        out = MemOps._dcopy(A, shape)
        ipiv = (ctypes.c_int*(shape[0]))() if ipiv is None else ipiv
        lp_lib.LAPACKE_dgetri.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        info = lp_lib.LAPACKE_dgetri(101, shape[1], out, shape[1], ipiv)
        if info != 0:
            raise Exception("LAPACKE_dgetri failed with error code {}".format(info))
        return out
    
    def _sgetri(A, ipiv, shape):
        out = MemOps._scopy(A, shape)
        ipiv = (ctypes.c_int*(shape[0]))() if ipiv is None else ipiv
        lp_lib.LAPACKE_sgetri.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        info = lp_lib.LAPACKE_sgetri(101, shape[1], out, shape[1], ipiv)
        if info != 0:
            raise Exception("LAPACKE_sgetri failed with error code {}".format(info))
        return out
    
    def _dpinv(A, shape):
        dmin = min(shape[0], shape[1])
        u, s, vt = LAPACK._dsvd(A, shape, False)
        for i in range(dmin): 
            if s[i*dmin+i] > 1e-15: s[i*dmin+i] = 1/s[i*dmin+i]
        tmp = CBLAS._dgemm(vt, s, (shape[1], shape[1]), shape, 112, 111)
        return CBLAS._dgemm(tmp, u, shape, (shape[0], shape[0]), 111, 112)
    
    def _spinv(A, shape):
        dmin = min(shape[0], shape[1])
        u, s, vt = LAPACK._ssvd(A, shape, False)
        for i in range(dmin):
            if s[i*dmin+i] > 1e-15: s[i*dmin+i] = 1/s[i*dmin+i]
        tmp = CBLAS._sgemm(vt, s, (shape[1], shape[1]), shape, 112, 111)
        return CBLAS._sgemm(tmp, u, shape, (shape[0], shape[0]), 111, 112)
        
    def _dinv(A, shape):
        out, ipiv = LAPACK._dgetrf(A, shape)
        out = LAPACK._dgetri(out, ipiv, shape)
        return out
    
    def _sinv(A, shape):
        out, ipiv = LAPACK._sgetrf(A, shape)
        out = LAPACK._sgetri(out, ipiv, shape)
        return out
    
    def _dlu(A, shape):
        out, _ = LAPACK._dgetrf(A, shape)
        upper = (ctypes.c_double*(shape[0]*shape[1]))()
        lower = (ctypes.c_double*(shape[0]*shape[1]))()
        for i in range(shape[0]*shape[1]): 
            if i%shape[1] <= i//shape[1]: lower[i] = out[i]
            if i%shape[1] == i//shape[1]: upper[i] = 1.0
            if i%shape[1] > i//shape[1]: upper[i] = out[i]
        return lower, upper
    
    def _slu(A, shape):
        out, _ = LAPACK._sgetrf(A, shape)
        upper = (ctypes.c_float*(shape[0]*shape[1]))()
        lower = (ctypes.c_float*(shape[0]*shape[1]))()
        for i in range(shape[0]*shape[1]): 
            if i%shape[1] <= i//shape[1]: lower[i] = out[i]
            if int(i%shape[1]) == int(i//shape[1]): upper[i] = 1.0
            if i%shape[1] > i//shape[1]: upper[i] = out[i]
        return lower, upper
    
    

