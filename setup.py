from setuptools import setup, Extension
import os
# setup extension
def NaN_setup():
    utils_path = os.getcwd() + '/NaN/utils/'
    src_path = os.getcwd() + '/NaN/src/'

    compile_arg1 = ['-std=c99', '-O3',
                        '-Wall', '-Wextra',
                        '-Wno-unused-parameter', 
                        '-Wno-unused-function', 
                        '-Wno-unused-variable', 
                        '-Wno-unused-but-set-variabl']
    
    #compile_arg2 = ['-lpthread', '-std=gnu99', '-O2', '-Wall', '-lm'
    #                ,'-dynamiclib']
    
    module1 = Extension('data_transfer',
                        sources=[utils_path+'data_transfer.c'],
                        extra_compile_args=compile_arg1)
    
    #module2 = Extension('mat_gen',
    #                    sources=[src_path+'mat_gen.c'],
    #                    include_dirs=[src_path],
    #                    extra_compile_args=compile_arg2)

    setup(name='NaN',
        version='1.0',
        description='A simple and fast matrix library',
        author='Jiexiang Liu',
        license='MIT',
        install_requires=['pylib-openblas', 'colorama'],
        python_requires='>=3.8',
        ext_modules=[module1],
        extras_require={
            'testing': ['numpy'],
        },)



if __name__ == "__main__":
    NaN_setup()