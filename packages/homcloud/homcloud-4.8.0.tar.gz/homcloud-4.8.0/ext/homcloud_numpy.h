// -*- mode: c++ -*-
#ifndef HOMCLOUD_NUMPY_H
#define HOMCLOUD_NUMPY_H

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

#ifndef SIZEOF_PY_HASH_T
typedef Py_ssize_t Py_hash_t;
#endif

template<class T> PyObject* cast_PyObj(T* obj) {
  return reinterpret_cast<PyObject*>(obj);
}

static bool ArrayIsDoubleType(PyArrayObject* points) {
  if (PyArray_TYPE(points) == NPY_DOUBLE)
    return true;

  PyErr_SetString(PyExc_TypeError, "Array must be double");
  return false;
}

template<typename T>
T* GETPTR1D(PyArrayObject* ary, npy_intp i) {
  return reinterpret_cast<T*>(PyArray_GETPTR1(ary, i));
}

template<typename T>
T* GETPTR2D(PyArrayObject* ary, npy_intp i, npy_intp j) {
  return reinterpret_cast<T*>(PyArray_GETPTR2(ary, i, j));
}


#endif // HOMCLOUD_NUMPY_H
