from setuptools import setup, Extension
import platform
import os

# setup extension

def utils_lib():
    path = os.getcwd() + '/NaN/utils/'
    extra_compile_args = ['-std=c99', '-O3',
                        '-Wall', '-Wextra',
                        '-Wno-unused-parameter', 
                        '-Wno-unused-function', 
                        '-Wno-unused-variable', 
                        '-Wno-unused-but-set-variabl']
    
    module = Extension('data_transfer',
                        sources=[path+'data_transfer.c'],
                        extra_compile_args=extra_compile_args)

    setup(name = 'data_transfer',
        version = '1.0',
        ext_modules=[module],
    )

def matgen_lib():
    path = os.getcwd() + '/NaN/kernels/'
    extra_compile_args = ['-lpthread', '-std=gnu99', '-O2', '-Wall', '-lm']
    
    if platform.system() == 'Darwin':
        extra_compile_args.append('-dynamiclib')
    
    if platform.system() == 'Linux':
        extra_compile_args.append('-fPIC')
        extra_compile_args.append('-shared')
    
    module = Extension('matGen',
                        sources=[path+'mat_gen.c'],
                        extra_compile_args=extra_compile_args)

    setup(name = 'matgen_lib',
        version = '1',
        ext_modules=[module],
    )


def NaN_setup():
    setup(name='NaN',
        version='1.0',
        description='A simple and fast matrix library',
        author='Jiexiang Liu',
        license='MIT',
        install_requires=['pylib-openblas', 'colorama'],
        python_requires='>=3.8',
        extras_require={
            'testing': ['numpy'],
        },)



if __name__ == "__main__":
    utils_lib()