from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import os
# setup extension
def NaN_setup():
    utils_path = os.getcwd() + '/NaN/utils/'

    compile_arg1 = ['-O3']

    module1 = Extension('repr',
                        language='c++',
                        sources=[utils_path+'repr.pyx'],
                        extra_compile_args=compile_arg1)
    
    module2 = Extension('matgen',
                        sources=[utils_path+'matgen.pyx'],
                        extra_compile_args=['-fopenmp', '-O3'],
                        extra_link_args=['-fopenmp'])
    

    setup(name='NaN',
        version='1.0',
        description='A lightweight and fast matrix library',
        author='Jiexiang Liu',
        license='MIT',
        packages=find_packages(),
        install_requires=['pylib-openblas', 'colorama', 'cython'],
        python_requires='>=3.8',
        ext_modules=cythonize([module1,module2]),
        zip_safe=False,
        extras_require={
            'testing': ['numpy'],
        },)



if __name__ == "__main__":
    NaN_setup()