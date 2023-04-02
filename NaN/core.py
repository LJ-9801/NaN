from ctypes import *
lib = cdll.LoadLibrary("kernals/build/mat_gen.dylib")


class object:
    def __init__(self, data, shape, dtype):
        self.dtype = dtype
        self.shape = shape
        self.data = data


class MATGEN:
    def _drandn(size, length):
        ap = (c_double*size[0]*size[1])()
        lib.drandfill.argtypes = [c_int, c_double, c_double, c_double*size[0]*size[1]]
        lib.drandfill(size[0]*size[1], length[0], length[1], ap)
        ap = POINTER(c_double)(ap)
        return object(ap, size, 'double')

    def _srandn(size, length):
        ap = (c_float*size[0]*size[1])()
        lib.drandfill.argtypes = [c_int, c_float, c_float, c_float*size[0]*size[1]]
        lib.drandfill(size[0]*size[1], length[0], length[1], ap)
        ap = POINTER(c_float)(ap)
        return object(ap, size, 'float')
    
    def _dzeros(size):
        ap = (c_double*size[0]*size[1])()
        lib.dzeros.argtypes = [c_int, c_int, c_double*size[0]*size[1]]
        lib.dzeros(size[0], size[1], ap)
        ap = POINTER(c_double)(ap)
        return object(ap, size, 'double')
    
    def _szeros(size):
        ap = (c_float*size[0]*size[1])()
        lib.szeros.argtypes = [c_int, c_int, c_float*size[0]*size[1]]
        lib.szeros(size[0], size[1], ap)
        ap = POINTER(c_float)(ap)
        return object(ap, size, 'float')
    
    def _deye(size):
        ap = (c_double*size*size)()
        lib.deye.argtypes = [c_int, c_double*size*size]
        lib.deye(size, ap)
        ap = POINTER(c_double)(ap)
        return object(ap, (size,size), 'double')
    
    def _seye(size):
        ap = (c_float*size*size)()
        lib.seye.argtypes = [c_int, c_float*size*size]
        lib.seye(size, ap)
        ap = POINTER(c_float)(ap)
        return object(ap, (size,size), 'float')
    
    def _drot2(angle):
        trans = (c_double*2*2)()
        lib.drot2.argtypes = [c_double*2*2, c_double]
        lib.drot2(trans, angle)  
        trans = POINTER(c_double)(trans)
        return object(trans, (2, 2), 'double')
    
    def _srot2(angle):
        trans = (c_float*2*2)()
        lib.srot2.argtypes = [c_float*2*2, c_float]
        lib.srot2(trans, angle)  
        trans = POINTER(c_float)(trans)
        return object(trans, (2, 2), 'float')
    
    def _drot3(angle, axis):
        trans = (c_double*3*3)()
        lib.drot3.argtypes = [c_double*3*3, c_double, c_int]
        lib.drot3(trans, angle, axis)
        trans = POINTER(c_double)(trans)
        return object(trans, (3, 3), 'double')
    
    def _srot3(angle, axis):
        trans = (c_float*3*3)()
        lib.srot3.argtypes = [c_float*3*3, c_float, c_int]
        lib.srot3(trans, angle, axis)
        trans = POINTER(c_float)(trans)
        return object(trans, (3, 3), 'float')
        