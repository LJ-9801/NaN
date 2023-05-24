cimport cython
from libcpp.string cimport string

def upper(input, int m, int n):
    cdef string matrix = "["
    cdef int i
    cdef int j
    cdef string row
    cdef int index
    for i in range(4):
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

    return matrix

def lower(input, int m, int n):
    cdef string matrix = ""
    cdef int i
    cdef int j
    cdef string row
    cdef int index
    for i in range(4):
        j = 0
        row = " ["

        for j in range(n):
            index = (m-4+i)*n + j
            val = f"{input[index]:.4f}"
            row = row + bytes(val, 'utf-8')
            if j < n-1:
                row = row + bytes(", ", 'utf-8')
        if i < 4-1:
            row = row + bytes("]", 'utf-8') + bytes("\n", 'utf-8')
        else:
            row = row + bytes("]", 'utf-8')
        matrix = matrix + row
    
    matrix = matrix + bytes("]", 'utf-8')
    return matrix


def largeN_upper(input, int m, int n):
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

        for j in range(4):
            index = i*n + j
            val = f"{input[index]:.4f}"
            row = row + bytes(val, 'utf-8')
            if j < n-1:
                row = row + bytes(", ", 'utf-8')
        row = row + bytes("... ", 'utf-8')
        for j in range(4):
            index = i*n + (n-4+j)
            val = f"{input[index]:.4f}"
            row = row + bytes(val, 'utf-8')
            if j < 4-1:
                row = row + bytes(", ", 'utf-8')
        if i < m-1:
            row = row + bytes("]", 'utf-8') + bytes("\n", 'utf-8')
        else:
            row = row + bytes("]", 'utf-8')
        matrix = matrix + row

    return matrix

def largeN_lower(input, int m, int n):
    cdef string matrix = ""
    cdef int i
    cdef int j
    cdef string row
    cdef int index
    for i in range(4):
        j = 0
        row = " ["

        for j in range(4):
            index = (m-4+i)*n + j
            val = f"{input[index]:.4f}"
            row = row + bytes(val, 'utf-8')
            if j < n-1:
                row = row + bytes(", ", 'utf-8')
        row = row + bytes("... ", 'utf-8')
        for j in range(4):
            index = (m-4+i)*n + (n-4+j)
            val = f"{input[index]:.4f}"
            row = row + bytes(val, 'utf-8')
            if j < 4-1:
                row = row + bytes(", ", 'utf-8')
        if i < 4-1:
            row = row + bytes("]", 'utf-8') + bytes("\n", 'utf-8')
        else:
            row = row + bytes("]", 'utf-8')
        matrix = matrix + row
    
    matrix = matrix + bytes("]", 'utf-8')
    return matrix

    

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

def largeM(input, int m, int n):
    matrix = upper(input, m, n)
    matrix = matrix + bytes(" "*(n*8//2) + "..." + " "*(n*8//2), 'utf-8') + bytes("\n", 'utf-8')
    matrix = matrix + lower(input, m, n)
    return matrix

def largeN(input, int m, int n):
    matrix = largeN_upper(input, m, n)
    matrix = matrix + bytes("]", 'utf-8')
    return matrix

def largeMN(input, int m, int n):
    matrix = largeN_upper(input, 4, n) + bytes("\n", 'utf-8')
    matrix = matrix + bytes(" "*34 + "..." + " "*34, 'utf-8') + bytes("\n", 'utf-8')
    matrix = matrix + largeN_lower(input, m, n)
    return matrix

