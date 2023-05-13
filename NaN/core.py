from ctypes import *
import matgen


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

    def _drand(size, length):
        out = matgen.duniform(int(size[0]), int(size[1]), length[0], length[1])
        ap = POINTER(c_double)(out)
        return object(ap, size, 'double')
    
    def _srand(size, length):
        out = matgen.suniform(int(size[0]), int(size[1]), length[0], length[1])
        ap = POINTER(c_float)(out)
        return object(ap, size, 'float')
    
    def _drandn(size, length):
        out = matgen.drandn(int(size[0]), int(size[1]), length[0], length[1])
        ap = POINTER(c_double)(out)
        return object(ap, size, 'double')

    def _srandn(size, length):
        out = matgen.srandn(int(size[0]), int(size[1]), length[0], length[1])
        ap = POINTER(c_float)(out)
        return object(ap, size, 'float')
    
    def _dzeros(size):
        out = matgen.dzeros(int(size[0]), int(size[1]))
        ap = POINTER(c_double)(out)
        return object(ap, size, 'double')
    
    def _szeros(size):
        out = matgen.szeros(int(size), int(size[1]))
        ap = POINTER(c_float)(out)
        return object(ap, size, 'float')
    
    def _deye(size):
        out = matgen.deye(int(size))
        ap = POINTER(c_double)(out)
        return object(ap, (size,size), 'double')
    
    def _seye(size):
        out = matgen.seye(int(size))
        ap = POINTER(c_float)(out)
        return object(ap, (size,size), 'float')
    
    def _drot2(angle):
        out = matgen.drot2(angle)
        trans = POINTER(c_double)(out)
        return object(trans, (2, 2), 'double')
    
    def _srot2(angle):
        out = matgen.srot2(angle)
        trans = POINTER(c_float)(out)
        return object(trans, (2, 2), 'float')
    
    def _drot3(angle, axis):
        out = matgen.drot3(angle, int(axis))
        trans = POINTER(c_double)(out)
        return object(trans, (3, 3), 'double')
    
    def _srot3(angle, axis):
        out = matgen.srot3(angle, int(axis))
        trans = POINTER(c_float)(out)
        return object(trans, (3, 3), 'float')
        