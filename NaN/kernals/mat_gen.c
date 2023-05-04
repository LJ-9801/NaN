#define PY_SSIZE_T_CLEAN
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <pthread.h>
#include "mat_gen.h"
#define NUM_THREADS 8

void *drandfill_thread(void *arg)
{
    double_data_t *data = (double_data_t *)arg;

    unsigned int seed = time(NULL) ^ (data->thread_id + (data->thread_id << 16));

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = (double)rand_r(&seed) / (double)RAND_MAX * (data->r2 - data->r1) + data->r1;
    }

    return NULL;
}

void *srandfill_thread(void *arg)
{
    float_data_t *data = (float_data_t *)arg;

    unsigned int seed = time(NULL) ^ (data->thread_id + (data->thread_id << 16));

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = (float)rand_r(&seed) / (float)RAND_MAX * (data->r2 - data->r1) + data->r1;
    }

    return NULL;
}

void *dzero_thread(void *arg)
{
    double_data_t *data = (double_data_t *)arg;

    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = 0.0;
    }

    return NULL;
}

void *szero_thread(void *arg){
    float_data_t *data = (float_data_t *)arg;
    for (int t = data->start; t < data->end; t++)
    {
        data->array[t] = 0.0;
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

void drandfill(const int n1, const double r1, const double r2, double *array)
{
    srand(time(NULL));
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
    srand(time(NULL));

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

    int chunk_size = n1 / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        double_data[i].thread_id = i;
        double_data[i].start = i * chunk_size;
        double_data[i].end = (i == NUM_THREADS - 1) ? n1 : (i + 1) * chunk_size;
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

    int chunk_size = n1 / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        float_data[i].thread_id = i;
        float_data[i].start = i * chunk_size;
        float_data[i].end = (i == NUM_THREADS - 1) ? n1 : (i + 1) * chunk_size;
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
    int t,j;
    //#pragma omp parallel for private(t,j)
    for(t=0;t<n;t++)
    {
        for(j=0;j<n;j++)
        {
            if(t == j) array[j + t*n] = 1.0;
            else array[j + t*n] = 0.0;
        }
    }
    //#pragma omp barrier
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
