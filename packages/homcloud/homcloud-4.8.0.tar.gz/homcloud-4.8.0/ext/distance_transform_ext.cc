// -*- mode: c++ -*-
#pragma GCC diagnostic ignored "-Wunused-function"
#include "homcloud_common.h"
#include "homcloud_numpy.h"
#include <vector>
#include <deque>
#include <functional>
#include <iostream>

template<typename T, typename NpyType>
T GetAry(PyArrayObject* ary, const std::vector<npy_intp>& index) {
  npy_intp* idx = const_cast<npy_intp*>(index.data());
  return *reinterpret_cast<NpyType*>(PyArray_GetPtr(ary, idx));
}

template<typename T, typename NpyType>
void SetAry(PyArrayObject* ary, const std::vector<npy_intp>& index, T value) {
  npy_intp* idx = const_cast<npy_intp*>(index.data());
  *reinterpret_cast<NpyType*>(PyArray_GetPtr(ary, idx)) = value;
}

static bool GETBOOL(PyArrayObject* ary, const std::vector<npy_intp>& at) {
  return GetAry<bool, npy_bool>(ary, at);
}

static void SETBOOL(PyArrayObject* ary, const std::vector<npy_intp>& at, bool value) {
  SetAry<bool, npy_bool>(ary, at, value);
}

static void SETDBL(PyArrayObject* ary, const std::vector<npy_intp>& at, double value) {
  SetAry<double, npy_double>(ary, at, value);
}

static bool IsShapeAndTypeOK(PyArrayObject* bitmap, PyArrayObject* mask,
                             PyArrayObject* distances) {
  if (PyArray_TYPE(bitmap) != NPY_BOOL) {
    PyErr_SetString(PyExc_TypeError, "Bitmap type mast be bool");
    return false;
  }
  if (PyArray_TYPE(mask) != NPY_BOOL) {
    PyErr_SetString(PyExc_TypeError, "mask type mast be bool");
    return false;
  }
  if (PyArray_TYPE(distances) != NPY_DOUBLE) {
    PyErr_SetString(PyExc_TypeError, "distance type mast be double");
    return false;
  }
  if (!PyArray_SAMESHAPE(bitmap, mask) || !PyArray_SAMESHAPE(bitmap, distances)) {
    PyErr_SetString(PyExc_TypeError, "bitmap, mask, and distances must have the same shape");
    return false;
  }
  return true;
}

using IndexFunc = std::function<void (std::vector<npy_intp>&)>;

static void ScanIndexIter(int nd, npy_intp* shape, IndexFunc f, int k,
                          std::vector<npy_intp>* index) {
  if (k == nd) {
    f(*index);
  } else {
    for (int i = 0; i < shape[k]; ++i) {
      index->at(k) = i;
      ScanIndexIter(nd, shape, f, k + 1, index);
    }
  }
}

static void ScanIndex(int nd, npy_intp* shape, IndexFunc f) {
  std::vector<npy_intp> index(nd);
  ScanIndexIter(nd, shape, f, 0, &index);
}

static void ScanNeighbour(int nd, npy_intp* shape, const std::vector<npy_intp>& center,
                          IndexFunc f) {
  std::vector<npy_intp> index = center;
  for (int k = 0; k < nd; ++k) {
    for (int s = -1; s <= 1; s += 2) {
      if (index[k] + s < 0 || index[k] + s >= shape[k])
        continue;
      index[k] += s;
      f(index);
      index[k] -= s;
    }
  }
}

static PyObject*
positive_distance_transform_manhattan_with_mask(PyObject* self, PyObject* args) {
  PyArrayObject* bitmap;
  PyArrayObject* mask;
  PyArrayObject* distances;
  
  if (!PyArg_ParseTuple(args, "O!O!O!", &PyArray_Type, &bitmap, &PyArray_Type, &mask,
                        &PyArray_Type, &distances))
    return nullptr;

  if (!IsShapeAndTypeOK(bitmap, mask, distances))
    return nullptr;

  int ndim = PyArray_NDIM(bitmap);
  npy_intp* shape = PyArray_DIMS(bitmap);
  PyArrayObject *visited =
      reinterpret_cast<PyArrayObject*>(PyArray_ZEROS(ndim, shape, NPY_BOOL, 0));
  if (!visited)
    return nullptr;

  std::deque<std::pair<std::vector<npy_intp>, double>> deque;

  ScanIndex(ndim, shape, [=,&deque](const std::vector<npy_intp>& index) {
      if (GETBOOL(mask, index)) {
        SETDBL(distances, index, INFINITY);
        SETBOOL(visited, index, true);
      } else if (!GETBOOL(bitmap, index)) {
        SETDBL(distances, index, INFINITY);
      } else {
        deque.push_back(std::make_pair(index, 0));
        SETBOOL(visited, index, true);
      }
    });

  while (!deque.empty()) {
    std::vector<npy_intp> current;
    double dist;
    std::tie(current, dist) = deque.front();
    deque.pop_front();
    ScanNeighbour(ndim, shape, current, [=,&deque](const std::vector<npy_intp>& next) {
        if (!GETBOOL(visited, next)) {
          SETBOOL(visited, next, true);
          SETDBL(distances, next, dist + 1);
          deque.push_back(std::make_pair(next, dist + 1));
        }
      });
  }

  Py_XDECREF(visited);
  Py_RETURN_NONE;
}

static PyMethodDef distance_transform_ext_Methods[] = {
  {"positive_distance_transform_manhattan_with_mask",
   positive_distance_transform_manhattan_with_mask, METH_VARARGS,
   "Distance transform by manhattan metric with a mask"},
  {NULL, NULL, 0, NULL}
};

static PyModuleDef distance_transform_ext_Moudle = {
  PyModuleDef_HEAD_INIT,
  "homcloud.distance_transform_ext",
  "The module for distance transformation with a mask",
  -1,
  distance_transform_ext_Methods,
};

PyMODINIT_FUNC
PyInit_distance_transform_ext()
{
  PyObject* module = PyModule_Create(&distance_transform_ext_Moudle);
  if (!module)
    return NULL;
  
  import_array();
  return module;
}

