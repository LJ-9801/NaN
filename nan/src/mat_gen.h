#define __mat_gen_h__
#ifdef __mat_gen_h__
#include <random>

// data structure for thread
typedef struct double_data {
    int thread_id;
    int start;
    int end;
    int n1;
    double r1;
    double r2;
    double *array;
} double_data_t;

typedef struct float_data {
    int thread_id;
    int start;
    int end;
    int n1;
    float r1;
    float r2;
    float *array;
} float_data_t;

// thread function (double)
void *drandfill_thread(void *threadarg);
void *drandn_thread(void *threadarg);
void *dzero_thread(void *arg);
void *deye_thread(void *arg);


// thread function (float)
void *srandfill_thread(void *threadarg);
void *srandn_thread(void *threadarg);
void *szero_thread(void *arg);
void *seye_thread(void *arg);

// double precision
void drandfill(const int n1, const double r1, const double r2, double *array);
void drandnfill(const int n1, const double mean, const double std, double *array);
void dzeros(const int n1, const int n2, double *array);
void deye(int n, double *array);
void drot3(double *array, double theta, int axis);
void drot2(double *array, double theta);

// single precision
void srandfill(const int n1, const float r1, const float r2, float *array);
void srandnfill(const int n1, const float mean, const float std, float *array);
void szeros(const int n1, const int n2, float *array);
void seye(int n, float *array);
void srot3(float *array, float theta, int axis);
void srot2(float *array, float theta);

//Python interface (double)
PyObject* drand_wrapper(PyObject *self, PyObject *args);
PyObject* drandn_wrapper(PyObject *self, PyObject *args);
PyObject* dzeros_wrapper(PyObject *self, PyObject *args);
PyObject* deye_wrapper(PyObject *self, PyObject *args);
PyObject* drot3_wrapper(PyObject *self, PyObject *args);
PyObject* drot2_wrapper(PyObject *self, PyObject *args);

//Python interface (float)
PyObject* srand_wrapper(PyObject *self, PyObject *args);
PyObject* srandn_wrapper(PyObject *self, PyObject *args);
PyObject* szeros_wrapper(PyObject *self, PyObject *args);
PyObject* seye_wrapper(PyObject *self, PyObject *args);
PyObject* srot3_wrapper(PyObject *self, PyObject *args);
PyObject* srot2_wrapper(PyObject *self, PyObject *args);
#endif