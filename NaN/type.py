from ctypes import *
from NaN.core import MATGEN
from NaN.mkl import CBLAS, MemOps

class ALLType:
        TypeDict = {'double': c_double, 
            'float': c_float, 
            'int': c_int, 
            'long': c_long, 
            'short': c_short, 
            'char': c_char, 
            'bool': c_bool}

        MatGenDict = {'randn': {'double': MATGEN._drandn, 'float': MATGEN._srandn},
            'zeros': {'double': MATGEN._dzeros, 'float': MATGEN._szeros},
            'eye': {'double': MATGEN._deye, 'float': MATGEN._seye},
            'rot2': {'double': MATGEN._drot2, 'float': MATGEN._srot2},
            'rot3': {'double': MATGEN._drot3, 'float': MATGEN._srot3}
        }

        MatOpsDict = {'matmul': {'double': CBLAS._dgemm, 'float': CBLAS._sgemm},
                      'matadd': {'double': CBLAS._dadd, 'float': CBLAS._sadd},
                      'matsub': {'double': CBLAS._dsub, 'float': CBLAS._ssub},}
        
        MemOpsDict = {'copy': {'double': MemOps._dcopy, 'float': MemOps._scopy},}
        
    
    
