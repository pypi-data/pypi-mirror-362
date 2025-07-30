#include "Python.h"
#include "structmember.h"

#include <vector>
#include <cstdlib>
#include <new>
#include <iostream>

class CompressedSparseColumn {
 public:
  std::vector<int> indices_;
  std::vector<int> data_;

  CompressedSparseColumn(int num_rows) {}

  void ReduceStep(const CompressedSparseColumn& other) {
    std::vector<int> orig_data;
    std::vector<int> orig_indices;
    data_.swap(orig_data);
    indices_.swap(orig_indices);
    
    int lowdata = orig_data.back();

    int i = 0, j = 0;
    while (i < (int)orig_indices.size() || j < (int)other.indices_.size()) {
      if (i == (int)orig_indices.size()) {
        Set(other.indices_[j], -lowdata * other.data_[j]);
        ++j;
      } else if (j == (int)other.indices_.size()) {
        Set(orig_indices[i], orig_data[i]);
        ++i;
      } else if (orig_indices[i] == other.indices_[j]) {
        int d = orig_data[i] - lowdata * other.data_[j];
        if (d != 0) {
          Set(orig_indices[i], d);
        }
        ++i; ++j;
      } else if (orig_indices[i] < other.indices_[j]) {
        Set(orig_indices[i], orig_data[i]);
        ++i;
      } else {
        Set(other.indices_[j], -lowdata * other.data_[j]);
        ++j;
      }
    }
  }

  void Set(int index, int value) {
    if (value == 0)
      return;

    indices_.push_back(index);
    data_.push_back(value);
  }

  void AdjustSign() {
    if (data_.back() == -1) {
      for (int k = 0; k < (int)data_.size(); ++k) {
        data_[k] *= -1;
      }
    }
  }
  int Low() { return indices_.back(); }
  void Die() { data_.clear(); indices_.clear(); }
  bool IsDead() { return indices_.empty(); }
  bool IsAlive() { return !indices_.empty(); }
  int LowValue() { return data_.back(); }
  void Print() const {
    std::cout << "CSC{";
    for (size_t k = 0; k < indices_.size(); ++k) {
      std::cout << "(" << indices_[k] << "," << data_[k] << ") ";
    }
    std::cout << "}" << std::endl;
  }

  std::vector<int> Vectorize(int n) const {
    std::vector<int> v(n, 0);
    for (size_t k = 0; k < indices_.size(); ++k)
      v[indices_[k]] = data_[k];
    return v;
  }
};


class Matrix {
 public:
  using Column = CompressedSparseColumn;
  using CellID = int;

  int maxdim_;
  std::vector<std::vector<Column>> columns_;
  std::vector<int> num_cells_;
  std::vector<int> cellid_to_localindex_;
  std::vector<int> dim_of_cells_;
  std::vector<std::vector<CellID>> localindex_to_cellid_;


  Matrix(int dimension, const std::vector<int>& num_cells):
      maxdim_(dimension),
      columns_(dimension + 1),
      num_cells_(num_cells),
      localindex_to_cellid_(dimension + 1)
  {}

  Matrix(const std::vector<int>& num_cells):
      columns_(num_cells.size()),
      num_cells_(num_cells)
  {}

  // All cells must be added by the increasing order of birth times
  CellID AddCell(int dimension) {
    int new_cellid = cellid_to_localindex_.size();
    int new_localindex = localindex_to_cellid_.at(dimension).size();
    cellid_to_localindex_.push_back(new_localindex);
    localindex_to_cellid_.at(dimension).push_back(new_cellid);
    dim_of_cells_.push_back(dimension);
    columns_.at(dimension).emplace_back(NumCells(dimension - 1));
    return new_cellid;
  }

  int NumCells(int dimension) {
    return (dimension < 0) ? 0 : num_cells_.at(dimension);
  }
  // Preconditions:
  // * rows in the same col must be given by the increasing order
  // * col > row
  void AddBoundaryCoef(CellID col, CellID row, int value) {
    int d = dim_of_cells_.at(col);
    int col_localindex = cellid_to_localindex_.at(col);
    int row_localindex = cellid_to_localindex_.at(row);
    columns_.at(d).at(col_localindex).Set(row_localindex, value);
  }
  
  // Twist algortihm is used
  std::pair<int, int> Reduce(int d) {
    std::vector<int> L(num_cells_[d - 1], -1);
    
    for (int j=0; j < num_cells_[d]; ++j) {
      Column& column = columns_[d][j];
      if (column.IsDead())
        continue;
      while (true) {
        if (column.IsDead())
          break;
        int l = L[column.Low()];
        if (l < 0)
          break;
        column.ReduceStep(columns_[d][l]);
      }
      if (column.IsAlive()) {
        if (std::abs(column.LowValue()) != 1)
          return std::make_pair(std::abs(column.LowValue()),
                                localindex_to_cellid_[d][j]);
        column.AdjustSign();
        int i = column.Low();
        L[i] = j;
        columns_[d - 1][i].Die();
      }
    }

    return std::make_pair(0, 0);
  }

