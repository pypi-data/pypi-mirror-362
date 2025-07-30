#include <iostream>
#include <vector>
#include <cassert>
#include <random>
#include <unordered_set>

class ModpInvTable {
 public:
  int p_;
  std::vector<int> table_;

  explicit ModpInvTable(int p): p_(p), table_(p, -1) {
    table_[1] = 1;
    for (int k=2; k < p_; ++k)
      inv(k);
  }

  int inv(int a) {
    if (table_[a] < 0)
      table_[a] = p_ - inv(p_ % a) * (p_ / a) % p_;
    return table_[a];
  }

  int get(int k) const { return table_.at(k); }
  int operator[](int k) const { return table_.at(k); }
};
  
class CompressedSparseModpColumn {
 public:
  std::vector<int> indices_;
  std::vector<int> data_;
  int p_;
  const ModpInvTable& inv_;

  CompressedSparseModpColumn(int p, const ModpInvTable& inv):
      p_(p), inv_(inv)
  {
  }

  void ReduceStep(const CompressedSparseModpColumn& other) {
    assert(other.data_.back() == 1);
    
    std::vector<int> orig_data;
    std::vector<int> orig_indices;
    data_.swap(orig_data);
    indices_.swap(orig_indices);

    int lowvalue = orig_data.back();
    int i = 0, j = 0;
    while (i < (int)orig_indices.size() || j < (int)other.indices_.size()) {
      if (i == (int)orig_indices.size()) {
        Set(other.indices_[j], (p_ - lowvalue) * other.data_[j] % p_);
        ++j;
      } else if (j == (int)other.indices_.size()) {
        Set(orig_indices[i], orig_data[i]);
        ++i;
      } else if (orig_indices[i] == other.indices_[j]) {
        int d = (orig_data[i] + (p_ - lowvalue) * other.data_[j]) % p_;
        if (d != 0) {
          Set(orig_indices[i], d);
        }
        ++i; ++j;
      } else if (orig_indices[i] < other.indices_[j]) {
        Set(orig_indices[i], orig_data[i]);
        ++i;
      } else {
        Set(other.indices_[j], (p_ - lowvalue) * other.data_[j] % p_);
        ++j;
      }
    }
  }

  void Adjust() {
    int inv = inv_[data_.back()];
    if (inv == 1)
      return;
    for (int k = 0; k < (int)data_.size(); ++k)
      data_[k] = (data_[k] * inv) % p_;
  }

  void Set(int index, int value) {
    if (value == 0)
      return;

    indices_.push_back(index);
    data_.push_back(value);
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

  void PrintFlat() const {
    std::cout << "{";
    int n = 0;
    for (size_t k = 0; k < indices_.size(); ++k) {
      for (;n < indices_[k]; ++n) {
        std::cout << 0;
      }
      ++n;
      std::cout << data_[k];
    }
    std::cout << "}" << std::endl;
  }

};

class Matrix {
 public:
  using Column = CompressedSparseModpColumn;
  using CellID = int;

  int p_;
  int maxdim_;
  ModpInvTable table_;
  std::vector<std::vector<Column>> columns_;
  std::vector<int> num_cells_;
  std::vector<int> cellid_to_localindex_;
  std::vector<int> dim_of_cells_;
  std::vector<std::vector<CellID>> localindex_to_cellid_;
  

  Matrix(int p, int dimension, const std::vector<int>& num_cells):
      p_(p),
      maxdim_(dimension),
      table_(p),
      columns_(dimension + 1),
      num_cells_(num_cells),
      localindex_to_cellid_(dimension + 1)
  {}

  // All cells must be added by the increasing order of birth times
  CellID AddCell(int dimension) {
    int new_cellid = cellid_to_localindex_.size();
    int new_localindex = localindex_to_cellid_.at(dimension).size();
    cellid_to_localindex_.push_back(new_localindex);
    localindex_to_cellid_.at(dimension).push_back(new_cellid);
    dim_of_cells_.push_back(dimension);
    columns_.at(dimension).emplace_back(p_, table_);
    return new_cellid;
  }

  int NumCells(int dimension) {
    return (dimension < 0) ? 0 : num_cells_.at(dimension);
  }

  int NumAllDimCells() {
    return cellid_to_localindex_.size();
  }

  // Preconditions:
  // * rows in the same col must be given by the increasing order
  // * col > row
  void AddBoundaryCoef(CellID col, CellID row, int value) {
    int d = dim_of_cells_.at(col);
    int col_localindex = cellid_to_localindex_.at(col);
    int row_localindex = cellid_to_localindex_.at(row);
    value = (p_ + value % p_) % p_;
    columns_.at(d).at(col_localindex).Set(row_localindex, value);
  }

