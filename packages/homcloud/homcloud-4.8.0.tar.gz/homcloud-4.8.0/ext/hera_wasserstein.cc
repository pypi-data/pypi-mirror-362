#pragma GCC diagnostic ignored "-Wunused-function"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"

#include "homcloud_common.h"
#include "homcloud_numpy.h"

#include "hera_common.h"
#include <hera/wasserstein.h>

#include <vector>
#include <utility>
#include <cmath>
#include <iostream>

static PyObject* wasserstein_distance(PyObject* self, PyObject* args) {
  PyObject* births_1;
  PyObject* deaths_1;
  PyObject* births_2;
  PyObject* deaths_2;
  double power;
  double internal_p;
  double delta;
  
  if (!PyArg_ParseTuple(args, "OOOOddd", &births_1, &deaths_1, &births_2, &deaths_2,
                        &power, &internal_p, &delta))
    return nullptr;

  Pairs pd1, pd2;
  if (!BirthDeath2Pairs(births_1, deaths_1, &pd1))
    return nullptr;
  if (!BirthDeath2Pairs(births_2, deaths_2, &pd2))
    return nullptr;

  if (power < 1.0) {
    PyErr_SetString(PyExc_ValueError, "power must larger than or equal to 1.0");
    return nullptr;
  }
  if (delta < 0.0) {
    PyErr_SetString(PyExc_ValueError, "delta must be zero or positive");
    return nullptr;
  }

  if (internal_p < 1.0) {
    PyErr_SetString(PyExc_ValueError, "internal_p must be larger than or equal to 1.0 or +inf");
    return nullptr;
  }

  hera::AuctionParams<double> params;
  params.wasserstein_power = power;
  params.delta = delta;
  params.internal_p = std::isinf(internal_p) ? hera::get_infinity<double>() : internal_p;
  
  try {
    return Py_BuildValue("d", hera::wasserstein_dist(pd1, pd2, params));
  } catch (const std::runtime_error& e) {
    PyErr_Format(PyExc_RuntimeError, "wasserstein_distance: %s", e.what());
    return nullptr;
  }
}


static PyMethodDef hera_wasserstein_Methods[] = {
  {"wasserstein_distance", (PyCFunction)wasserstein_distance, METH_VARARGS,
   "Compute wasserstein distance between two diagrams"},
  {NULL, NULL, 0, NULL},
};

static PyModuleDef hera_wasserstein_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.hera_wasserstein",
  "The module for hera's wasserstein distance",
  -1,
  hera_wasserstein_Methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_hera_wasserstein()
{
  PyObject* module = PyModule_Create(&hera_wasserstein_Module);
  if (!module)
    return nullptr;

  import_array();

  return module;
}
