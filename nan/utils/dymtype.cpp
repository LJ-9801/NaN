#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <string>
#include <iostream>


static PyObject *POINTER = NULL;
static PyObject *c_double = NULL;
static PyObject *c_float = NULL;
static PyObject *from_address = NULL;

static PyObject *toctypes(PyObject *self, PyObject *args) {
    PyObject *obj;
    Py_buffer view;
    if (!PyArg_ParseTuple(args, "O", &obj)) {
        return NULL;
    }

    if (PyObject_GetBuffer(obj, &view, PyBUF_SIMPLE) != 0) {
        return NULL;
    }

    if (view.ndim != 1) {
        PyErr_SetString(PyExc_TypeError, "Expected a 1-dimensional array");
        PyBuffer_Release(&view);
        return NULL;
    }

    double *data = (double *)view.buf;
    PyObject* double_pointer_type = PyObject_CallFunction(POINTER, "O", c_double);
    if (double_pointer_type == NULL) {
        PyBuffer_Release(&view);
        return NULL;
    }

    PyObject* arglist = Py_BuildValue("(lO)", (long)data, double_pointer_type);
    if (arglist == NULL) {
        PyBuffer_Release(&view);
        return NULL;
    }

    PyObject* result = PyObject_CallObject(from_address, arglist);

    Py_DECREF(arglist);
    Py_DECREF(double_pointer_type);

    return result;
}

static PyMethodDef DymtypeMethods[] = {
    {"toctypes", toctypes, METH_VARARGS, "Convert a numpy array to a ctypes pointer"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef dymtype_module = {
    PyModuleDef_HEAD_INIT,
    "dymtype",
    "Convert a numpy array to a ctypes pointer",
    -1,
    DymtypeMethods
};

PyMODINIT_FUNC PyInit_dymtype(void){
    PyObject *m = PyModule_Create(&dymtype_module);
    if (m == NULL) {
        return NULL;
    }

    PyObject *ctypes = PyImport_ImportModule("ctypes");
    if (ctypes == NULL) {
        return NULL;
    }

    POINTER = PyObject_GetAttrString(ctypes, "POINTER");
    c_double = PyObject_GetAttrString(ctypes, "c_double");
    c_float = PyObject_GetAttrString(ctypes, "c_float");
    from_address = PyObject_GetAttrString(ctypes, "cast");

    Py_INCREF(POINTER);
    Py_INCREF(c_double);
    Py_INCREF(c_float);
    Py_INCREF(from_address);

    return m;
}