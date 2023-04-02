import ctypes, ctypes.util

if ctypes.util.find_library('cblas') == None:
    raise ImportError('Error, CBLAS not found')
else:
    print('CBLAS found')
if ctypes.util.find_library('lapack') == None:
    raise ImportError('Error, LAPACK not found')
else:
    print('LAPACK found')

print('All libraries found')
