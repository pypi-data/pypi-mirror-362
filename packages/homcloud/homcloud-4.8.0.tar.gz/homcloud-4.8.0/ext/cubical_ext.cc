#include <cstdint>
#include <cmath>
#include <vector>
#include <unordered_map>
#include <limits>
#include <iostream>
#include <bitset>
#include <sstream>
#include <algorithm>

#include "homcloud_common.h"
#include "homcloud_numpy.h"

#define HOMCLOUD_PHAT_EXT_MODULE
#include "phat_ext.h"

using CubeID = unsigned long long;

struct StringWriter {
  std::string* buf_;

  StringWriter(std::string* buf) {
    buf_ = buf;
  }

  template<typename T>
  void Write(T n) {
    buf_->append(reinterpret_cast<char*>(&n), sizeof(T));
  }
};

class CubeEncoder {
 public:
  CubeEncoder(int ndim, const npy_intp* shape):
      ndim_(ndim), shape_(shape, shape + ndim),
      required_bits_(ndim), bottom_bit_(ndim + 1)
  {
    bottom_bit_[0] = 0;
    
    for (int n = 0; n < ndim_; ++n) {
      npy_intp bits = RequiredBits1D(shape_[n]);
      required_bits_[n] = bits;
      bottom_bit_[n + 1] = bottom_bit_[n] + bits;
    }

    cubedim_mask_ = BuildCubeDimMask();
  }

  static npy_intp RequiredBits1D(npy_intp n) {
    for (npy_intp k = 0; k < 32; ++k)
      if ((1 << k) >= n)
        return k + 1;
    return -1;
  }

  CubeID BuildCubeDimMask() {
    CubeID mask = 0;
    for (int k = 0; k < ndim_; ++k)
      mask |= 1 << bottom_bit_[k];
    return mask;
  }

  int CubeDim(CubeID id) const {
#ifdef __GNUC__
    return __builtin_popcountll(id & cubedim_mask_);
#else
    int dim = 0;
    for (int n = 0; n < ndim_; ++n) {
      dim += (id & Mask(n)) & 1;
      id >>= required_bits_[n];
    }
    return dim;
#endif
  }

  CubeID Encode(const std::vector<npy_intp>& coords,
                const std::vector<npy_intp>& non_degenerate) const {
    CubeID id = 0;
    for (int n = ndim_ - 1; n >= 0; --n) {
      id = (id << required_bits_[n]) | (coords[n] << 1) | non_degenerate[n];
    }
    return id;
  }

  void Decode(CubeID id,
              std::vector<npy_intp>* coords,
              std::vector<npy_intp>* non_degenerate) const {
    for (int n = 0; n < ndim_; ++n) {
      CubeID slice = id & Mask(n);
      coords->at(n) = slice >> 1;
      non_degenerate->at(n) = slice & 1;
      id >>= required_bits_[n];
    }
  }

  CubeID Mask(int n) const {
    return ((1 << required_bits_[n]) - 1);
  }

  CubeID BuildFacet(CubeID partial, CubeID coface, CubeID mask, int n) const {
    return (coface & ~mask) | (partial << (bottom_bit_[n] + 1));
  }

  std::vector<CubeID> Facets(CubeID id) const {
    std::vector<CubeID> result;

    for (int n = 0; n < ndim_; ++n) {
      CubeID mask = Mask(n) << bottom_bit_[n];
      CubeID slice = (id & mask) >> bottom_bit_[n];
      if (slice & 1) {
        result.push_back(BuildFacet(((slice >> 1) + 1) % shape_[n], id, mask, n));
        result.push_back(BuildFacet(slice >> 1, id, mask, n));
      }
    }
    return result;
  }

  size_t TotalBits() const {
    return bottom_bit_[ndim_];
  }

  // For Python
  static bool ValidSequence(PyObject* obj, int expected_size) {
    return PySequence_Check(obj) && (PySequence_Size(obj) == expected_size);
  }

