from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import os
# setup extension
def NaN_setup():
    utils_path = os.getcwd() + '/NaN/utils/'
    src_path = os.getcwd() + '/NaN/src/'

    module1 = Extension('mtostr',
                        language='c++',
                        sources=[utils_path+'repr.cpp'],
                        extra_compile_args=['-O3'])
    
    cmodule = Extension('generator',
                        language='c++',
                        sources=[src_path+'mat_gen.cpp'],
                        include_dirs=[src_path],
                        extra_compile_args=['-O3', '-pthread'],
                        extra_link_args=['-std=c++11'])
    
    dymtype = Extension('dymtype',
                        language='c++',
                        sources=[utils_path+'dymtype.cpp'],
                        extra_compile_args=['-O3'],
                        extra_link_args=['-std=c++11'])
    

    setup(name='NaN',
        version='1.0',
        description='A lightweight and fast matrix library',
        author='Jiexiang Liu',
        license='MIT',
        packages=find_packages(),
        install_requires=['pylib-openblas', 'colorama', 'cython'],
        python_requires='>=3.8',
        ext_modules=cythonize([module1]) + [cmodule, dymtype],
        zip_safe=False,
        extras_require={
            'testing': ['numpy'],
        },)



if __name__ == "__main__":
    NaN_setup()