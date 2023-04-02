#define __mat_gen_h__
#ifdef __mat_gen_h__

// double precision
void drandfill(const int n1, const double r1, const double r2, double *array);
void dzeros(const int n1, const int n2, double *array);
void deye(int n, double *array);
void drot3(double *array, double theta, int axis);
void drot2(double *array, double theta);

// single precision
void srandfill(const int n1, const float r1, const float r2, float *array);
void szeros(const int n1, const int n2, float *array);
void seye(int n, float *array);
void srot3(float *array, float theta, int axis);
void srot2(float *array, float theta);
#endif