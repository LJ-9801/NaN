#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <omp.h>


PyObject *tolist(PyObject *self ,PyObject *args)
{
    int n1;
    int n2;
    PyObject *list;

    if(!PyArg_ParseTuple(args, "iiO", &n1, &n2, &list))
        return NULL;

    if(!PyList_Check(list))
        return NULL;

    PyObject *newlist = PyList_New(n1);
    for (int i = 0; i < n1; i++)
    {
        PyObject *tmp = PyList_New(n2);
        for (int j = 0; j < n2; j++)
        {
            PyObject *item = PyList_GetItem(list, i*n2+j);
            double item_ptr = PyFloat_AsDouble(item);
            PyList_SetItem(tmp, j, PyFloat_FromDouble(item_ptr));
        }
        PyList_SetItem(newlist, i, tmp);
    }

    Py_DECREF(list);
    return newlist;
}


static PyMethodDef methods[] = {
    {"tolist", (PyCFunction)tolist, METH_VARARGS},
    {NULL, NULL}
};

static struct PyModuleDef data_transfer = {
    PyModuleDef_HEAD_INIT,
    "data_transfer",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_data_transfer(void)
{
    return PyModule_Create(&data_transfer);
}