from ctypes import *
from nan.core import MATGEN, cArray
from nan.mkl import CBLAS, MemOps, LAPACK


class ALLType:
        TypeDict = {'double': c_double, 
            'float': c_float, 
            'int': c_int, 
            'long': c_long, 
            'short': c_short, 
            'char': c_char, 
            'bool': c_bool}

        MatGenDict = {'randn': {'double': MATGEN._drandn, 'float': MATGEN._srandn},
            'rand': {'double': MATGEN._drand, 'float': MATGEN._srand},
            'zeros': {'double': MATGEN._dzeros, 'float': MATGEN._szeros},
            'eye': {'double': MATGEN._deye, 'float': MATGEN._seye},
            'rot2': {'double': MATGEN._drot2, 'float': MATGEN._srot2},
            'rot3': {'double': MATGEN._drot3, 'float': MATGEN._srot3}
        }

        MatOpsDict = {'matmul': {'double': CBLAS._dgemm, 'float': CBLAS._sgemm},
                      'matadd': {'double': CBLAS._dadd, 'float': CBLAS._sadd},
                      'matsub': {'double': CBLAS._dsub, 'float': CBLAS._ssub},
                      'transpose': {'double': CBLAS._dtranspose, 'float': CBLAS._stranspose},}
        
        MemOpsDict = {'copy': {'double': MemOps._dcopy, 'float': MemOps._scopy},}

        ArrayDict = {'double': {'1d': cArray.to_double_1dpointers, '2d': cArray.to_double_2dpointers},
                     'float':  {'1d': cArray.to_float_1dpointers, '2d': cArray.to_float_2dpointers}}
        
        LapackDict = {'eig': {'double': LAPACK._deig, 'float': LAPACK._seig},
                      'svd': {'double': LAPACK._dsvd, 'float': LAPACK._ssvd},
                      'lu': {'double': LAPACK._dlu, 'float': LAPACK._slu},
                      'inv': {'double': LAPACK._dinv, 'float': LAPACK._sinv},
                      'pinv': {'double': LAPACK._dpinv, 'float': LAPACK._spinv},}

        TypeRank = {'bool': 0, 'char': 1, 'short': 2, 'int': 3, 'long': 4, 'float': 5, 'double': 6}
        
        
    
    
