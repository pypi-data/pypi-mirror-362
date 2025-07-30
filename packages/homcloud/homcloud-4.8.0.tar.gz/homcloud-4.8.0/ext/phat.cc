#include <iostream>
#include <msgpack.hpp>

#include "homcloud_common.h"
#include "homcloud_numpy.h"
#include "phat_ext.h"
#include "birth_death_pair_encoder.h"

using phat_ext::Matrix;

namespace Matrix_methods {

static void dealloc(Matrix* self) {
  self->TearDown();
  Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static int init(Matrix* self, PyObject* args, PyObject* kwds) {
  int num_cols;
  char* dstyle;

  if (!PyArg_ParseTuple(args, "is", &num_cols, &dstyle))
    return -1;

  self->SetUp(num_cols, dstyle);

  return 0;
}

static PyObject* set_dim_col(Matrix* self, PyObject* args) {
  int idx, dim;
  PyObject* col;
  if (!PyArg_ParseTuple(args, "iiO!", &idx, &dim, &PyList_Type, &col))
    return nullptr;

  Py_ssize_t size = PyList_Size(col);
  phat::column column(size);
  for (int n = 0; n < size; ++n)
    column[n] = PyLong_AsLong(PyList_GetItem(col, n));

  self->SetDimCol(idx, dim, &column);
  Py_RETURN_NONE;
}

static PyObject* reduce_twist(Matrix* self) {
  Py_BEGIN_ALLOW_THREADS
  self->ReduceTwist();
  Py_END_ALLOW_THREADS
  Py_RETURN_NONE;
}

static PyObject* reduce_chunk(Matrix* self) {
#ifdef HOMCLOUD_OPENMP
  Py_BEGIN_ALLOW_THREADS
  self->ReduceChunk();
  Py_END_ALLOW_THREADS
  Py_RETURN_NONE;
#else
  PyErr_SetString(PyExc_NotImplementedError,
                  "the paralle chunk algorithm is not available");
  return nullptr;
#endif
}


static PyObject* reduce(Matrix* self, PyObject* args) {
  char* algorithm;

  if (!PyArg_ParseTuple(args, "z", &algorithm))
    return nullptr;

  if (algorithm == nullptr || std::string(algorithm) == "phat-twist") {
    return reduce_twist(self);
  } else if (std::string(algorithm) == "phat-chunk-parallel") {
    return reduce_chunk(self);
  } else {
    return PyErr_Format(PyExc_NotImplementedError, "Unknown algoithm: %s", algorithm);
  }
}

static PyObject* boundary_map_byte_sequence(Matrix* self) {
  if (!self->boundary_map_buf_)
    Py_RETURN_NONE;
  return PyBytes_FromStringAndSize(self->boundary_map_buf_->data(),
                                   self->boundary_map_buf_->size());
}

static PyObject* birth_death_pairs(Matrix* self) {
  ListOfTupleEncoder encoder;
  if (encoder.IsAllocationError()) return nullptr;

  self->Pairs(&encoder);

  if (encoder.stopped_) return nullptr;
  
  return encoder.list_;
}

static PyMethodDef methods[] = {
  {"set_dim_col", (PyCFunction)set_dim_col, METH_VARARGS,
   "Set dimension and column (boundary) of the cell"},
  {"reduce_twist", (PyCFunction)reduce_twist, METH_NOARGS, "Reduction the matrix"},
  {"reduce_chunk", (PyCFunction)reduce_chunk, METH_NOARGS, "Reduction the matrix"},
  {"reduce", (PyCFunction)reduce, METH_VARARGS, "Reduce the matrix"},
  {"boundary_map_byte_sequence", (PyCFunction)boundary_map_byte_sequence, METH_NOARGS,
   "msgpack's byte sequence for boundary map"},
  {"birth_death_pairs", (PyCFunction)birth_death_pairs, METH_NOARGS,
   "Returns the list of (degree, birth, death) tuples"},
  {NULL}
};

}; // namespace Matrix_methods

static PyTypeObject MatrixType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.phat_ext.Matrix", // tp_name
  sizeof(Matrix), // tp_basicsize
  0, // tp_itemsize
  reinterpret_cast<destructor>(Matrix_methods::dealloc), // tp_dealloc
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
  "Class for phat's matrix",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Matrix_methods::methods,  // tp_methods 
  0, // tp_members
  0, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(Matrix_methods::init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 


static PyModuleDef phat_ext_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.phat_ext",
  "The module for phat",
  -1,
  NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_phat_ext()
{
  if (PyType_Ready(&MatrixType) < 0)
    return nullptr;
  
  PyObject* module = PyModule_Create(&phat_ext_Module);
  if (!module)
    return nullptr;

  Py_INCREF(&MatrixType);
  PyModule_AddObject(module, "Matrix", reinterpret_cast<PyObject*>(&MatrixType));

#ifdef HOMCLOUD_OPENMP
  PyModule_AddObject(module, "compile_with_openmp", PyBool_FromLong(1));
#else
  PyModule_AddObject(module, "compile_with_openmp", PyBool_FromLong(0));
#endif
  static void *phat_ext_API[] = {
    reinterpret_cast<void*>(&MatrixType),
  };
  PyObject* api_object = PyCapsule_New(phat_ext_API, "homcloud.phat_ext._C_API", NULL);
  if (api_object)
    PyModule_AddObject(module, "_C_API", api_object);

  import_array();
  
  return module;
}
