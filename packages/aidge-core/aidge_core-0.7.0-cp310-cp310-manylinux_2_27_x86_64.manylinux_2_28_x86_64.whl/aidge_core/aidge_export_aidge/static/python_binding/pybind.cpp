#include <pybind11/pybind11.h>

#include "dnn.hpp"

namespace py = pybind11;


void init_export(py::module& m){
    m.def("generate_model", generateModel);
}

PYBIND11_MODULE(export, m) {
    init_export(m);
}
