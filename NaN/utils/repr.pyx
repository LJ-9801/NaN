cimport cython
from libcpp.string cimport string

def tostr(input, int m, int n):
    cdef string matrix = "["
    cdef int i
    cdef int j
    cdef string row
    cdef int index
    for i in range(m):
        j = 0
        if i == 0:
            row = "["
        else:
            row = " ["

        for j in range(n):
            index = i*n + j
            val = f"{input[index]:.4f}"
            row = row + bytes(val, 'utf-8')
            if j < n-1:
                row = row + bytes(", ", 'utf-8')
        if i < m-1:
            row = row + bytes("]", 'utf-8') + bytes("\n", 'utf-8')
        else:
            row = row + bytes("]", 'utf-8')
        matrix = matrix + row

    matrix = matrix + bytes("]", 'utf-8')
    return matrix


