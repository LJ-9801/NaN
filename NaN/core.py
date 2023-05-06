from ctypes import *
import ctypes.util
import os

curr_dir = os.getcwd()
path = os.path.join(curr_dir, 'NaN/src/build/mat_gen.dylib')
lib = cdll.LoadLibrary(path)


class object:
    def __init__(self, data, shape, dtype):
        self.dtype = dtype
        self.shape = shape
        self.data = data

class cArray:
    def _to_2dlist(inpointer, shape: tuple):
        outlist = []
        for i in range(shape[0]):
            outlist.append(inpointer[i*shape[1]:(i+1)*shape[1]])
        return outlist
    
    def _to_1dlist(inpointer, shape: tuple):
        outlist = []
        for i in range(shape[0]):
            outlist.append(inpointer[i])
        return outlist

    def to_double_1dpointers(inlist):
        mem = (c_double*len(inlist))()
        mem[:] = inlist[:]
        return POINTER(c_double)(mem)

    def to_double_2dpointers(inlist):
        mem = (c_double*len(inlist[0])*len(inlist))()
        for i in range(len(inlist)):
            for j in range(len(inlist[0])):
                mem[i][j] = inlist[i][j]
        return POINTER(c_double)(mem)

    def to_float_1dpointers(inlist):
        mem = (c_float*len(inlist))()
        mem[:] = inlist[:]
        return POINTER(c_float)(mem)

    def to_float_2dpointers(inlist):
        mem = (c_float*len(inlist[0])*len(inlist))()
        for i in range(len(inlist)):
            for j in range(len(inlist[0])):
                mem[i][j] = inlist[i][j]
        return POINTER(c_float)(mem)

class MATGEN:
    def __init__(self) -> None:
        pass
    
    def _drandn(size, length):
        ap = (c_double*size[0]*size[1])()
        lib.drandfill.argtypes = [c_int, c_double, c_double, c_double*size[0]*size[1]]
        lib.drandfill(size[0]*size[1], length[0], length[1], ap)
        ap = POINTER(c_double)(ap)
        return object(ap, size, 'double')

    def _srandn(size, length):
        ap = (c_float*size[0]*size[1])()
        lib.srandfill.argtypes = [c_int, c_float, c_float, c_float*size[0]*size[1]]
        lib.srandfill(size[0]*size[1], length[0], length[1], ap)
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
        