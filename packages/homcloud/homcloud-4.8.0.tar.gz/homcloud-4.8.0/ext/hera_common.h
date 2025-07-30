// -*- mode: c++ -*-
#ifndef HOMCLOUD_HERA_COMMON_H
#define HOMCLOUD_HERA_COMMON_H

#include <vector>
#include <utility>

// Define ssize_t for hera
#if (PY_VERSION_HEX >= 0x030a0000) && !HAVE_SSIZE_T && defined(_MSC_VER)
using ssize_t = Py_ssize_t;
#endif

using Pairs = std::vector<std::pair<double, double>>;

static PyArrayObject* ToArray(PyObject* ary) {
  return reinterpret_cast<PyArrayObject*>(PyArray_FROM_OT(ary, NPY_DOUBLE));
}

static bool BirthDeath2Pairs(PyObject* births, PyObject* deaths, Pairs* pairs) {
  PyArrayObject* births_ = nullptr;
  PyArrayObject* deaths_ = nullptr;
  
  births_ = ToArray(births);
  if (!births_) goto error;
  
  deaths_ = ToArray(deaths);
  if (!deaths_) goto error;

  if (PyArray_NDIM(births_) != 1 || PyArray_NDIM(deaths_) != 1) {
    PyErr_SetString(PyExc_ValueError, "births and deaths must be 1D array");
    goto error;
  }
  
  if (PyArray_SIZE(births_) != PyArray_SIZE(deaths_)) {
    PyErr_SetString(PyExc_ValueError, "births and deaths must be the same length");
    goto error;
  }

  for (unsigned int n = 0; n < PyArray_SIZE(births_); ++n) {
    pairs->emplace_back(*GETPTR1D<double>(births_, n), *GETPTR1D<double>(deaths_, n));
  }

  return true;

error:
  Py_XDECREF(births_);
  Py_XDECREF(deaths_);

  return false;
}


#endif // HOMCLOUD_HERA_COMMON_H
