from setuptools import setup, Extension
import setuptools
import subprocess
import os

# setup extension


def matgen_lib():
    path = os.getcwd() + '/NaN/NaN/src/'
    subprocess.run(['make', '-C', path])



def NaN_setup():
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

    setup(name='NaN',
        version='0.0.1',
        description='A simple and fast matrix library',
        author='Jiexiang Liu',
        license='MIT',
        packages=setuptools.find_packages(),
        install_requires=['pylib-openblas', 'colorama', 'numpy'],
        python_requires='>=3.8',
        extras_require={
            'testing': ['numpy'],
        },
        ext_modules=[module],)



if __name__ == "__main__":
    matgen_lib()
    NaN_setup()