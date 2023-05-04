import ctypes, ctypes.util
import subprocess as sp

if ctypes.util.find_library('openblas') == None:
    print("BLAS library not found, installing...")
    sp.run(['conda', 'install', '-c', 'conda-forge', 'openblas'])
    print("BLAS library installed")
else:
    print('CBLAS found')

print("Setting up libraries...")
if sp.run(["find", "kernals/build"], stdout=sp.PIPE).stdout.decode('utf-8') == '':
    sp.run(['make', '-C', 'kernals'])
sp.run(['cd', 'NaN/utils', '&&', 'pip install .'])
sp.run(['cd ..'])
sp.run(['cd ..'])

print('NaN is set up, runnning tests...')
#sp.run(['python', 'test.py'])
