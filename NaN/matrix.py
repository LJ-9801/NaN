from ctypes import *
import data_transfer
from NaN.core import object
from NaN.type import ALLType
from NaN.mkl import MemOps


class utils:
    # use pyobject in c++ to turn pointers to list
    def toList(data, shape):
        result = data[:shape[0]*shape[1]]
        result = data_transfer.tolist(shape[0], shape[1] ,result)
        return result
    # same with turning list to pointers
    def toPointer(data, dtype):
        if dtype == 'double':
            if type(data[0]) == list:
                mem = (c_double*len(data[0])*len(data))()
                for i in range(len(data)):
                    for j in range(len(data[0])):
                        mem[i][j] = data[i][j]
                pointers = POINTER(c_double)(mem)
            else:
                mem = (c_double*len(data))()
                for i in range(len(data)):
                    mem[i] = data[i]
                pointers = POINTER(c_double)(mem)
        elif dtype == 'float':
            if type(data[0]) == list:
                mem = (c_float*len(data[0])*len(data))()
                for i in range(len(data)):
                    for j in range(len(data[0])):
                        mem[i][j] = data[i][j]
                pointers = POINTER(c_float)(mem)
            else:
                mem = (c_float*len(data))()
                for i in range(len(data)):
                    mem[i] = data[i]
                pointers = POINTER(c_float)(mem)
        return pointers

class matrix:
    def __init__(self, data, dtype):
        # this will hold pointers to the data
        if type(data) == list:
            self.dtype = dtype
            self.shape = (len(data), len(data[0])) if type(data[0]) == list else (len(data), 1)
            self.data = utils.toPointer(data, dtype)
            self.core = object(self.data, self.shape, dtype)
        elif type(data) == object:
            self.core = data
            self.dtype = data.dtype
            self.shape = data.shape
            self.data = data.data

    def copy(self):
        ret = ALLType.MemOpsDict['copy'][self.dtype](self.data, self.shape)
        return matrix(object(ret, self.shape, self.dtype), self.dtype)

    
    def __mul__(self, other):
        out_dim = (self.shape[0], other.shape[1])
        if(type(other) != type(self)):
            raise TypeError('Invalid data type, input must be of type matrix')
        if(self.shape[1] != other.shape[0]):
            raise ValueError('Matrix dimensions are not compatible')
        if self.dtype != other.dtype:
            raise TypeError('Matrix data types are not compatible')
        A = self.core.data
        B = other.core.data
        func = ALLType.MatOpsDict['matmul'][self.dtype]
        C = func(A,B,self.shape,other.shape)
        return matrix(object(C, out_dim, self.dtype), self.dtype)
    
    def __add__(self, other):
        if(type(other) != type(self)):
            raise TypeError('Invalid data type, input must be of type matrix')
        if(self.shape != other.shape):
            raise ValueError('Matrix dimensions are not compatible')
        if self.dtype != other.dtype:
            raise TypeError('Matrix data types are not compatible')
        A = self.core.data
        B = other.core.data
        func = ALLType.MatOpsDict['matadd'][self.dtype]
        C = func(A,B,self.shape)
        return matrix(object(C, self.shape, self.dtype), self.dtype)
    
    def __sub__(self, other):
        if(type(other) != type(self)):
            raise TypeError('Invalid data type, input must be of type matrix')
        if(self.shape != other.shape):
            raise ValueError('Matrix dimensions are not compatible')
        if self.dtype != other.dtype:
            raise TypeError('Matrix data types are not compatible')
        A = self.core.data
        B = other.core.data
        func = ALLType.MatOpsDict['matsub'][self.dtype]
        C = func(A,B,self.shape)
        return matrix(object(C, self.shape, self.dtype), self.dtype)
    
    def __str__(self):
        #this will realize the matrix from the pointers
        return str(utils.toList(self.core.data, self.shape))
    
    def __getitem__(self, index):
        if isinstance(index, tuple) and isinstance(index[0], int) and isinstance(index[1], int):
            ret = ALLType.MemOpsDict['copy'][self.dtype](self.core.data[index[0] + index[1]*self.shape[0]], (1,1))
            return matrix(object(ret, (1,1), self.dtype), self.dtype)
        elif isinstance(index, tuple) and isinstance(index[0], int) and isinstance(index[1], slice):
            ret = ALLType.MemOpsDict['copy'][self.dtype](self.core.data[index[0] + index[1].start*self.shape[0]:index[0] + index[1].stop*self.shape[0]], (index[1].stop - index[1].start, 1))
            return matrix(object(ret, (index[1].stop - index[1].start, 1), self.dtype), self.dtype)
        elif isinstance(index, tuple) and isinstance(index[0], slice) and isinstance(index[1], int):
            ret = ALLType.MemOpsDict['copy'][self.dtype](self.core.data[index[0].start + index[1]*self.shape[0]:index[0].stop + index[1]*self.shape[0]], (index[0].stop - index[0].start, 1))
            return matrix(object(ret, (index[0].stop - index[0].start, 1), self.dtype), self.dtype)
        elif isinstance(index, tuple) and isinstance(index[0], slice) and isinstance(index[1], slice):
            ret = (ALLType.TypeDict[self.dtype]*((index[0].stop - index[0].start)*(index[1].stop - index[1].start)))()
            for i in range(index[1].start, index[1].stop):
                ret[(i - index[1].start)*(index[0].stop - index[0].start):(i - index[1].start)*(index[0].stop - index[0].start) + (index[0].stop - index[0].start)] = self.core.data[index[0].start + i*self.shape[0]:index[0].stop + i*self.shape[0]]
            #ret = ALLType.MemOpsDict['copy'][self.dtype](ret, (index[0].stop - index[0].start, index[1].stop - index[1].start))
            return matrix(object(ret, (index[0].stop - index[0].start, index[1].stop - index[1].start), self.dtype), self.dtype)
                
            