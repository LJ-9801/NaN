from NaN.matrix import matrix
from ctypes import *
from NaN.core import MATGEN


class matGen:
    def randn(size, length, dtype):
        if type(size) != tuple:
            raise TypeError('Invalid data type, size input must be of type tuple')
        if type(length) != tuple:
            raise TypeError('Invalid data type, range input must be of type tuple')
        
        if dtype == 'double':
            A = MATGEN._drandn(size, length)
        elif dtype == 'float':
            A = MATGEN._srandn(size, length)
        return matrix(A, dtype)

    def zeros(size, dtype):
        if type(size) != tuple:
            raise TypeError('Invalid data type, size input must be of type tuple')
        if dtype == 'double':
            ret = MATGEN._dzeros(size)
        elif dtype == 'float':
            ret = MATGEN._szeros(size)
        return matrix(ret, dtype)

    def eye(size, dtype):
        if type(size) != int:
            raise TypeError('Invalid data type, input must be of type int')
        if dtype == 'double':
            ret = MATGEN._deye(size)
        elif dtype == 'float':
            ret = MATGEN._seye(size)
        return matrix(ret, dtype)
    
    def rot2(angle, dtype = 'float'):
        if dtype == 'double':
            ret = MATGEN._drot2(angle)
        elif dtype == 'float':
            ret = MATGEN._srot2(angle)
        return  matrix(ret, dtype)
    
    def rot3(angle, axis, dtype = 'float'):
        if(axis > 2):
            raise TypeError('Invalid rotation axis')    
        if dtype == 'double':
            ret = MATGEN._drot3(angle, axis)
        elif dtype == 'float':
            ret = MATGEN._srot3(angle, axis)
        return matrix(ret, dtype)
    

class ops:
    def eig(in_matrix):
        return None

    def transpose(in_matrix):
        return None

    def det(in_matrix):
        return None

    def svd(in_matrix):
        return None
    
    def inv(in_matrix):
        return None

    def pinv(in_matrix):
        return None