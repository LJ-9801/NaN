from nan.matrix import matrix, object
from ctypes import *
from nan.type import ALLType

class matgen:
    @staticmethod
    def rand(size, length, dtype = 'float'):
        if type(size) != tuple:
            raise TypeError('Invalid data type, size input must be of type tuple')
        if type(length) != tuple:
            raise TypeError('Invalid data type, range input must be of type tuple')
        if length[0] > length[1]:
            raise ValueError('Invalid range input, range must be in ascending order')
        func = ALLType.MatGenDict['rand'][dtype]
        A = func(size, length)
        return matrix(A, dtype)
    
    @staticmethod
    def randn(size, length, dtype = 'float'):
        if type(size) != tuple:
            raise TypeError('Invalid data type, size input must be of type tuple')
        if type(length) != tuple:
            raise TypeError('Invalid data type, range input must be of type tuple')
        func = ALLType.MatGenDict['randn'][dtype]
        A = func(size, length)
        return matrix(A, dtype)

    @staticmethod
    def zeros(size, dtype = 'float'):
        if type(size) != tuple:
            raise TypeError('Invalid data type, size input must be of type tuple')
        if dtype not in ALLType.TypeDict: 
            raise TypeError('Invalid data type')
        func = ALLType.MatGenDict['zeros'][dtype]
        A = func(size)
        return matrix(A, dtype)
    
    @staticmethod
    def eye(size, dtype = 'float'):
        if type(size) != int:
            raise TypeError('Invalid data type, input must be of type int')
        if dtype not in ALLType.TypeDict: 
            raise TypeError('Invalid data type')
        func = ALLType.MatGenDict['eye'][dtype]
        A = func(size)
        return matrix(A, dtype)
    
    @staticmethod
    def rot2(angle, dtype = 'float'):
        if dtype not in ALLType.TypeDict: 
            raise TypeError('Invalid data type')
        func = ALLType.MatGenDict['rot2'][dtype]
        A = func(angle)
        return matrix(A, dtype)
    
    @staticmethod
    def rot3(angle, axis, dtype = 'float'):
        if(axis > 2):
            raise TypeError('Invalid rotation axis')    
        if dtype not in ALLType.TypeDict:
            raise TypeError('Invalid data type')
        func = ALLType.MatGenDict['rot3'][dtype]
        A = func(angle, axis)
        return matrix(A, dtype)
    

class ops(matrix):
    @staticmethod
    def eig(in_matrix: matrix):
        if in_matrix.dtype not in ALLType.TypeDict:
            raise TypeError('Invalid data type')
        if in_matrix.shape[0] != in_matrix.shape[1]:
            raise TypeError('Non-square matrix cannot be eigendecomposed')
        func = ALLType.LapackDict['eig'][in_matrix.dtype]
        wr, wi, ev = func(in_matrix.core.data, in_matrix.shape)
        return (matrix(object(wr, (1,in_matrix.shape[0]), in_matrix.dtype), in_matrix.dtype), 
                matrix(object(wi, (1,in_matrix.shape[0]), in_matrix.dtype), in_matrix.dtype),
                matrix(object(ev, in_matrix.shape, in_matrix.dtype), in_matrix.dtype))
    
    @staticmethod
    def svd(in_matrix: matrix):
        if in_matrix.dtype not in ALLType.TypeDict:
            raise TypeError('Invalid data type')
        func = ALLType.LapackDict['svd'][in_matrix.dtype]
        U,S,V = func(in_matrix.core.data, in_matrix.shape, False)
        return (matrix(object(U, (in_matrix.shape[0], in_matrix.shape[0]), in_matrix.dtype), in_matrix.dtype), 
                matrix(object(S, in_matrix.shape, in_matrix.dtype), in_matrix.dtype), 
                matrix(object(V, (in_matrix.shape[1], in_matrix.shape[1]), in_matrix.dtype), in_matrix.dtype))
    
    @staticmethod
    def lu(in_matrix: matrix):
        if in_matrix.dtype not in ALLType.TypeDict:
            raise TypeError('Invalid data type')
        if in_matrix.shape[0] != in_matrix.shape[1]:
            raise TypeError('Non-square matrix cannot be LU decomposed')
        func = ALLType.LapackDict['lu'][in_matrix.dtype]
        L, U = func(in_matrix.core.data, in_matrix.shape)
        return (matrix(object(L, in_matrix.shape, in_matrix.dtype), in_matrix.dtype),
                matrix(object(U, in_matrix.shape, in_matrix.dtype), in_matrix.dtype))
    
    @staticmethod
    def inv(in_matrix: matrix):
        if in_matrix.dtype not in ALLType.TypeDict:
            raise TypeError('Invalid data type')
        if in_matrix.shape[0] != in_matrix.shape[1]:
            raise TypeError('Non-square matrix cannot be inverted')
        func = ALLType.LapackDict['inv'][in_matrix.dtype]
        A = func(in_matrix.core.data, in_matrix.shape)
        return matrix(object(A, in_matrix.shape, in_matrix.dtype), in_matrix.dtype)
    
    @staticmethod
    def pinv(in_matrix: matrix):
        if in_matrix.dtype not in ALLType.TypeDict:
            raise TypeError('Invalid data type')
        func = ALLType.LapackDict['pinv'][in_matrix.dtype]
        A = func(in_matrix.core.data, in_matrix.shape)
        return matrix(object(A, (in_matrix.shape[1], in_matrix.shape[0]), in_matrix.dtype), in_matrix.dtype)

    def qr(in_matrix: matrix):
        return None    

    def chol(in_matrix: matrix):
        return None

    