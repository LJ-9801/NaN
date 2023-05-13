from libc.math cimport sin, cos
from libc.stdlib cimport malloc, rand, RAND_MAX, free
from libc.time cimport time
from libc.stdio cimport printf
from ctypes import *


cdef extern from "<random>" namespace "std":
    cdef cppclass mt19937:
        mt19937()
        mt19937(unsigned int seed)
    
    cdef cppclass uniform_real_distribution[T]:
        uniform_real_distribution()
        uniform_real_distribution(T a, T b)
        T operator()(mt19937 gen)

    cdef cppclass uniform_int_distribution[T]:
        uniform_int_distribution()
        uniform_int_distribution(T a, T b)
        T operator()(mt19937 gen)
    
    cdef cppclass normal_distribution[T]:
        normal_distribution()
        normal_distribution(T mean, T stddev)
        T operator()(mt19937 gen)
        

def duniform(int m, int n, double a, double b):
    cdef mt19937 gen = mt19937(int(time(NULL)))
    cdef uniform_real_distribution[double] distribution = uniform_real_distribution[double](a, b)

    buff = (c_double*(m*n))()
    cdef int i
    for i in range(m * n):
        buff[i] = distribution(gen)
    return buff


def suniform(int m, int n, float a, float b):
    cdef mt19937 gen = mt19937(int(time(NULL)))
    cdef uniform_real_distribution[float] distribution = uniform_real_distribution[float](a, b)

    buff = (c_float*(m*n))()
    cdef int i
    for i in range(m * n):
        buff[i] = distribution(gen)
    return buff


def drandn(int m, int n, double mean, double dev):
    cdef mt19937 gen = mt19937(int(time(NULL)))
    cdef normal_distribution[double] distribution = normal_distribution[double](mean, dev)

    buff = (c_double*(m*n))()
    cdef int i
    for i in range(m * n):
        buff[i] = distribution(gen)
    return buff


def srandn(int m, int n, float mean, float dev):
    cdef mt19937 gen = mt19937(int(time(NULL)))
    cdef normal_distribution[float] distribution = normal_distribution[float](mean, dev)

    buff = (c_float*(m*n))()
    cdef int i
    for i in range(m * n):
        buff[i] = distribution(gen)
    return buff

def dzeros(int m, int n):
    return(c_double*(m*n))()


def szeros(int m, int n):
    return (c_float*(m*n))()
    

def deye(int size):
    buff = (c_double*(size*size))()
    cdef int i
    cdef double one = 1.0
    for i in range(size*size):
        if i % (size + 1) == 0:
            buff[i] = one
    return buff

def seye(int size):
    buff = (c_float*(size*size))()
    cdef int i
    cdef float one = 1.0
    for i in range(size*size):
        if i % (size + 1) == 0:
            buff[i] = one
    return buff

def drot2(double angle):
    buff = (c_double*4)()
    cdef double c, s
    c = cos(angle)
    s = sin(angle)
    buff[0] = c
    buff[1] = -s
    buff[2] = s
    buff[3] = c
    return buff

def srot2(float angle):
    buff = (c_float*4)()
    cdef float c, s
    c = cos(angle)
    s = sin(angle)
    buff[0] = c
    buff[1] = -s
    buff[2] = s
    buff[3] = c
    return buff

def drot3(double angle, int axis):
    buff = (c_double*9)()
    cdef double c, s
    c = cos(angle)
    s = sin(angle)
    if axis == 0:
        buff[0] = 1.0
        buff[1] = 0.0
        buff[2] = 0.0
        buff[3] = 0.0
        buff[4] = c
        buff[5] = -s
        buff[6] = 0.0
        buff[7] = s
        buff[8] = c
    elif axis == 1:
        buff[0] = c
        buff[1] = 0.0
        buff[2] = s
        buff[3] = 0.0
        buff[4] = 1.0
        buff[5] = 0.0
        buff[6] = -s
        buff[7] = 0.0
        buff[8] = c
    elif axis == 2:
        buff[0] = c
        buff[1] = -s
        buff[2] = 0.0
        buff[3] = s
        buff[4] = c
        buff[5] = 0.0
        buff[6] = 0.0
        buff[7] = 0.0
        buff[8] = 1.0
    return buff

def srot3(float angle, int axis):
    buff = (c_float*9)()
    cdef float c, s
    c = cos(angle)
    s = sin(angle)
    if axis == 0:
        buff[0] = 1.0
        buff[1] = 0.0
        buff[2] = 0.0
        buff[3] = 0.0
        buff[4] = c
        buff[5] = -s
        buff[6] = 0.0
        buff[7] = s
        buff[8] = c
    elif axis == 1:
        buff[0] = c
        buff[1] = 0.0
        buff[2] = s
        buff[3] = 0.0
        buff[4] = 1.0
        buff[5] = 0.0
        buff[6] = -s
        buff[7] = 0.0
        buff[8] = c
    elif axis == 2:
        buff[0] = c
        buff[1] = -s
        buff[2] = 0.0
        buff[3] = s
        buff[4] = c
        buff[5] = 0.0
        buff[6] = 0.0
        buff[7] = 0.0
        buff[8] = 1.0
    return buff


    
