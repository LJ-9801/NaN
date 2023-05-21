#define PY_SSIZE_T_CLEAN
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <pthread.h>
#include <Python.h>
#include "mat_gen.h"
#define NUM_THREADS 8

void *drandn_thread(void *arg){
    double_data_t *data = (double_data_t *)arg;
    std::mt19937 gen(data->thread_id ^ (unsigned int)time(NULL));
    double mean = data->r1;
    double std = data->r2;
    std::normal_distribution<double> dis(mean, std);

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = dis(gen);
    }

    return NULL;
}

void *srandn_thread(void *arg){
    float_data_t *data = (float_data_t *)arg;
    std::mt19937 gen(data->thread_id ^ (unsigned int)time(NULL));
    float mean = data->r1;
    float std = data->r2;
    std::normal_distribution<float> dis(mean, std);

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = dis(gen);
    }

    return NULL;
}

void *drandfill_thread(void *arg)
{
    double_data_t *data = (double_data_t *)arg;
    std::mt19937 gen(data->thread_id ^ (unsigned int)time(NULL));
    double a = data->r1;
    double b = data->r2;
    std::uniform_real_distribution<> dis(a, b);

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = (double)dis(gen);
    }

    return NULL;
}

void *srandfill_thread(void *arg)
{
    float_data_t *data = (float_data_t *)arg;

    std::mt19937 gen(data->thread_id ^ (unsigned int)time(NULL));
    float a = data->r1;
    float b = data->r2;
    std::uniform_real_distribution<> dis(a, b);

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = (float)dis(gen);
    }

    return NULL;
}

void *dzero_thread(void *arg)
{
    double_data_t *data = (double_data_t *)arg;

    for (int t = data->start; t < data->end; t++)
    {
        double zero = (double)0.0;
        data->array[t] = zero;
    }

    return NULL;
}

void *szero_thread(void *arg){
    float_data_t *data = (float_data_t *)arg;
    for (int t = data->start; t < data->end; t++)
    {
        float zero = (float)0.0;
        data->array[t] = zero;
    }
    return NULL;
}

void *deye_thread(void *arg){
    double_data_t *data = (double_data_t *)arg;
    int n1 = data->n1;

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = ((t % (n1+1)) == 0) ? 1.0 : 0.0;
    }
    return NULL;
}

void *seye_thread(void *arg){
    float_data_t *data = (float_data_t *)arg;
    int n1 = data->n1;

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = ((t % (n1+1)) == 0) ? 1.0 : 0.0;
    }
    return NULL;
}


