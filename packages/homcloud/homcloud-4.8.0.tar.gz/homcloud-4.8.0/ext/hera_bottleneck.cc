#pragma GCC diagnostic ignored "-Wunused-function"

#include "homcloud_common.h"
#include "homcloud_numpy.h"

#include "hera_common.h"
#include <hera/bottleneck.h>

static PyObject* bottleneck_distance(PyObject* self, PyObject* args) {
  PyObject* births_1;
  PyObject* deaths_1;
  PyObject* births_2;
  PyObject* deaths_2;
  double delta;
  
  if (!PyArg_ParseTuple(args, "OOOOd", &births_1, &deaths_1, &births_2, &deaths_2, &delta))
    return nullptr;

  Pairs pd1, pd2;
  if (!BirthDeath2Pairs(births_1, deaths_1, &pd1))
    return nullptr;
  if (!BirthDeath2Pairs(births_2, deaths_2, &pd2))
    return nullptr;

  if (delta < 0.0) {
    PyErr_SetString(PyExc_ValueError, "delta must be zero or positive");
    return nullptr;
  }

  if (delta == 0.0) {
    return Py_BuildValue("d", hera::bottleneckDistExact(pd1, pd2));
  } else {
    return Py_BuildValue("d", hera::bottleneckDistApprox(pd1, pd2, delta));
  }
}

static PyMethodDef hera_bottleneck_Methods[] = {
  {"bottleneck_distance", (PyCFunction)bottleneck_distance, METH_VARARGS,
   "Compute bottleneck distance between two diagrams"},
  {NULL, NULL, 0, NULL},
};

static PyModuleDef hera_bottleneck_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.hera_bottleneck",
  "The module for hera's bottleneck distance",
  -1,
  hera_bottleneck_Methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_hera_bottleneck()
{
  PyObject* module = PyModule_Create(&hera_bottleneck_Module);
  if (!module)
    return nullptr;

  import_array();

  return module;
}