  PyObject* encode_cube(PyObject* args) const {
    PyObject* coords;
    PyObject* non_degenerate;

    if (!PyArg_ParseTuple(args, "OO", &coords, &non_degenerate))
      return nullptr;

    if (!ValidSequence(coords, ndim_) ||
        !ValidSequence(non_degenerate, ndim_)) {
      PyErr_SetString(PyExc_RuntimeError,
                      "coords or non_degenerate is not a valid sequence");
      return nullptr;
    }

    std::vector<npy_intp> v_coords(ndim_);
    std::vector<npy_intp> v_non_degenerate(ndim_);
    for (int n = 0; n < ndim_; ++n) {
      v_coords[n] = PyLong_AsLong(PySequence_GetItem(coords, n));
      v_non_degenerate[n] = PyLong_AsLong(PySequence_GetItem(non_degenerate, n));
    }
    return PyLong_FromLong(Encode(v_coords, v_non_degenerate));
  }

  PyObject* decode_cube(PyObject* args) const {
    CubeID id;
    if (!PyArg_ParseTuple(args, "K", &id))
      return nullptr;

    std::vector<npy_intp> v_coords(ndim_);
    std::vector<npy_intp> v_non_degenerate(ndim_);

    Decode(id, &v_coords, &v_non_degenerate);

    PyObject* coords = nullptr;
    PyObject* non_degenerate = nullptr;

    coords = PyList_New(ndim_);
    non_degenerate = PyList_New(ndim_);
    if (!coords || !non_degenerate)
      goto error;

    for (int n = 0; n < ndim_; ++n) {
      PyObject* coord = PyLong_FromLong(v_coords[n]);
      if (!coord) goto error;
      PyList_SET_ITEM(coords, n, coord);
    
      PyObject* ndeg = PyLong_FromLong(v_non_degenerate[n]);
      if (!ndeg) goto error;
      PyList_SET_ITEM(non_degenerate, n, ndeg);
    }

    return Py_BuildValue("(OO)", coords, non_degenerate);

 error:
    Py_XDECREF(coords);
    Py_XDECREF(non_degenerate);
    return nullptr;
  }

  PyObject* cube_dim(PyObject* args) {
    CubeID id;
    if (!PyArg_ParseTuple(args, "K", &id))
      return nullptr;

    return PyLong_FromLong(CubeDim(id));
  }

  int ndim_;
  std::vector<npy_intp> shape_;
  std::vector<npy_intp> required_bits_;
  std::vector<npy_intp> bottom_bit_;
  CubeID cubedim_mask_;
}; // struct CubeEncoder

struct CubeEncoderClass {
  PyObject_HEAD
  CubeEncoder* encoder_;
};

struct CubicalFiltrationExt {
  PyObject_HEAD
  PyArrayObject* array_;
  PyObject* periodicity_;
  int ndim_;
  npy_intp* shape_;
  CubeEncoder* encoder_;
  std::vector<double>* cache_value_at_;
  std::vector<CubeID>* sorted_cubes_;
  bool save_boundary_map_;

  void SetUp(PyArrayObject* array, PyObject* periodicity, bool save_boundary_map) {
    ndim_ = PyArray_NDIM(array);
    shape_ = PyArray_DIMS(array);
    array_ = array;
    periodicity_ = periodicity;
    Py_INCREF(array_);
    Py_INCREF(periodicity_);

    encoder_ = new CubeEncoder(ndim_, shape_);
    
    cache_value_at_ = new std::vector<double>(1 << encoder_->bottom_bit_[ndim_],
                                             std::numeric_limits<double>::quiet_NaN());

    PrepareSortedCubes();

    save_boundary_map_ = save_boundary_map;
  }

  void TearDown() {
    Py_XDECREF(array_);
    Py_XDECREF(periodicity_);
    delete encoder_; encoder_ = nullptr;
    delete cache_value_at_; cache_value_at_ = nullptr;
    delete sorted_cubes_; sorted_cubes_ = nullptr;
  }

  int CubeDim(CubeID id) {
    return encoder_->CubeDim(id);
  }

  std::vector<int> BoundarySigns(CubeID id) {
    int dim = CubeDim(id);
    std::vector<int> result(2 * dim);
    for (int i = 0; i < 2 * dim; ++i) 
      result[i] = (i % 4 == 0 || i % 4 == 3) ? 1 : -1;
    return result;
  }

