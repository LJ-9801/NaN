#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#define PRECISION 4


void findMaxLength(double *data, int startn, int startm, int m, int n, int &maxlen) {
    for (int i = startn; i < m; i++) {
        for (int j = startm; j < n; j++) {
            std::string st = std::to_string(data[i * n + j]);
            std::string val = st.substr(0, st.find(".") + PRECISION + 1);
            if (val.length() > maxlen) {maxlen = val.length();}
        }
    }
}

void upper(double *data, int m, int n, std::string &s, int maxlen) {
    s+= "[";
    std::string row = "";
    for (int i = 0; i < 4; i++) {
        if (i == 0) {row = "[";} 
        else {row = " [";}
        for (int j = 0; j < n; j++) {
            std::string st = std::to_string(data[i * n + j]);
            std::string val = st.substr(0, st.find(".") + PRECISION + 1);
            std::string bl(maxlen - val.length(), ' ');
            row += (bl + val);
            if (j < n - 1) {row += ", ";}
        }
        if(i < m-1){row += "]\n";} 
        else {row += "]";}
        s += row;
    }
}

void lower(double *data, int m, int n, std::string &s, int maxlen) {
    std::string row = "";
    int precision = 4;
    for (int i = m-4; i < m; i++) {
        row = " [";
        for (int j = 0; j < n; j++) {
           std::string st = std::to_string(data[i * n + j]);
            std::string val = st.substr(0, st.find(".") + PRECISION + 1);
            std::string bl(maxlen - val.length(), ' ');
            row += (bl + val);
            if (j < n - 1) {row += ", ";}
        }
        if(i < 3){row += "]\n";} 
        else {row += "]";}
        s += row;
    }
    s += "]";
}

void largeN_upper(double *data, int m, int n, std::string &s, int maxlen) {
    s+= "[";
    std::string row = "";
    for (int i = 0; i < m; i++) {
        if (i == 0) {row = "[";} 
        else {row = " [";}
        for (int j = 0; j < 4; j++) {
            std::string st = std::to_string(data[i * n + j]);
            std::string val = st.substr(0, st.find(".") + PRECISION + 1);
            std::string bl(maxlen - val.length(), ' ');
            row += (bl + val);
            if (j < 3) {row += ", ";}
        }
        row += ", ... ,";
        for (int j = n - 4; j < n; j++) {
            std::string st = std::to_string(data[i * n + j]);
            std::string val = st.substr(0, st.find(".") + PRECISION + 1);
            std::string bl(maxlen - val.length(), ' ');
            row += (bl + val);
            if (j < n-1) {row += ", ";}
        }

        if(i < m-1){row += "]\n";} 
        else {row += "]";}
        s += row;
    }
}

void largeN_lower(double *data, int m, int n, std::string &s, int maxlen) {
    std::string row = "";
    for (int i = m-4; i < m; i++) {
        row = " [";
        for (int j = 0; j < 4; j++) {
            std::string st = std::to_string(data[i * n + j]);
            std::string val = st.substr(0, st.find(".") + PRECISION + 1);
            std::string bl(maxlen - val.length(), ' ');
            row += (bl + val);
            if (j < 3) {row += ", ";}
        }
        row += ", ... ,";
        for (int j = n - 4; j < n; j++) {
            std::string st = std::to_string(data[i * n + j]);
            std::string val = st.substr(0, st.find(".") + PRECISION + 1);
            std::string bl(maxlen - val.length(), ' ');
            row += (bl + val);
            if (j < n - 1) {row += ", ";}
        }

        if(i < m-1){row += "]\n";} 
        else {row += "]";}
        s += row;
    }
    s += "]";
}

void tostr(double* data, int m, int n, std::string& s, int maxlen){
    s = "[";
    std::string row = "";
    for (int i = 0; i < m; i++) {
        if (i == 0) {row = "[";} 
        else {row = " [";}
        for (int j = 0; j < n; j++) {
            std::string st = std::to_string(data[i * n + j]);
            std::string val = st.substr(0, st.find(".") + PRECISION + 1);
            std::string bl(maxlen - val.length(), ' ');
            row += (bl + val);
            if (j < n - 1) {row += ", ";}
        }
        if(i < m-1){row += "]\n";} 
        else {row += "]";}
        s += row;
    }
    s += "]";
}   


PyObject* normal(PyObject* self, PyObject* args) {
    PyObject* obj;
    int m, n;
    if (!PyArg_ParseTuple(args, "Oii", &obj, &m, &n)){
        return NULL;
    }
    Py_buffer view;
    if (PyObject_GetBuffer(obj, &view, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
        return NULL;
    }
    double* data = (double*)view.buf;
    std::string s = "";
    int maxlen = 0;
    findMaxLength(data, 0, 0, m, n, maxlen);
    tostr(data, m, n, s, maxlen);
    PyBuffer_Release(&view);
    return PyUnicode_FromString(s.c_str());
}

PyObject* largeM(PyObject* self, PyObject* args) {
    PyObject* obj;
    int m, n;
    if (!PyArg_ParseTuple(args, "Oii", &obj, &m, &n)){
        return NULL;
    }
    Py_buffer view;
    if (PyObject_GetBuffer(obj, &view, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
        return NULL;
    }
    double* data = (double*)view.buf;
    std::string s = "";
    int maxlen = 0;
    findMaxLength(data, 0, 0, 4, n, maxlen);
    upper(data, m, n, s, maxlen);
    s += std::string(n*8/2, ' ') + "...\n";
    maxlen = 0;
    findMaxLength(data, m-4, 0, m, n, maxlen);
    lower(data, m, n, s, maxlen);
    PyBuffer_Release(&view);
    return PyUnicode_FromString(s.c_str());
}

PyObject* largeN(PyObject* self, PyObject* args){
    PyObject* obj;
    int m, n;
    if (!PyArg_ParseTuple(args, "Oii", &obj, &m, &n)){
        return NULL;
    }
    Py_buffer view;
    if (PyObject_GetBuffer(obj, &view, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
        return NULL;
    }
    double* data = (double*)view.buf;
    std::string s = "";
    int maxlen = 0;
    findMaxLength(data, 0, 0, m, n, maxlen);
    largeN_upper(data, m, n, s, maxlen);
    s += "]";
    PyBuffer_Release(&view);
    return PyUnicode_FromString(s.c_str());
}

PyObject* largeMN(PyObject* self, PyObject* args){
    PyObject* obj;
    int m, n;
    if (!PyArg_ParseTuple(args, "Oii", &obj, &m, &n)){
        return NULL;
    }
    Py_buffer view;
    if (PyObject_GetBuffer(obj, &view, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
        return NULL;
    }
    double* data = (double*)view.buf;
    std::string s = "";
    int maxlen = 0;
    findMaxLength(data, 0, 0, 4, n, maxlen);
    largeN_upper(data, 4, n, s, maxlen);
    s += "\n";
    s += std::string((maxlen+2)*4+2, ' ') + "...\n";
    maxlen = 0;
    findMaxLength(data, m-4, 0, m, n, maxlen);
    largeN_lower(data, m, n, s, maxlen);
    PyBuffer_Release(&view);
    return PyUnicode_FromString(s.c_str());
}


static PyMethodDef methods[] = {
    {"normal", normal, METH_VARARGS, "normal"},
    {"largeM", largeM, METH_VARARGS, "largeM"},
    {"largeN", largeN, METH_VARARGS, "largeN"},
    {"largeMN", largeMN, METH_VARARGS, "largeMN"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "mtostr",
    "matrix",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_mtostr(void) {
    return PyModule_Create(&module);
}