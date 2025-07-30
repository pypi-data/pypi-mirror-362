// -*- mode: c++ -*-
#pragma GCC diagnostic ignored "-Wunused-function"
#include "homcloud_common.h"
#include "homcloud_cgal.h"

static PyModuleDef cgal_info_Moudle = {
  PyModuleDef_HEAD_INIT,
  "homcloud.cgal_info",
  "The module which has cgal information such as version",
  -1,
};

PyMODINIT_FUNC
PyInit_cgal_info()
{
  PyObject* module = PyModule_Create(&cgal_info_Moudle);
  
  if (!module)
    return NULL;

  PyObject* version_string = PyUnicode_FromString(CGAL_VERSION_STR);
  PyModule_AddObject(module, "version", version_string);

  PyObject* version_number = PyLong_FromLong(CGAL_VERSION_NR);
  PyModule_AddObject(module, "numerical_version", version_number);
  
  return module;
}