  // Twist algortihm is used
  void Reduce(int d) {
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
        column.Adjust();
        int i = column.Low();
        L[i] = j;
        columns_[d - 1][i].Die();
      }
    }
  }

  void ReduceALL() {
    for (int d = maxdim_; d > 0; --d)
      Reduce(d);
  }

  std::vector<int> ColumnVector(int col) const {
    int dim_of_cell = dim_of_cells_[col];
    int localindex = cellid_to_localindex_[col];
    if (dim_of_cell == 0)
      return std::vector<int>();
    int num_rows = num_cells_[dim_of_cell - 1];

    return columns_[dim_of_cell][localindex].Vectorize(num_rows);
  }

  std::vector<std::vector<std::pair<int, int>>> BirthDeathPairs() {
    std::vector<std::vector<std::pair<int, int>>> pairs(maxdim_);
    std::vector<bool> killed(NumAllDimCells(), false);

    for (int d = maxdim_; d >= 0; --d) {
      for (int l = 0; l < (int)columns_[d].size(); ++l) {
        int cellid = localindex_to_cellid_[d][l];
        if (columns_[d][l].IsAlive()) {
          int cellid_birth = localindex_to_cellid_[d - 1][columns_[d][l].Low()];
          
          pairs[d - 1].emplace_back(cellid_birth, cellid);
          killed[cellid_birth] = true;
        } else if (!killed[cellid]) {
          pairs[d].emplace_back(cellid, -1);
        }
      }
    }
    return pairs;
  }

  template<typename PairEncoder>
  void Pairs(PairEncoder* encoder) {
    std::vector<bool> killed(NumAllDimCells(), false);

    for (int d = maxdim_; d >= 0; --d) {
      for (int l = 0; l < (int)columns_[d].size(); ++l) {
        int cellid = localindex_to_cellid_[d][l];
        if (columns_[d][l].IsAlive()) {
          int cellid_birth = localindex_to_cellid_[d - 1][columns_[d][l].Low()];

          encoder->AddPair(d - 1, cellid_birth, cellid);
          killed[cellid_birth] = true;
        } else if (!killed[cellid]) {
          encoder->AddEssentialPair(d, cellid);
        }
      }
    }
  }
};

#ifdef PYTHON
#include "homcloud_common.h"
#include "birth_death_pair_encoder.h"


struct ModpMatrix {
  PyObject_HEAD

  Matrix* matrix_;
};

