from NaN.matrix import matrix
from ctypes import *
from NaN.type import ALLType

class matGen:
    def rand(size, length, dtype = 'float'):
        if type(size) != tuple:
            raise TypeError('Invalid data type, size input must be of type tuple')
        if type(length) != tuple:
            raise TypeError('Invalid data type, range input must be of type tuple')
        func = ALLType.MatGenDict['rand'][dtype]
        A = func(size, length)
        return matrix(A, dtype)

    def randn(size, length, dtype = 'float'):
        if type(size) != tuple:
            raise TypeError('Invalid data type, size input must be of type tuple')
        if type(length) != tuple:
            raise TypeError('Invalid data type, range input must be of type tuple')
        func = ALLType.MatGenDict['randn'][dtype]
        A = func(size, length)
        return matrix(A, dtype)

    def zeros(size, dtype = 'float'):
        if type(size) != tuple:
            raise TypeError('Invalid data type, size input must be of type tuple')
        if dtype not in ALLType.TypeDict: 
            raise TypeError('Invalid data type')
        func = ALLType.MatGenDict['zeros'][dtype]
        A = func(size)
        return matrix(A, dtype)

    def eye(size, dtype = 'float'):
        if type(size) != int:
            raise TypeError('Invalid data type, input must be of type int')
        if dtype not in ALLType.TypeDict: 
            raise TypeError('Invalid data type')
        func = ALLType.MatGenDict['eye'][dtype]
        A = func(size)
        return matrix(A, dtype)
    
    def rot2(angle, dtype = 'float'):
        if dtype not in ALLType.TypeDict: 
            raise TypeError('Invalid data type')
        func = ALLType.MatGenDict['rot2'][dtype]
        A = func(angle)
        return matrix(A, dtype)
    
    def rot3(angle, axis, dtype = 'float'):
        if(axis > 2):
            raise TypeError('Invalid rotation axis')    
        if dtype not in ALLType.TypeDict:
            raise TypeError('Invalid data type')
        func = ALLType.MatGenDict['rot3'][dtype]
        A = func(angle, axis)
        return matrix(A, dtype)
    

class ops(matrix):
    def eig(in_matrix: matrix):
        return None

    def transpose(in_matrix: matrix):
        return None

    def det(in_matrix: matrix):
        return None

    def svd(in_matrix: matrix):
        return None
    
    def inv(in_matrix: matrix):
        return None

    def pinv(in_matrix: matrix):
        return None