  std::pair<int, int> ReduceALL() {
    for (int d = maxdim_; d > 0; --d) {
      auto c = Reduce(d);
      if (c.first != 0)
        return c;
    }
    return std::make_pair(0, 0);
  }

  std::vector<int> ColumnVector(int col) const {
    int dim_of_cell = dim_of_cells_[col];
    int localindex = cellid_to_localindex_[col];
    if (dim_of_cell == 0)
      return std::vector<int>();
    int num_rows = num_cells_[dim_of_cell - 1];

    return columns_[dim_of_cell][localindex].Vectorize(num_rows);
  }
};

struct Checker {
  PyObject_HEAD

  Matrix* matrix_;
};

namespace Checker_methods {

static void dealloc(Checker* self) {
  delete self->matrix_;
  self->matrix_ = nullptr;
  Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static int init(Checker* self, PyObject* args, PyObject* kwds) {
  PyObject* num_cells;
  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &num_cells))
    return -1;

  int dimension = PyList_Size(num_cells) - 1;
  std::vector<int> num_cells_vector(dimension + 1);
  for (int i = 0; i <= dimension; ++i) {
    long n = PyLong_AsLong(PyList_GetItem(num_cells, i));
    if (PyErr_Occurred()) {
      return -1;
    }
    num_cells_vector[i] = n;
  }

  self->matrix_ = new(std::nothrow) Matrix(dimension, num_cells_vector);
  if (!self->matrix_) {
    PyErr_SetString(PyExc_RuntimeError, "Memory allocation error");
    return -1;
  }

  return 0;
}

static PyObject* check(Checker* self) {
  std::pair<int, int> result = self->matrix_->ReduceALL();
  return Py_BuildValue("(ii)", result.first, result.second);
}

static PyObject* add_cell(Checker* self, PyObject* args) {
  int dimension;
  if (!PyArg_ParseTuple(args, "i", &dimension))
    return nullptr;
  return Py_BuildValue("i", self->matrix_->AddCell(dimension));
}

static PyObject* add_boundary_coef(Checker* self, PyObject* args) {
  int col, row, value;
  if (!PyArg_ParseTuple(args, "iii", &col, &row, &value))
    return nullptr;
  self->matrix_->AddBoundaryCoef(col, row, value);
  Py_RETURN_NONE;
}

static PyObject* column(Checker* self, PyObject* args) {
  int col;
  if (!PyArg_ParseTuple(args, "i", &col))
    return nullptr;
  std::vector<int> v = self->matrix_->ColumnVector(col);
  PyObject* list = PyList_New(v.size());
  if (!list)
    return nullptr;

  for (size_t k = 0; k < v.size(); ++k) {
    PyObject* value = PyLong_FromLong(v[k]);
    if (!value) goto error;
    PyList_SET_ITEM(list, k, value);
  }
  return list;

error:
  Py_XDECREF(list);
  return nullptr;
}

static PyMethodDef methods[] = {
  {"check", (PyCFunction)check, METH_NOARGS, "Check the coefficient problem"},
  {"add_cell", (PyCFunction)add_cell, METH_VARARGS, "Add a cell"},
  {"add_boundary_coef", (PyCFunction)add_boundary_coef, METH_VARARGS,
   "Add boundary matrix information"},
  {"column", (PyCFunction)column, METH_VARARGS, "For debug"},
  {NULL}
};

} // namespace Checker_methods

static PyTypeObject CheckerType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.int_reduction_ext.Checker", // tp_name
  sizeof(Checker), // tp_basicsize
  0, // tp_itemsize
  reinterpret_cast<destructor>(Checker_methods::dealloc), // tp_dealloc
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
  "Class for int reduction checker",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Checker_methods::methods,  // tp_methods 
  0, // tp_members
  0, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(Checker_methods::init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 

static PyModuleDef int_reduction_ext_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.int_reduction_ext",
  "The module for int_reduction",
  -1,
};


PyMODINIT_FUNC
PyInit_int_reduction_ext()
{
  if (PyType_Ready(&CheckerType) < 0)
    return nullptr;

  PyObject* module = PyModule_Create(&int_reduction_ext_Module);
  if (!module)
    return nullptr;

  Py_INCREF(&CheckerType);
  PyModule_AddObject(module, "Checker", reinterpret_cast<PyObject*>(&CheckerType));

  return module;
}
