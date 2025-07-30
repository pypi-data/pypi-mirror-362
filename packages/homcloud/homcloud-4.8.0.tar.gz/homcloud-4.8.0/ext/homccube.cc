#pragma GCC diagnostic ignored "-Wmaybe-uninitialized"
#pragma GCC diagnostic ignored "-Wunused-function"

#include "homcloud_common.h"
#include "homcloud_numpy.h"

#include "homccube3/bitmap.hpp"
#include "homccube3/config.hpp"
#include "homccube3/cubemap.hpp"
#include "homccube3/io.hpp"
#include "homccube3/link_find.hpp"
#include "homccube3/pd.hpp"
#include "homccube3/reducer.hpp"
#include "homccube3/maxdim2/basic_types.hpp"
#include "homccube3/maxdim3/basic_types.hpp"

#include <memory>
#include <sstream>
#include <type_traits>

using homccube::maxdim2::Policy2D;
using homccube::maxdim2::PolicyPeriodic2D;
using homccube::maxdim3::Policy3D;
using homccube::maxdim3::PolicyPeriodic3D;

using homccube::Config;

static std::vector<int> ShapeFromArray(PyArrayObject* array) {
  npy_intp* shape = PyArray_DIMS(array);
  return std::vector<int>(shape, shape + PyArray_NDIM(array));
}
    
static bool IsValidShape(const std::vector<int>& shape) {
  if (shape.size() == 2) {
    if (homccube::maxdim2::valid_shape(shape)) {
      return true;
    } else {
      PyErr_SetString(PyExc_ValueError,
                      "Invalid shape: array must be smaller than 32765x65534");
      return false;
    }
  }
  if (shape.size() == 3) {
    if (homccube::maxdim3::valid_shape(shape)) {
      return true;
    } else {
      PyErr_SetString(PyExc_ValueError,
                      "Invalid shape: array must be smaller than 1021x1021x1021");
      return false;
    }
  }

  PyErr_SetString(PyExc_ValueError, "HomcCube supports only 2D and 3D bitmaps");
  return false;
}

unsigned long ParsePeriodicityList(PyObject* periodicity) {
  unsigned long ret = 0;
  for (int i = 0; i < PyList_Size(periodicity); ++i)
    ret |= (PyObject_IsTrue(PyList_GetItem(periodicity, i)) << i);
  return ret;
}

template<typename Bitmap>
void LoadLevels(PyArrayObject* array, Bitmap* bitmap) {
  npy_int32* data = reinterpret_cast<npy_int32*>(PyArray_DATA(array));
  size_t num_pixels = bitmap->shape_.num_pixels();
  bitmap->levels_.assign(num_pixels, 0);
  std::copy(data, data + num_pixels, bitmap->levels_.begin());
}

template<typename Policy>
struct Runner {
  template <int d> using Cube = typename Policy::template Cube<d>;
  using Bitmap = homccube::Bitmap<Policy>;
  using Periodicity = typename Policy::Periodicity;
  using PD = homccube::PD<Policy>;
  using LinkFind = homccube::LinkFind<Policy>;
  template<int dim>
  using Reducer = homccube::Reducer<dim, Policy>;
  template<int dim>
  using Survivors = std::shared_ptr<std::vector<Cube<dim>>>;

  static const auto INFINITE_LEVEL = Policy::INFINITE_LEVEL;
  
  static PyObject* Run2D(PyArrayObject* array, unsigned long periodicity,
                         const std::vector<int>&shape, Config config) {
    Bitmap bitmap(shape, Periodicity(periodicity));
    PD pd;
    LoadLevels(array, &bitmap);

    auto survivors0 = Compute0thPD(bitmap, &pd);
    auto survivors1 = ComputeKthPD<1>(bitmap, survivors0, config, &pd);

    for (Cube<2> s: *survivors1)
      pd.add_ess_pair(2, s.level_);

    return Pairs(pd);
  }

