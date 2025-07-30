#ifndef FUNC_H
#define FUNC_H
#include <vector>
#include <vector>
#include <complex>
#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
std::vector<std::vector<double>> Wignerindex(int l);
std::vector<std::complex<double>> SphHarm6(double theta, double phi);
#endif // FUNC_H