  double ValueAt(CubeID id) {
    double cache_value = cache_value_at_->at(id);
    if (!std::isnan(cache_value))
      return cache_value;
    
    double value;
    if (CubeDim(id) == 0) {
      std::vector<npy_intp> coords(ndim_);
      std::vector<npy_intp> non_degenerate(ndim_);
      encoder_->Decode(id, &coords, &non_degenerate);
      value = *reinterpret_cast<double*>(PyArray_GetPtr(array_, coords.data()));
    } else {
      auto facets = Facets(id);
      value = std::max(ValueAt(facets[0]), ValueAt(facets[1]));
    }
    
    cache_value_at_->at(id) = value;

    return value;
  }

  std::vector<CubeID> Facets(CubeID id) {
    return encoder_->Facets(id);
  }

  bool ValidCoords(const std::vector<npy_intp>& coords,
                   const std::vector<npy_intp>& non_degenerate) const {
    for (int n = 0; n < ndim_; ++n) {
      if (PyObject_IsTrue(PySequence_GetItem(periodicity_, n)))
        continue;
      if (coords[n] + non_degenerate[n] >= shape_[n])
        return false;
    }
    return true;
  }

  void AllCubesIter(int n,
                    std::vector<npy_intp>* indexlist,
                    std::vector<npy_intp>* non_degenerate,
                    std::vector<CubeID>* result) {
    if (n == ndim_) {
      CubeID cubeid = encoder_->Encode(*indexlist, *non_degenerate);
      if (ValidCoords(*indexlist, *non_degenerate) && ValueAt(cubeid) != INFINITY) {
        result->push_back(cubeid);
      }
      return;
    }

    for (npy_intp k = 0; k < shape_[n]; ++k) {
      indexlist->at(n) = k;
      for (npy_intp nd=0; nd <= 1; ++nd) {
        non_degenerate->at(n) = nd;
        AllCubesIter(n + 1, indexlist, non_degenerate, result);
      }
    }
  }
                    
  std::vector<CubeID> AllCubes() {
    std::vector<CubeID> result;
    std::vector<npy_intp> indexlist(ndim_);
    std::vector<npy_intp> non_degenerate(ndim_);
    
    AllCubesIter(0, &indexlist, &non_degenerate, &result);
    return result;
  }

  bool CompareCube(CubeID x, CubeID y) {
    double x_value = ValueAt(x);
    double y_value = ValueAt(y);
    if (x_value != y_value)
      return x_value < y_value;
    else
      return CubeDim(x) < CubeDim(y);
  }

  void PrepareSortedCubes() {
    if (sorted_cubes_)
      return;

    sorted_cubes_ = new std::vector<CubeID>();
    *sorted_cubes_ = std::move(AllCubes());
    std::stable_sort(sorted_cubes_->begin(), sorted_cubes_->end(),
                     [this](CubeID x, CubeID y) { return CompareCube(x, y); });
  }

  std::vector<int64_t> Cube2Index() {
    std::vector<int64_t> cube2index(1 << encoder_->TotalBits());
    for (unsigned n = 0; n < sorted_cubes_->size(); ++n)
      cube2index[(*sorted_cubes_)[n]] = n;
    return cube2index;
  }

  std::string DiphaByteSequence() {
    std::string buf;
    StringWriter output(&buf);

    std::vector<int64_t> cube2index = Cube2Index();

    // Write headers
    output.Write<int64_t>(8067171840);
    output.Write<int64_t>(0);
    output.Write<int64_t>(0);
    output.Write<int64_t>(sorted_cubes_->size());
    output.Write<int64_t>(ndim_);
    
    // Write dimensions
    for (CubeID cube : *sorted_cubes_)
      output.Write<int64_t>(CubeDim(cube));

    // Write birth time
    for (unsigned i = 0; i < sorted_cubes_->size(); ++i)
      output.Write<double>(i);

    // Write Boundary map sizes
    int n = 0;
    for (CubeID cube : *sorted_cubes_) {
      output.Write<int64_t>(n);
      n += CubeDim(cube) * 2;
    }
    output.Write<int64_t>(n);

    // Write boundary map
    for (CubeID cube : *sorted_cubes_)
      for (CubeID facet : Facets(cube))
        output.Write<int64_t>(cube2index[facet]);

    return buf;
  }