  static PyObject* Run3D(PyArrayObject* array, unsigned long periodicity,
                         const std::vector<int>&shape, Config config) {
    Bitmap bitmap(shape, Periodicity(periodicity));
    PD pd;
    LoadLevels(array, &bitmap);

    auto survivors0 = Compute0thPD(bitmap, &pd);
    auto survivors1 = ComputeKthPD<1>(bitmap, survivors0, config, &pd);
    survivors0 = nullptr;
    auto survivors2 = ComputeKthPD<2>(bitmap, survivors1, config, &pd);

    for (Cube<3> s: *survivors2)
      pd.add_ess_pair(3, s.level_);

    return Pairs(pd);
  }

  static Survivors<1> Compute0thPD(const Bitmap& bitmap, PD* pd) {
    LinkFind link_find(bitmap, pd);
    link_find.compute();
    return link_find.survivors_;
  }

  template<int dim> static 
  Survivors<dim + 1> ComputeKthPD(const Bitmap& bitmap,
                                  const Survivors<dim> survivors,
                                  Config config, PD* pd) {
    Reducer<dim> reducer(bitmap, *survivors, config, pd);
    reducer.compute();
    return reducer.upper_survivors();
  }

  static
  PyObject* Pairs(const PD& pd) {
    PyObject* pairs = PyList_New(0);
    if (!pairs) return nullptr;
    
    for (size_t i = 0; i < pd.size(); ++i) {
      PyObject* pair = BuildPair(pd.degrees_[i], pd.births_[i], pd.deaths_[i]);
      if (!pair) goto error;
      if (PyList_Append(pairs, pair) < 0) goto error;
      Py_CLEAR(pair);
    }

    return pairs;

 error:
    Py_XDECREF(pairs);
    return nullptr;
  }

  static
  PyObject* BuildPair(int degree, unsigned long birth, unsigned long death) {
    if (death == INFINITE_LEVEL) {
      return Py_BuildValue("ikO", degree, birth, Py_None);
    } else {
      return Py_BuildValue("ikk", degree, birth, death);
    }
  }
};


static PyObject* compute_pd(PyObject* self, PyObject* args) {
  PyObject* ary;
  PyObject* periodicity_list;
  int algorithm_threshold;
  
  PyArrayObject* array = nullptr;
  PyObject* ret = nullptr;

  if (!PyArg_ParseTuple(args, "OO!i", &ary, &PyList_Type, &periodicity_list,
                        &algorithm_threshold))
    return nullptr;

  array = reinterpret_cast<PyArrayObject*>(PyArray_FROM_OTF(ary, NPY_INT32, NPY_ARRAY_C_CONTIGUOUS));
  if (!array) return nullptr;

  int ndim = PyArray_NDIM(array);

  if (PyList_Size(periodicity_list) != ndim) {
    PyErr_SetString(PyExc_ValueError, "Periodicity list length mismatch");
    return nullptr;
  }

  std::vector<int> shape = ShapeFromArray(array);
  
  if (!IsValidShape(shape))
    return nullptr;

  Config config = { algorithm_threshold, false };

  unsigned long periodicity = ParsePeriodicityList(periodicity_list);

  if (ndim == 2 && periodicity == 0) {
    ret = Runner<Policy2D>::Run2D(array, 0, shape, config);
  } else if (ndim == 2 && periodicity != 0) {
    ret = Runner<PolicyPeriodic2D>::Run2D(array, periodicity, shape, config);
  } else if (ndim == 3 && periodicity == 0) {
    ret = Runner<Policy3D>::Run3D(array, 0, shape, config);
  } else if (ndim == 3 && periodicity != 0) {
    ret = Runner<PolicyPeriodic3D>::Run3D(array, periodicity, shape, config);
  }

  Py_DECREF(array);
  return ret;
}

static PyMethodDef homccube_Methods[] = {
  {"compute_pd", (PyCFunction)compute_pd, METH_VARARGS,
   "Compute a persistence diagram from bitmap"},
  {NULL, NULL, 0, NULL},
};

static PyModuleDef homccube_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.homccube",
  "The module for homccube",
  -1,
  homccube_Methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_homccube()
{
  PyObject* module = PyModule_Create(&homccube_Module);
  if (!module)
    return nullptr;

  import_array();

  return module;
}
