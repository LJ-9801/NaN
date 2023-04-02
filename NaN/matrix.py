from NaN.mkl import CBLAS
from ctypes import *
from ctypes.util import find_library
import data_transfer
from NaN.core import object


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

    
    def __mul__(self, other):
        out_dim = (self.shape[0], other.shape[1])
        if(type(other) != type(self)):
            raise TypeError('Invalid data type, input must be of type matrix')
        
        if(self.shape[1] != other.shape[0]):
            raise ValueError('Matrix dimensions are not compatible')
        
        # we need to support dynamic typing
        # this is only temperary
        if self.dtype != other.dtype:
            raise TypeError('Matrix data types are not compatible')
        # no need to convert to pointers, all calculation 
        # is done using pointers under the hood
        A = self.core.data
        B = other.core.data
        if self.dtype == 'double':
            C = CBLAS._dgemm(A,B,self.shape,other.shape)
        elif self.dtype == 'float': # float does not work
            C = CBLAS._sgemm(A,B,self.shape,other.shape)
        C = object(C, out_dim, self.dtype)
        self.C = matrix(C, self.dtype)
        return self.C
    
    def __str__(self):
        #this will realize the matrix from the pointers
        return str(utils.toList(self.core.data, self.shape))
    
    def __getItem__(self, index):
        if self.shape[1] == 1:
            return self.core.data[index]
        else:
            return self.core.data[index[0]*self.shape[1] + index[1]]