from setuptools import setup, Extension

extra_compile_args = ['-std=c99', '-O3', '-fopenmp',
                      '-lm', '-Wall', '-Wextra',
                      '-Wno-unused-parameter', 
                      '-Wno-unused-function', 
                      '-Wno-unused-variable', 
                      '-Wno-unused-but-set-variabl']

setup(name = 'utils_lib',
      version = '1',
      ext_modules=[Extension('data_transfer', ['data_transfer.c'], 
                             extra_compile_args=extra_compile_args)],
)