from cython.parallel import prange
from libc.math cimport sin, cos
from libc.stdlib cimport malloc, rand, RAND_MAX, free
from libc.time cimport time
from libc.stdio cimport printf
from ctypes import *


def drandn(int m, int n, double r1, double r2):
    buff = (c_double*(m*n))()
    cdef int i
    for i in range(m * n):
        buff[i] = r1 + r2 * (2.0 * rand() / RAND_MAX - 1.0)
    return buff

'''
def drandn(int m, int n, double r1, double r2):
    out = (c_double*(m*n))()
    out = POINTER(c_double)(out)
    cdrandn(m,n,r1,r2,out)
    return out
'''

def srandn(int m, int n, float r1, float r2):
    buff = (c_float*(m*n))()
    cdef int i
    for i in range(m * n):
        buff[i] = r1 + r2 * (2.0 * rand() / RAND_MAX - 1.0)
    return buff

def dzeros(int m, int n):
    return(c_double*(m*n))()


def szeros(int m, int n):
    return (c_float*(m*n))()
    

def deye(int size):
    buff = (c_double*(size*size))()
    cdef int i
    for i in range(size*size):
        if i % (size + 1) == 0:
            buff[i] = 1.0
        else:
            buff[i] = 0.0
    return buff

def seye(int size):
    buff = (c_float*(size*size))()
    cdef int i
    for i in range(size*size):
        if i % (size + 1) == 0:
            buff[i] = 1.0
        else:
            buff[i] = 0.0
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


    
