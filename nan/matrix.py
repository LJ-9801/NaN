from ctypes import *
from nan.core import object, cArray
from nan.type import ALLType
import array
import mtostr


class utils:
    # use pyobject in c++ to turn pointers to list
    # same with turning list to pointers
    def toPointer(data: list, dtype):
        if isinstance(data[0], list):return ALLType.ArrayDict[dtype]['2d'](data)
        else:return ALLType.ArrayDict[dtype]['1d'](data)

class matrix:
    def __init__(self, data, dtype = 'float'):
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

    def T(self):
        ret = ALLType.MatOpsDict['transpose'][self.dtype](self.data, self.shape)
        return matrix(object(ret, (self.shape[1], self.shape[0]), self.dtype), self.dtype)

    def copy(self):
        ret = ALLType.MemOpsDict['copy'][self.dtype](self.data, self.shape)
        return matrix(object(ret, self.shape, self.dtype), self.dtype)
    
    def __repr__(self) -> str:
        dat = array.array('d', self.core.data[:self.shape[0]*self.shape[1]])
        if self.shape[0] > 8 and self.shape[1] < 8:
            return str(mtostr.largeM(dat, self.shape[0], self.shape[1]))
        elif self.shape[0] < 8 and self.shape[1] > 8:
            return str(mtostr.largeN(dat, self.shape[0], self.shape[1]))
        elif self.shape[0] > 8 and self.shape[1] > 8:
            return str(mtostr.largeMN(dat, self.shape[0], self.shape[1]))
        return str(mtostr.normal(dat, self.shape[0], self.shape[1]))
    
    def __mul__(self, other):
        if ALLType.TypeRank[self.dtype] > ALLType.TypeRank[other.dtype]:
            other.core = cArray._float_to_double(other.core)
            other.dtype = other.core.dtype
        elif ALLType.TypeRank[self.dtype] < ALLType.TypeRank[other.dtype]:
            self.core = cArray._float_to_double(self.core)
            self.dtype = self.core.dtype

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
        if ALLType.TypeRank[self.dtype] > ALLType.TypeRank[other.dtype]:
            other.core = cArray._float_to_double(other.core)
            other.dtype = other.core.dtype
        elif ALLType.TypeRank[self.dtype] < ALLType.TypeRank[other.dtype]:
            self.core = cArray._float_to_double(self.core)
            self.dtype = self.core.dtype

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
        if ALLType.TypeRank[self.dtype] > ALLType.TypeRank[other.dtype]:
            other.core = cArray._float_to_double(other.core)
            other.dtype = other.core.dtype
        elif ALLType.TypeRank[self.dtype] < ALLType.TypeRank[other.dtype]:
            self.core = cArray._float_to_double(self.core)
            self.dtype = self.core.dtype

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
    
    def __getitem__(self, index):
        if isinstance(index, tuple) and isinstance(index[0], int) and isinstance(index[1], int):
            if index[0] >= self.shape[0] or index[1] >= self.shape[1]:
                raise IndexError('Index out of range')
            ret = (ALLType.TypeDict[self.dtype]*1)(self.core.data[index[1] + index[0]*self.shape[1]])
            return matrix(object(ret, (1,1), self.dtype), self.dtype)
        elif isinstance(index, tuple) and isinstance(index[0], int) and isinstance(index[1], slice):
            if index[0] >= self.shape[0] or index[1].stop > self.shape[1] or index[1].start - index[1].stop > self.shape[1]:
                raise IndexError('Index out of range')
            ret = (ALLType.TypeDict[self.dtype]*(index[1].stop - index[1].start))()
            ret[:] = self.core.data[index[0]*self.shape[1] + index[1].start:index[0]*self.shape[1] + index[1].stop]
            return matrix(object(ret, (1,index[1].stop - index[1].start), self.dtype), self.dtype)
        elif isinstance(index, tuple) and isinstance(index[0], slice) and isinstance(index[1], int):
            if index[0].stop > self.shape[0] or index[1] >= self.shape[1] or index[0].start - index[0].stop > self.shape[0]:
                raise IndexError('Index out of range')
            ret = (ALLType.TypeDict[self.dtype]*(index[0].stop - index[0].start))()
            for i in range(index[0].start, index[0].stop):ret[i] = self.core.data[index[1] + i*self.shape[1]]
            return matrix(object(ret, (index[0].stop - index[0].start, 1), self.dtype), self.dtype)
        elif isinstance(index, tuple) and isinstance(index[0], slice) and isinstance(index[1], slice):
            if index[0].stop > self.shape[0] or index[1].stop > self.shape[1] or index[0].start - index[0].stop > self.shape[0] or index[1].start - index[1].stop > self.shape[1]:
                raise IndexError('Index out of range')
            ret = (ALLType.TypeDict[self.dtype]*((index[0].stop - index[0].start)*(index[1].stop - index[1].start)))()
            for i in range(index[0].start, index[0].stop):
                ret[(i - index[0].start)*(index[1].stop - index[1].start):(i - index[0].start)*(index[1].stop - index[1].start) + (index[1].stop - index[1].start)] = self.core.data[i*self.shape[1]:i*self.shape[1] + index[1].stop - index[1].start]
            ret = ALLType.MemOpsDict['copy'][self.dtype](ret, (index[0].stop - index[0].start, index[1].stop - index[1].start))
            return matrix(object(ret, (index[0].stop - index[0].start, index[1].stop - index[1].start), self.dtype), self.dtype)
                
            