  phat_ext::Matrix* BuildPhatMatrix() {
    phat_ext::Matrix* matrix = phat_ext::MatrixNew(
        sorted_cubes_->size(), save_boundary_map_ ? "cubical" : "none");
        
    if (!matrix) return nullptr;

    auto cube2index = Cube2Index();

    for (unsigned i = 0; i < sorted_cubes_->size(); ++i) {
      CubeID cube = sorted_cubes_->at(i);
      std::vector<CubeID> facets = Facets(cube);
      std::vector<phat::index> facet_ids(facets.size());
      std::transform(facets.begin(), facets.end(), facet_ids.begin(),
                     [&cube2index](CubeID id) { return cube2index[id]; });
      matrix->SetDimCol(i, CubeDim(cube), &facet_ids);
    }
    
    return matrix;
  }
}; // struct CubicalFiltrationExt


namespace CubicalFiltrationExt_methods {

static void dealloc(CubicalFiltrationExt* self) {
  self->TearDown();
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static int init(CubicalFiltrationExt* self, PyObject* args, PyObject* kwds) {
  PyArrayObject* array;
  PyObject* periodicity;
  int save_boundary_map;
  
  if (!PyArg_ParseTuple(args, "O!O!p", &PyArray_Type, &array,
                        &PyList_Type, &periodicity, &save_boundary_map))
    return -1;

  if (!ArrayIsDoubleType(array))
    return -1;

  self->SetUp(array, periodicity, save_boundary_map);

  return 0;
}

static PyObject* get_required_bits(PyObject* self_, void* closure) {
  CubicalFiltrationExt* self = reinterpret_cast<CubicalFiltrationExt*>(self_);
  PyObject* list = PyList_New(self->ndim_);

  if (!list)
    return nullptr;

  for (int n = 0; n < self->ndim_; ++n) {
    PyObject* bits = PyLong_FromLong(self->encoder_->required_bits_[n]);
    if (!bits)
      goto error;

    PyList_SET_ITEM(list, n, bits);
  }
  return list;

error:
  Py_XDECREF(list);
  return nullptr;
}

static PyObject* get_sorted_cubes(CubicalFiltrationExt* self, void* closure) {
  PyObject* list = PyList_New(self->sorted_cubes_->size());
  
  if (!list)
    return nullptr;

  for (unsigned n = 0; n < self->sorted_cubes_->size(); ++n) {
    PyObject* cube = PyLong_FromLong((*self->sorted_cubes_)[n]);
    if (!cube) goto error;
    PyList_SET_ITEM(list, n, cube);
  }

  return list;
error:
  Py_XDECREF(list);
  return nullptr;
}

static PyObject* encode_cube(CubicalFiltrationExt* self, PyObject* args) {
  return self->encoder_->encode_cube(args);
}

static PyObject* decode_cube(CubicalFiltrationExt* self, PyObject* args) {
  return self->encoder_->decode_cube(args);
}

static PyObject* cube_dim(CubicalFiltrationExt* self, PyObject* args) {
  return self->encoder_->cube_dim(args);
}

static PyObject* boundary(CubicalFiltrationExt* self, PyObject* args) {
  CubeID id;
  if (!PyArg_ParseTuple(args, "K", &id))
    return nullptr;

  int cube_dim = self->CubeDim(id);
    
  std::vector<CubeID> facets = self->Facets(id);
  std::vector<int> signs = self->BoundarySigns(id);
  PyObject* facets_list = PyList_New(cube_dim * 2);
  if (!facets_list)
    return nullptr;
  
  PyObject* signs_list = PyList_New(cube_dim * 2);
  if (!signs_list) {
    Py_XDECREF(facets_list);
    return nullptr;
  }

  for (int i = 0; i < 2 * cube_dim; ++i) {
    PyList_SET_ITEM(facets_list, i, PyLong_FromLong(facets[i]));
    PyList_SET_ITEM(signs_list, i, PyLong_FromLong(signs[i]));
  }

  return Py_BuildValue("(OO)", facets_list, signs_list);
}

static PyObject* value_at(CubicalFiltrationExt* self, PyObject* args) {
  CubeID id;
  if (!PyArg_ParseTuple(args, "K", &id))
    return nullptr;

  return PyFloat_FromDouble(self->ValueAt(id));
}

static PyObject* all_cubes(CubicalFiltrationExt* self) {
  PyObject* list = PyList_New(0);
  PyObject* cubeint = nullptr;

  auto all_cubes = self->AllCubes();
  for (CubeID cube : all_cubes) {
    cubeint = PyLong_FromLong(cube);
    if (!cubeint) goto error;
    if (PyList_Append(list, cubeint) < 0)
      goto error;
  }

  return list;
error:
  Py_XDECREF(list);
  Py_XDECREF(cubeint);
  return nullptr;
}

static PyObject* dipha_byte_sequence(CubicalFiltrationExt* self) {
  std::string buf = self->DiphaByteSequence();
  return PyBytes_FromStringAndSize(buf.c_str(), buf.size());
}

static PyObject* levels(CubicalFiltrationExt* self) {
  npy_intp dims[] = {static_cast<npy_intp>(self->sorted_cubes_->size())};
  PyObject* levels = PyArray_SimpleNew(1, dims, NPY_DOUBLE);
  if (!levels)
    return nullptr;

  for (unsigned i = 0; i < self->sorted_cubes_->size(); ++i)
    *GETPTR1D<double>((PyArrayObject*)levels, i) = self->ValueAt((*self->sorted_cubes_)[i]);
  return levels;
}

static PyObject* build_phat_matrix(CubicalFiltrationExt* self) {
  phat_ext::Matrix* matrix = self->BuildPhatMatrix();
  if (!matrix) {
    PyErr_SetString(PyExc_RuntimeError, "Build phat matrix error");
    return nullptr;
  }
    
  return reinterpret_cast<PyObject*>(matrix);
}

static PyMethodDef methods[] = {
  {"encode_cube", (PyCFunction)encode_cube, METH_VARARGS, "Encode cube id"},
  {"decode_cube", (PyCFunction)decode_cube, METH_VARARGS, "Decode cube id"},
  {"cube_dim", (PyCFunction)cube_dim, METH_VARARGS, "Dimension of the cube id"},
  {"boundary", (PyCFunction)boundary, METH_VARARGS, "Boundary map"},
  {"value_at", (PyCFunction)value_at, METH_VARARGS, "Level of the cube"},
  {"all_cubes", (PyCFunction)all_cubes, METH_NOARGS, "List of all cubes"},
  {"dipha_byte_sequence", (PyCFunction)dipha_byte_sequence, METH_NOARGS,
   "Byte sequence for dipha"},
  {"levels", (PyCFunction)levels, METH_NOARGS, "index to levels"},
  {"build_phat_matrix", (PyCFunction)build_phat_matrix, METH_NOARGS,
   "Return phat' matrix object"},
  {NULL}
};

static PyMemberDef members[] = {
  {"array", T_OBJECT, offsetof(CubicalFiltrationExt, array_), READONLY,
   "Numpy array object"},
  {"periodicity", T_OBJECT, offsetof(CubicalFiltrationExt, periodicity_),
   READONLY, "periodicity"},
  {NULL}
};

static PyGetSetDef getsetters[] = {
  {"required_bits", get_required_bits, nullptr,
   "Required bits for each coordinate"},
  {"sorted_cubes", (getter)get_sorted_cubes, nullptr, "Sorted cubes"},
  {NULL}
};

} // namespace CubicalFiltrationExt_methods

static PyTypeObject CubicalFiltrationExtType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.cubical_ext.CubicalFiltrationExt", // tp_name
  sizeof(CubicalFiltrationExt), // tp_basicsize
  0, // tp_itemsize
  (destructor)CubicalFiltrationExt_methods::dealloc, // tp_dealloc
  0, // tp_print
  0, // tp_getattr
  0, // tp_setattr
  0, // tp_reserved
  0, // tp_repr
  0, // tp_as_number
  0, // tp_as_sequence
  0, // tp_as_mapping
  0, // tp_hash 
  0, // tp_call
  0, // tp_str
  0, // tp_getattro
  0, // tp_setattro
  0, // tp_as_buffer
  Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE, // tp_flags 
  "Class for fast cubical filtration",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  CubicalFiltrationExt_methods::methods,  // tp_methods 
  CubicalFiltrationExt_methods::members, // tp_members
  CubicalFiltrationExt_methods::getsetters, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(CubicalFiltrationExt_methods::init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 

namespace CubeEncoderClass_methods {

static int init(CubeEncoderClass* self, PyObject* args, PyObject* kwds) {
  PyObject* shape;
  
  if (!PyArg_ParseTuple(args, "O", &shape))
    return -1;

  if (!PySequence_Check(shape))
    return -1;

  int ndim = PySequence_Size(shape);
  std::vector<npy_intp> vshape(ndim);
  for (int n = 0; n < ndim; ++n) {
    vshape[n] = PyLong_AsLong(PySequence_GetItem(shape, n));
    if (PyErr_Occurred())
      return -1;
  }

  self->encoder_ = new CubeEncoder(ndim, vshape.data());
  return 0;
}

static void dealloc(CubeEncoderClass* self) {
  delete self->encoder_;
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static PyObject* encode_cube(CubeEncoderClass* self, PyObject* args) {
  return self->encoder_->encode_cube(args);
}

static PyObject* decode_cube(CubeEncoderClass* self, PyObject* args) {
  return self->encoder_->decode_cube(args);
}

static PyObject* cube_dim(CubeEncoderClass* self, PyObject* args) {
  return self->encoder_->cube_dim(args);
}

static PyMethodDef methods[] = {
  {"encode_cube", (PyCFunction)encode_cube, METH_VARARGS, "Encode cube id"},
  {"decode_cube", (PyCFunction)decode_cube, METH_VARARGS, "Decode cube id"},
  {"cube_dim", (PyCFunction)cube_dim, METH_VARARGS, "Dimension of the cube id"},
  {NULL}
};
  
}; // namespace CubeEncoderClass

static PyTypeObject CubeEncoderClassType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.cubical_ext.CubeEncoder", // tp_name
  sizeof(CubeEncoderClass), // tp_basicsize
  0, // tp_itemsize
  (destructor)CubeEncoderClass_methods::dealloc, // tp_dealloc
  0, // tp_print
  0, // tp_getattr
  0, // tp_setattr
  0, // tp_reserved
  0, // tp_repr
  0, // tp_as_number
  0, // tp_as_sequence
  0, // tp_as_mapping
  0, // tp_hash 
  0, // tp_call
  0, // tp_str
  0, // tp_getattro
  0, // tp_setattro
  0, // tp_as_buffer
  Py_TPFLAGS_DEFAULT, // tp_flags 
  "Class for encode/decode cubes of homcloud.cubical_ext.CubicalFiltrationExt",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  CubeEncoderClass_methods::methods,  // tp_methods 
  0, // tp_members
  0, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(CubeEncoderClass_methods::init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 


static PyModuleDef cubical_ext_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.cubical_ext",
  "The module for fast cubical filtrations",
  -1,
  NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_cubical_ext()
{
  if (PyType_Ready(&CubicalFiltrationExtType) < 0)
    return nullptr;
  if (PyType_Ready(&CubeEncoderClassType) < 0)
    return nullptr;

  PyObject* module = PyModule_Create(&cubical_ext_Module);
  if (!module)
    return nullptr;

  Py_INCREF(&CubicalFiltrationExtType);
  PyModule_AddObject(module, "CubicalFiltrationExt",
                     cast_PyObj(&CubicalFiltrationExtType));

  Py_INCREF(&CubeEncoderClassType);
  PyModule_AddObject(module, "CubeEncoder",
                     cast_PyObj(&CubeEncoderClassType));
  
  import_array();
  phat_ext::import();

  return module;
}