namespace ModpMatrix_methods {

static void dealloc(ModpMatrix* self) {
  delete self->matrix_;
  self->matrix_ = nullptr;
  Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static int init(ModpMatrix* self, PyObject* args, PyObject* kwds) {
  int p;
  PyObject* num_cells;
  if (!PyArg_ParseTuple(args, "iO!", &p, &PyList_Type, &num_cells))
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
  self->matrix_ = new(std::nothrow) Matrix(p, dimension, num_cells_vector);
  if (!self->matrix_) {
    PyErr_SetString(PyExc_RuntimeError, "Memory allocation error");
    return -1;
  }

  return 0;
}

static PyObject* add_cell(ModpMatrix* self, PyObject* args) {
  int dimension;
  if (!PyArg_ParseTuple(args, "i", &dimension))
    return nullptr;
  return Py_BuildValue("i", self->matrix_->AddCell(dimension));
}

static PyObject* add_boundary_coef(ModpMatrix* self, PyObject* args) {
  int col, row, value;
  if (!PyArg_ParseTuple(args, "iii", &col, &row, &value))
    return nullptr;
  self->matrix_->AddBoundaryCoef(col, row, value);
  Py_RETURN_NONE;
}

static PyObject* reduce(ModpMatrix* self) {
  self->matrix_->ReduceALL();
  Py_RETURN_NONE;
}

static PyObject* birth_death_pairs(ModpMatrix* self) {
  ListOfTupleEncoder encoder;
  if (encoder.IsAllocationError()) return nullptr;

  self->matrix_->Pairs(&encoder);

  if (encoder.stopped_) return nullptr;
  
  return encoder.list_;
}

static PyMethodDef methods[] = {
  {"add_cell", (PyCFunction)add_cell, METH_VARARGS, "Add a cell"},
  {"add_boundary_coef", (PyCFunction)add_boundary_coef, METH_VARARGS,
   "Add boundary matrix information"},
  {"reduce", (PyCFunction)reduce, METH_NOARGS, "Reduce all columns"},
  {"birth_death_pairs", (PyCFunction)birth_death_pairs, METH_NOARGS,
   "Returns the list of (degree, birth, death) tuples"},
  {NULL}
};

} // ModpMatrix_methods

static PyTypeObject ModpMatrixType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.modp_reduction_ext.ModpMatrix", // tp_name
  sizeof(ModpMatrix), // tp_basicsize
  0, // tp_itemsize
  reinterpret_cast<destructor>(ModpMatrix_methods::dealloc), // tp_dealloc
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
  "Class for modp reduction",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  ModpMatrix_methods::methods,  // tp_methods 
  0, // tp_members
  0, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(ModpMatrix_methods::init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 

static PyModuleDef modp_reduction_ext_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.modp_reduction_ext",
  "The module for modp_reduction",
  -1,
};


PyMODINIT_FUNC
PyInit_modp_reduction_ext()
{
  if (PyType_Ready(&ModpMatrixType) < 0)
    return nullptr;

  PyObject* module = PyModule_Create(&modp_reduction_ext_Module);
  if (!module)
    return nullptr;

  Py_INCREF(&ModpMatrixType);
  PyModule_AddObject(module, "ModpMatrix", reinterpret_cast<PyObject*>(&ModpMatrixType));

  return module;
}

#endif

#ifdef DEBUG_MAIN

void test_modp_inv_table() {
  for (int p: std::vector<int>{ 2, 3, 5, 7, 11, 13}) {
    ModpInvTable table(p);
    std::cout << p << " {";
    for (int k = 0; k < p; ++k) {
      std::cout << table.get(k) << ", ";
    }
    std::cout << "}" << std::endl;
    std::cout << p << " {**, ";
    for (int k = 1; k < p; ++k) {
      std::cout << table[k] * k % p << ", ";
    }
    std::cout << "}" << std::endl;
  }
}

void test_modp_column() {
  std::mt19937 mt(49379052);
  std::uniform_int_distribution<> rand100(0, 99);
  
  for (int p: std::vector<int>{2, 3, 5, 7}) {
    std::uniform_int_distribution<> randp(1, p - 1);

    using Column = CompressedSparseModpColumn;
    ModpInvTable table(p);
    Column x(p, table), y(p, table);
    for (int k=0; k < 8; ++k) {
      if (rand100(mt) < 70)
        x.Set(k, randp(mt));
      if (rand100(mt) < 70)
        y.Set(k, randp(mt));
    }
    x.Set(8, randp(mt));
    y.Set(8, randp(mt));
    std::cout << p << std::endl;
    y.PrintFlat();
    y.Adjust();
    y.PrintFlat();
    x.PrintFlat();
    x.ReduceStep(y);
    x.PrintFlat();
  }
}

void test_modp_reduction_all_tetrahedron() {
  for (int p: std::vector<int>{2, 3, 5, 7}) {
    Matrix matrix(p, 3, std::vector<int>{4, 6, 4, 1});
    for (int d: std::vector<int>{0, 0, 0, 1, 1, 1, 2, 0, 1, 1, 1, 2, 2, 2, 3}) {
      matrix.AddCell(d);
    }
    matrix.AddBoundaryCoef(3, 0, 1);
    matrix.AddBoundaryCoef(3, 2, -1);
    matrix.AddBoundaryCoef(4, 1, 1);
    matrix.AddBoundaryCoef(4, 2, -1);
    matrix.AddBoundaryCoef(5, 0, 1);
    matrix.AddBoundaryCoef(5, 1, -1);
    matrix.AddBoundaryCoef(6, 3, -1);
    matrix.AddBoundaryCoef(6, 4, 1);
    matrix.AddBoundaryCoef(6, 5, 1);
    matrix.AddBoundaryCoef(8, 1, 1);
    matrix.AddBoundaryCoef(8, 7, -1);
    matrix.AddBoundaryCoef(9, 2, 1);
    matrix.AddBoundaryCoef(9, 7, -1);
    matrix.AddBoundaryCoef(10, 0, 1);
    matrix.AddBoundaryCoef(10, 7, -1);
    matrix.AddBoundaryCoef(11, 4, 1);
    matrix.AddBoundaryCoef(11, 8, -1);
    matrix.AddBoundaryCoef(11, 9, 1);
    matrix.AddBoundaryCoef(12, 5, 1);
    matrix.AddBoundaryCoef(12, 8, 1);
    matrix.AddBoundaryCoef(12, 10, -1);
    matrix.AddBoundaryCoef(13, 3, 1);
    matrix.AddBoundaryCoef(13, 9, 1);
    matrix.AddBoundaryCoef(13, 10, -1);
    matrix.AddBoundaryCoef(14, 6, -1);
    matrix.AddBoundaryCoef(14, 11, 1);
    matrix.AddBoundaryCoef(14, 12, 1);
    matrix.AddBoundaryCoef(14, 13, -1);

    matrix.ReduceALL();

    auto pairs = matrix.BirthDeathPairs();

    std::cout << "mod " << p << std::endl;
    for (int d = 0; d <= 2; ++d) {
      std::cout << "[" << d << "]" << std::endl;
      for (const auto& pair: pairs[d]) {
        std::cout << pair.first << " " << pair.second << std::endl;
      }
    }
  }
}

int main() {
  test_modp_inv_table();
  test_modp_column();
  test_modp_reduction_all_tetrahedron();
  return 0;
}
#endif