void drandnfill(const int n1, const double mean, const double std, double* array){
    pthread_t threads[NUM_THREADS];
    double_data_t double_data[NUM_THREADS];

    int chunk_size = n1 / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        double_data[i].thread_id = i;
        double_data[i].start = i * chunk_size;
        double_data[i].end = (i == NUM_THREADS - 1) ? n1 : (i + 1) * chunk_size;
        double_data[i].r1 = mean;
        double_data[i].r2 = std;
        double_data[i].array = array;
        pthread_create(&threads[i], NULL, drandn_thread, &double_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
}

void srandnfill(const int n1, const float mean, const float std, float* array){
    
    pthread_t threads[NUM_THREADS];
    float_data_t float_data[NUM_THREADS];

    int chunk_size = n1 / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        float_data[i].thread_id = i;
        float_data[i].start = i * chunk_size;
        float_data[i].end = (i == NUM_THREADS - 1) ? n1 : (i + 1) * chunk_size;
        float_data[i].r1 = mean;
        float_data[i].r2 = std;
        float_data[i].array = array;
        pthread_create(&threads[i], NULL, srandn_thread, &float_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
}

void drandfill(const int n1, const double r1, const double r2, double *array)
{
    pthread_t threads[NUM_THREADS];
    double_data_t double_data[NUM_THREADS];

    int chunk_size = n1 / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        double_data[i].thread_id = i;
        double_data[i].start = i * chunk_size;
        double_data[i].end = (i == NUM_THREADS - 1) ? n1 : (i + 1) * chunk_size;
        double_data[i].r1 = r1;
        double_data[i].r2 = r2;
        double_data[i].array = array;
        pthread_create(&threads[i], NULL, drandfill_thread, &double_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
}

void srandfill(const int n1, const float r1, const float r2, float *array)
{
    pthread_t threads[NUM_THREADS];
    float_data_t float_data[NUM_THREADS];

    int chunk_size = n1 / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        float_data[i].thread_id = i;
        float_data[i].start = i * chunk_size;
        float_data[i].end = (i == NUM_THREADS - 1) ? n1 : (i + 1) * chunk_size;
        float_data[i].r1 = r1;
        float_data[i].r2 = r2;
        float_data[i].array = array;
        pthread_create(&threads[i], NULL, srandfill_thread, &float_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
}

//generate zeros matrix
void dzeros(const int n1, const int n2, double *array){
    pthread_t threads[NUM_THREADS];
    double_data_t double_data[NUM_THREADS];
    int n = n1*n2;

    int chunk_size = n / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        double_data[i].thread_id = i;
        double_data[i].start = i * chunk_size;
        double_data[i].end = (i == NUM_THREADS - 1) ? n : (i + 1) * chunk_size;
        double_data[i].array = array;
        pthread_create(&threads[i], NULL, dzero_thread, &double_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

}

void szeros(const int n1, const int n2, float *array){
    pthread_t threads[NUM_THREADS];
    float_data_t float_data[NUM_THREADS];
    int n = n1*n2;
    int chunk_size = n / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        float_data[i].thread_id = i;
        float_data[i].start = i * chunk_size;
        float_data[i].end = (i == NUM_THREADS - 1) ? n : (i + 1) * chunk_size;
        float_data[i].array = array;
        pthread_create(&threads[i], NULL, szero_thread, &float_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
}

// generate identity matrix
void deye(int n, double *array){
    pthread_t threads[NUM_THREADS];
    double_data_t double_data[NUM_THREADS];

    int chunk_size = n*n / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        double_data[i].thread_id = i;
        double_data[i].start = i * chunk_size;
        double_data[i].n1 = n;
        double_data[i].end = (i == NUM_THREADS - 1) ? (n*n) : (i + 1) * chunk_size;
        double_data[i].array = array;

        pthread_create(&threads[i], NULL, deye_thread, &double_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
}

void seye(int n, float *array){
    pthread_t threads[NUM_THREADS];
    float_data_t float_data[NUM_THREADS];

    int chunk_size = n*n / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        float_data[i].thread_id = i;
        float_data[i].start = i * chunk_size;
        float_data[i].n1 = n;
        float_data[i].end = (i == NUM_THREADS - 1) ? (n*n) : (i + 1) * chunk_size;
        float_data[i].array = array;

        pthread_create(&threads[i], NULL, seye_thread, &float_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
}

void drot3(double *array, double theta, int axis){
    if (axis == 0)
    {
        array[0] = 1.0;
        array[1] = 0.0;
        array[2] = 0.0;
        array[3] = 0.0;
        array[4] = cos(theta);
        array[5] = -sin(theta);
        array[6] = 0.0;
        array[7] = sin(theta);
        array[8] = cos(theta);
    }else if (axis == 1)
    {
        array[0] = cos(theta);
        array[1] = 0.0;
        array[2] = sin(theta);
        array[3] = 0.0;
        array[4] = 1.0;
        array[5] = 0.0;
        array[6] = -sin(theta);
        array[7] = 0.0;
        array[8] = cos(theta);
    }else if (axis == 2)
    {
        array[0] = cos(theta);
        array[1] = -sin(theta);
        array[2] = 0.0;
        array[3] = sin(theta);
        array[4] = cos(theta);
        array[5] = 0.0;
        array[6] = 0.0;
        array[7] = 0.0;
        array[8] = 1.0;
    }
}

void srot3(float *array, float theta, int axis){
    if (axis == 0)
    {
        array[0] = 1.0;
        array[1] = 0.0;
        array[2] = 0.0;
        array[3] = 0.0;
        array[4] = cos(theta);
        array[5] = -sin(theta);
        array[6] = 0.0;
        array[7] = sin(theta);
        array[8] = cos(theta);
    }else if (axis == 1)
    {
        array[0] = cos(theta);
        array[1] = 0.0;
        array[2] = sin(theta);
        array[3] = 0.0;
        array[4] = 1.0;
        array[5] = 0.0;
        array[6] = -sin(theta);
        array[7] = 0.0;
        array[8] = cos(theta);
    }else if (axis == 2)
    {
        array[0] = cos(theta);
        array[1] = -sin(theta);
        array[2] = 0.0;
        array[3] = sin(theta);
        array[4] = cos(theta);
        array[5] = 0.0;
        array[6] = 0.0;
        array[7] = 0.0;
        array[8] = 1.0;
    }
}


void drot2(double *array, double theta){
    array[0] = cos(theta);
    array[1] = -sin(theta);
    array[2] = sin(theta);
    array[3] = cos(theta);
}

void srot2(float *array, float theta){
    array[0] = cos(theta);
    array[1] = -sin(theta);
    array[2] = sin(theta);
    array[3] = cos(theta);
}

static PyObject *POINTER = NULL;
static PyObject *c_double = NULL;
static PyObject *c_float = NULL;
static PyObject *from_address = NULL;

PyObject* dzeros_wrapper(PyObject *self, PyObject *args){
    int n1, n2;
    if (!PyArg_ParseTuple(args, "ii", &n1, &n2))
        return NULL;
    double *array = (double *)malloc(n1*n2*sizeof(double));
    dzeros(n1, n2, array);

    PyObject* double_pointer_type = PyObject_CallFunction(POINTER, "O", c_double);
    if (double_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, double_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* double_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(double_pointer_type);
    Py_DECREF(arglist);

    return double_array;   
}

PyObject* szeros_wrapper(PyObject *self, PyObject *args){
    int n1, n2;
    if (!PyArg_ParseTuple(args, "ii", &n1, &n2))
        return NULL;
    float *array = (float *)malloc(n1*n2*sizeof(float));
    szeros(n1, n2, array);

    PyObject* float_pointer_type = PyObject_CallFunction(POINTER, "O", c_float);
    if (float_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, float_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* float_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(float_pointer_type);
    Py_DECREF(arglist);

    return float_array;
}

PyObject* drand_wrapper(PyObject *self, PyObject *args){
    int n1,r1,r2;
    if (!PyArg_ParseTuple(args, "iii", &n1, &r1, &r2))
        return NULL;
    double *array = (double *)malloc(n1*sizeof(double));
    drandfill(n1,r1,r2,array);

    PyObject* double_pointer_type = PyObject_CallFunction(POINTER, "O", c_double);
    if (double_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, double_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* double_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(double_pointer_type);
    Py_DECREF(arglist);

    return double_array;   
}

PyObject* srand_wrapper(PyObject *self, PyObject *args){
    int n1,r1,r2;
    if (!PyArg_ParseTuple(args, "iii", &n1, &r1, &r2))
        return NULL;
    float *array = (float *)malloc(n1*sizeof(float));
    srandfill(n1,r1,r2,array);

    PyObject* float_pointer_type = PyObject_CallFunction(POINTER, "O", c_float);
    if (float_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, float_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* float_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(float_pointer_type);
    Py_DECREF(arglist);

    return float_array;
}

PyObject* drandn_wrapper(PyObject *self, PyObject *args){
    int n1,r1,r2;
    if (!PyArg_ParseTuple(args, "iii", &n1, &r1, &r2))
        return NULL;
    double *array = (double *)malloc(n1*sizeof(double));
    drandnfill(n1,r1,r2,array);

    PyObject* double_pointer_type = PyObject_CallFunction(POINTER, "O", c_double);
    if (double_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, double_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* double_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(double_pointer_type);
    Py_DECREF(arglist);

    return double_array;   
}

PyObject* srandn_wrapper(PyObject *self, PyObject *args){
    int n1,r1,r2;
    if (!PyArg_ParseTuple(args, "iii", &n1, &r1, &r2))
        return NULL;
    float *array = (float *)malloc(n1*sizeof(float));
    srandnfill(n1,r1,r2,array);

    PyObject* float_pointer_type = PyObject_CallFunction(POINTER, "O", c_float);
    if (float_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, float_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* float_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(float_pointer_type);
    Py_DECREF(arglist);

    return float_array;
}

PyObject* deye_wrapper(PyObject *self, PyObject *args){
    int n1;
    if (!PyArg_ParseTuple(args, "i", &n1))
        return NULL;
    double *array = (double *)malloc(n1*n1*sizeof(double));
    deye(n1, array);

    PyObject* double_pointer_type = PyObject_CallFunction(POINTER, "O", c_double);
    if (double_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, double_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* double_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(double_pointer_type);
    Py_DECREF(arglist);

    return double_array;   
}

PyObject* seye_wrapper(PyObject *self, PyObject *args){
    int n1;
    if (!PyArg_ParseTuple(args, "i", &n1))
        return NULL;
    float *array = (float *)malloc(n1*n1*sizeof(float));
    seye(n1, array);

    PyObject* float_pointer_type = PyObject_CallFunction(POINTER, "O", c_float);
    if (float_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, float_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* float_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(float_pointer_type);
    Py_DECREF(arglist);

    return float_array;
}

PyObject* drot2_wrapper(PyObject *self, PyObject *args){
    double theta;
    if (!PyArg_ParseTuple(args, "d", &theta))
        return NULL;
    double *array = (double *)malloc(4*sizeof(double));
    drot2(array, theta);

    PyObject* double_pointer_type = PyObject_CallFunction(POINTER, "O", c_double);
    if (double_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, double_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* double_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(double_pointer_type);
    Py_DECREF(arglist);

    return double_array;   
}

PyObject* srot2_wrapper(PyObject *self, PyObject *args){
    float theta;
    if (!PyArg_ParseTuple(args, "f", &theta))
        return NULL;
    float *array = (float *)malloc(4*sizeof(float));
    srot2(array, theta);

    PyObject* float_pointer_type = PyObject_CallFunction(POINTER, "O", c_float);
    if (float_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, float_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* float_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(float_pointer_type);
    Py_DECREF(arglist);

    return float_array;
}

PyObject* drot3_wrapper(PyObject* self, PyObject* args){
    int phi;
    double theta;
    if (!PyArg_ParseTuple(args, "di", &theta, &phi))
        return NULL;
    double *array = (double *)malloc(9*sizeof(double));
    drot3(array, theta, phi);

    PyObject* double_pointer_type = PyObject_CallFunction(POINTER, "O", c_double);
    if (double_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, double_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* double_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(double_pointer_type);
    Py_DECREF(arglist);

    return double_array;   
}

PyObject* srot3_wrapper(PyObject* self, PyObject* args){
    int phi;
    float theta;
    if (!PyArg_ParseTuple(args, "fi", &theta, &phi))
        return NULL;
    float *array = (float *)malloc(9*sizeof(float));
    srot3(array, theta, phi);

    PyObject* float_pointer_type = PyObject_CallFunction(POINTER, "O", c_float);
    if (float_pointer_type == NULL)
        return NULL;
    
    PyObject* arglist = Py_BuildValue("(lO)", (long)array, float_pointer_type);
    if (arglist == NULL)
        return NULL;
    
    PyObject* float_array = PyObject_CallObject(from_address, arglist);

    Py_DECREF(float_pointer_type);
    Py_DECREF(arglist);

    return float_array;
}

static PyMethodDef module_methods[] = {
    {"dzeros", dzeros_wrapper, METH_VARARGS, "Create a double array filled with zeros"},
    {"szeros", szeros_wrapper, METH_VARARGS, "Create a float array filled with zeros"},
    {"drand", drand_wrapper, METH_VARARGS, "Create a double array filled with random numbers"},
    {"srand", srand_wrapper, METH_VARARGS, "Create a float array filled with random numbers"},
    {"drandn", drandn_wrapper, METH_VARARGS, "Create a double array filled with random numbers from a normal distribution"},
    {"srandn", srandn_wrapper, METH_VARARGS, "Create a float array filled with random numbers from a normal distribution"},
    {"deye", deye_wrapper, METH_VARARGS, "Create a double identity matrix"},
    {"seye", seye_wrapper, METH_VARARGS, "Create a float identity matrix"},
    {"drot2", drot2_wrapper, METH_VARARGS, "Create a double 2D rotation matrix"},
    {"srot2", srot2_wrapper, METH_VARARGS, "Create a float 2D rotation matrix"},
    {"drot3", drot3_wrapper, METH_VARARGS, "Create a double 3D rotation matrix"},
    {"srot3", srot3_wrapper, METH_VARARGS, "Create a float 3D rotation matrix"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "carray",
    NULL,
    -1,
    module_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_carray(void){
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m)
        return NULL;
    PyObject* ctypes = PyImport_ImportModule("ctypes");
    if (ctypes == NULL)
        return NULL;
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