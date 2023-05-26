from ctypes import *
import generator
import array
import dymtype

class object:
    def __init__(self, data, shape, dtype):
        self.dtype = dtype
        self.shape = shape
        self.data = data

class cArray:
    def _float_to_double(inobj: object):
        arr = array.array('d', inobj.data[:inobj.shape[0]*inobj.shape[1]])
        out = dymtype.toctypes(arr)
        return object(out, inobj.shape, 'double')

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
        out = generator.drand(int(size[0])*int(size[1]), length[0], length[1])
        return object(out, size, 'double')
    
    def _srand(size, length):
        out = generator.srand(int(size[0])*int(size[1]), length[0], length[1])
        return object(out, size, 'float')
    
    def _drandn(size, length):
        out = generator.drandn(int(size[0])*int(size[1]), length[0], length[1])
        return object(out, size, 'double')

    def _srandn(size, length):
        out = generator.srandn(int(size[0])*int(size[1]), length[0], length[1])
        return object(out, size, 'float')
    
    def _dzeros(size):
        out = generator.dzeros(int(size[0]), int(size[1]))
        return object(out, size, 'double')
    
    def _szeros(size):
        out = generator.szeros(int(size[0]), int(size[1]))
        return object(out, size, 'float')
    
    def _deye(size):
        out = generator.deye(int(size))
        return object(out, (size,size), 'double')
    
    def _seye(size):
        out = generator.seye(int(size))
        return object(out, (size,size), 'float')
    
    def _drot2(angle):
        out = generator.drot2(angle)
        return object(out, (2, 2), 'double')
    
    def _srot2(angle):
        out = generator.srot2(angle)
        return object(out, (2, 2), 'float')
    
    def _drot3(angle, axis):
        out = generator.drot3(angle, int(axis))
        return object(out, (3, 3), 'double')
    
    def _srot3(angle, axis):
        out = generator.srot3(angle, int(axis))
        return object(out, (3, 3), 'float')
        