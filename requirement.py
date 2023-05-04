import ctypes, ctypes.util
import subprocess as sp

print("Installing Dependencies...")
if ctypes.util.find_library('openblas') == None:
    print("BLAS library not found, installing...")
    sp.run(['conda', 'install', '-c', 'conda-forge', 'openblas'])
    if ctypes.util.find_library('openblas') == None:
        print("BLAS installed failed, please install manually")
        exit()
    else:
        print("BLAS library installed")
else:
    print('CBLAS found')

print("Installing Numpy for testing...")
sp.run(['conda', 'install', 'numpy'])
print("Installing Colorama...")
sp.run(['conda', 'install -c conda-forge ', 'colorama'])

print("Setting up libraries...")
if sp.run(["find", "kernals/build"], stdout=sp.PIPE).stdout.decode('utf-8') == '':
    sp.run(['make', '-C', 'kernals'])
sp.run(['cd', 'NaN/utils', '&&', 'pip install .'])
sp.run(['cd ..'])

input("NaN installed, do you want to run the test? (y/n)")
while input() != 'y' or input() != 'n':
    input("Invalid input, please enter again (y/n): ")
if input() == 'y':
    sp.run(['python test.py'])
else:
    print("Test skipped")
