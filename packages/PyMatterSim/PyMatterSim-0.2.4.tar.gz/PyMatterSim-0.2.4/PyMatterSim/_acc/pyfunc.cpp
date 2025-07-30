#include "func.hpp"
#include "wignerSymbols.h"
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

PYBIND11_MODULE(acc, m) {
  m.def("Wignerindex", &Wignerindex).def("SphHarm6", &SphHarm6);
}