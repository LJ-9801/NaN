#define PY_SSIZE_T_CLEAN
//#include <Python.h>
#include <stdio.h>
//#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <omp.h>
#include "mat_gen.h"

// make this file into universal binary    
void drandfill(const int n1, const double r1, const double r2, double *array)
{
    int t;
    srand((unsigned int)time(NULL));

    #pragma omp parallel for private(t)
    for(t=0;t<n1;t++)
    {
        array[t] = (double)rand() / (double)RAND_MAX * (r2 - r1) + r1;
    }
}


void srandfill(const int n1, const float r1, const float r2, float *array)
{
    int t;
    srand((unsigned int)time(NULL));

    #pragma omp parallel for private(t)
    for(t=0;t<n1;t++)
    {
        array[t] = (float)rand() / (float)RAND_MAX * (r2 - r1) + r1;
    }
}

//generate zeros matrix
void dzeros(const int n1, const int n2, double *array){
    int t,j;
    #pragma omp parallel for private(t,j)
    for(t=0;t<n1;t++)
    {
        for(j=0;j<n2;j++)
        {
            array[j + t*n1] = 0.0;
        }
    }
}

void szeros(const int n1, const int n2, float *array){
    int t,j;
    #pragma omp parallel for private(t,j)
    for(t=0;t<n1;t++)
    {
        for(j=0;j<n2;j++)
        {
            array[j + t*n1] = 0.0;
        }
    }
}

// generate identity matrix
void deye(int n, double *array){
    int t,j;
    #pragma omp parallel for private(t,j)
    for(t=0;t<n;t++)
    {
        for(j=0;j<n;j++)
        {
            if(t == j) array[j + t*n] = 1.0;
            else array[j + t*n] = 0.0;
        }
    }
}

void seye(int n, float *array){
    int t,j;
    #pragma omp parallel for private(t,j)
    for(t=0;t<n;t++)
    {
        for(j=0;j<n;j++)
        {
            if(t == j) array[j + t*n] = 1.0;
            else array[j + t*n] = 0.0;
        }
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
