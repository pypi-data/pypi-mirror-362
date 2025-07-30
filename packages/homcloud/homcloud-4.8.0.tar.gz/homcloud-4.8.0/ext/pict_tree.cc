#include "homcloud_common.h"
#include "homcloud_numpy.h"

#include <iostream>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <tuple>
#include <cmath>
#include <limits>

using mindex_t = std::vector<npy_intp>;

struct Node {
  npy_intp id_;
  npy_intp order_;
  std::vector<Node*> children_;
  Node* parent_;
  double value_;
  Node* root_;
  double death_time_;
  Node* death_node_;
  bool is_boundary_;

  Node* root() {
    if (parent_)
      return root_ = root_->root();
    else 
      return this;
  }

  void InitializeAsInfNode() {
    id_ = -1;
    order_ = -2;
    death_node_ = root_ = parent_ = nullptr;
    value_ = std::numeric_limits<double>::infinity();
    death_time_ = -std::numeric_limits<double>::infinity();
    is_boundary_ = false;
  }

  void Initialize(npy_intp id, double value, bool is_boundary, Node* infnode) {
    id_ = id;
    order_ = -1;
    death_node_ = nullptr;
    value_ = value;
    death_time_ = -std::numeric_limits<double>::infinity();
    is_boundary_ = is_boundary;
    if (is_boundary)
      parent_ = root_ = infnode;
    else
      parent_ = root_ = nullptr;
  }

  void SetParent(Node* parent, double level, Node* death_node) {
    parent_ = root_ = parent;
    death_time_ = level;
    death_node_ = death_node;
    parent_->children_.push_back(this);
  }

  // Return true if the node does not appear on PD.
  bool IsTrivial() const {
    return (value_ == death_time_) || is_boundary_;
  }

  // Return true if the pixel of the node is on boundary.
  bool IsBoundary() const {
    return is_boundary_;
  }

  // Return true if the node conrresponds the point at infinity
  bool InfNode() const {
    return order_ < 0;
  }
}; // struct Node

struct MergeTree {
  PyObject_HEAD
  int is_superlevel_;
  int is_lower_;
  
  int ndim_;
  npy_intp size_;
  std::vector<npy_intp>* shape_;
  std::vector<Node>* nodes_;
  std::vector<npy_intp>* ordered_;
  Node infnode_;

  std::vector<npy_intp> index2mindex(npy_intp index) const {
    mindex_t result(ndim_);
    for (int i = 0; i < ndim_; ++i) {
      result[i] = index % shape_->at(i);
      index = index / shape_->at(i);
    }
    return result;
  }

  npy_intp mindex2index(const mindex_t& mindex) const {
    npy_intp index = 0;
    for (int i = ndim_ - 1; i >= 0; --i)
      index = index * shape_->at(i) + mindex[i];
    return index;
  }

  void PrintIndex(npy_intp index) {
    mindex_t mindex = this->index2mindex(index);
    for (npy_intp m : mindex) {
      std::cout << m << " ";
    }
    std::cout << std::endl;
  }

  bool IsOnBoundary(const mindex_t& mindex) const {
    for (int k=0; k < ndim_; ++k) {
      if (mindex[k] == 0 || mindex[k] == shape_->at(k) - 1)
        return true;
    }
    return false;
  }

  PyObject* Index2PyTuple(const npy_intp index) const {
    mindex_t mindex = index2mindex(index);
    PyObject* tuple = PyTuple_New(ndim_);
    PyObject* kth_index = NULL;

    if (!tuple) goto error;

    for (int k = 0; k < ndim_; ++k) {
      kth_index = PyLong_FromLong(mindex[k]);
      if (!kth_index) goto error;
      PyTuple_SetItem(tuple, k, kth_index);
    }
    return tuple;
 error:
    Py_XDECREF(tuple);
    Py_XDECREF(kth_index);
    return nullptr;
  }

  const Node* NthNodeFromPyArg(PyObject* args) const {
    int n;
    if (!PyArg_ParseTuple(args, "i", &n))
      return NULL;
    else
      return &nodes_->at(n);
  }
}; // struct MergeTree

static void MergeTree_dealloc(MergeTree* self) {
  delete self->shape_;
  self->shape_ = nullptr;
  delete self->nodes_;
  self->nodes_ = nullptr;
  delete self->ordered_;
  self->ordered_ = nullptr;
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static int MergeTree_init(MergeTree* self,
                          PyObject* args,
                          PyObject* kwds)
{
  PyArrayObject *bitmap;
  if (!PyArg_ParseTuple(args, "O!pp", &PyArray_Type, &bitmap,
                        &self->is_superlevel_, &self->is_lower_)) 
    return -1;

  if (!ArrayIsDoubleType(bitmap))
    return -1;

  self->ndim_ = PyArray_NDIM(bitmap);
  self->size_ = PyArray_SIZE(bitmap);
  self->shape_ = new std::vector<npy_intp>(self->ndim_);
  npy_intp* dims = PyArray_DIMS(bitmap);
  std::copy(dims, dims + self->ndim_, self->shape_->begin());
  self->nodes_ = new std::vector<Node>(self->size_);
  self->infnode_.InitializeAsInfNode();

  double sign = self->is_superlevel_ ? -1 : 1;

  for (npy_intp i = 0; i < self->size_; ++i) {
    mindex_t mindex = self->index2mindex(i);
    double value = *reinterpret_cast<double*>(PyArray_GetPtr(bitmap, mindex.data()));
    Node* node = &self->nodes_->at(i);
    node->Initialize(i, sign * value, !self->is_lower_  && self->IsOnBoundary(mindex),
                     &self->infnode_);
  }

  self->ordered_ = new std::vector<npy_intp>(self->size_);
  for (npy_intp i = 0; i < self->size_; ++i)
    self->ordered_->at(i) = i;

  std::sort(self->ordered_->begin(), self->ordered_->end(), [&self](npy_intp x, npy_intp y) {
      if (self->is_lower_) {
        return self->nodes_->at(x).value_ < self->nodes_->at(y).value_;
      } else {
        return self->nodes_->at(x).value_ > self->nodes_->at(y).value_;
      }
    });

  for (npy_intp i = 0; i < self->size_; ++i)
    self->nodes_->at(self->ordered_->at(i)).order_ = i;

  return 0;
}

static std::vector<npy_intp> AdjNodeLower(npy_intp n, MergeTree* self) {
  std::vector<npy_intp> result;
  mindex_t at = self->index2mindex(n);

  for (int k = 0; k < self->ndim_; ++k) {
    if (at[k] - 1 >= 0) {
      --at[k]; result.push_back(self->mindex2index(at)); ++at[k];
    }
    if (at[k] + 1 < self->shape_->at(k)) {
      ++at[k]; result.push_back(self->mindex2index(at)); --at[k];
    }
  }
  return result;
}

static void AdjNodeUpperIter(MergeTree* self, npy_intp n, int k,
                             mindex_t* mindex, std::vector<npy_intp>* result) {
  if (k == self->ndim_) {
    npy_intp m = self->mindex2index(*mindex);
    if (m != n)
      result->push_back(m);
  } else {
    if (mindex->at(k) > 0) {
      mindex->at(k)--;
      AdjNodeUpperIter(self, n, k + 1, mindex, result);
      mindex->at(k)++;
    }
    AdjNodeUpperIter(self, n, k + 1, mindex, result);
    if (mindex->at(k) + 1 < self->shape_->at(k)) {
      mindex->at(k)++;
      AdjNodeUpperIter(self, n, k + 1, mindex, result);
      mindex->at(k)--;
    }
  }
}

static std::vector<npy_intp> AdjNodeUpper(npy_intp n, MergeTree* self) {
  std::vector<npy_intp> result;
  mindex_t mindex = self->index2mindex(n);
  AdjNodeUpperIter(self, n, 0, &mindex, &result);
  return result;
}

static std::vector<npy_intp> AdjNode(npy_intp n, MergeTree* self) {
  if (self->is_lower_) {
    return AdjNodeLower(n, self);
  } else {
    return AdjNodeUpper(n, self);
  }
}

static std::pair<Node*, Node*> OrderNodes(Node* node1, Node* node2) {
  if (node1->order_ < node2->order_)
    return std::make_pair(node1, node2);
  else
    return std::make_pair(node2, node1);
}

static PyObject* MergeTree_compute(MergeTree* self) {
  for (auto n : *(self->ordered_)) {
    Node* node = &self->nodes_->at(n);
    for (auto adj : AdjNode(n, self)) {
      Node* adjnode = &self->nodes_->at(adj);
      if (node->order_ <= adjnode->order_)
        continue;
      Node* root1 = node->root();
      Node* root2 = adjnode->root();

      if (root1 == root2)
        continue;
      Node *parentroot, *childroot;
      std::tie(parentroot, childroot) = OrderNodes(root1, root2);
      childroot->SetParent(parentroot, node->value_, node);
    }
  }

  if (self->is_superlevel_)
    for (auto& node : *self->nodes_) {
      node.value_ *= -1;
      node.death_time_ *= -1;
    }
      
  Py_RETURN_NONE;
}

static PyObject* MergeTree_degree(MergeTree* self) {
  return PyLong_FromLong(self->is_lower_ ? 0 : self->ndim_ - 1);
}

static PyObject *MergeTree_num_nodes(MergeTree* self) {
  return PyLong_FromLong(self->size_);
}

static PyObject *MergeTree_node_id(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  return PyUnicode_FromFormat("%d", node->order_);
}

static PyObject *MergeTree_node_is_trivial(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  return PyBool_FromLong(node->IsTrivial());
}

static PyObject *MergeTree_node_is_on_boundary(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  return PyBool_FromLong(node->IsBoundary());
}

static PyObject *MergeTree_node_birth_time(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  return PyFloat_FromDouble(self->is_lower_ ? node->value_ : node->death_time_);
}

static PyObject *MergeTree_node_death_time(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  if (self->is_lower_) {
    if (node->parent_) {
      return PyFloat_FromDouble(node->death_time_);
    } else {
      Py_RETURN_NONE;
    }
  } else {
    return PyFloat_FromDouble(node->value_);
  }
}

static PyObject* parent_id(const Node* node) {
  if (node->parent_)
    return PyLong_FromLong(node->parent_->id_);
  else
    Py_RETURN_NONE;
}

static PyObject* get_id(const Node* node, bool is_parent_id) {
  if (!node) return nullptr;
  if (is_parent_id)
    return parent_id(node);
  else
    return PyLong_FromLong(node->id_);
}

static PyObject* MergeTree_node_birth_id(MergeTree* self, PyObject* args) {
  return get_id(self->NthNodeFromPyArg(args), !self->is_lower_);
}

static PyObject* MergeTree_node_death_id(MergeTree* self, PyObject* args) {
  return get_id(self->NthNodeFromPyArg(args), self->is_lower_);
}

static int VolumeIter(MergeTree* self, const Node* node, PyObject* volume) {
  PyObject* pixel = self->Index2PyTuple(node->id_);
  if (!pixel) return -1;
  if (PyList_Append(volume, pixel) < 0) return -1;
  Py_XDECREF(pixel);

  for (const Node* child: node->children_)
    if (VolumeIter(self, child, volume) < 0) return -1;
  return 0;
}

static PyObject *MergeTree_node_volume(MergeTree* self, PyObject* args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  PyObject* volume = PyList_New(0);
  if (!volume) return NULL;
  if (VolumeIter(self, node, volume) < 0) {
    Py_XDECREF(volume);
    return NULL;
  }
  return volume;
}

static PyObject *MergeTree_node_birth_pixel(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  return self->Index2PyTuple(self->is_lower_ ? node->id_ : node->death_node_->id_);
}

static PyObject *MergeTree_node_death_pixel(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  if (self->is_lower_) {
    if (node->death_node_) {
      return self->Index2PyTuple(node->death_node_->id_);
    } else {
      Py_RETURN_NONE;
    }
  } else {
    return self->Index2PyTuple(node->id_);
  }
}

static PyObject *MergeTree_node_parent(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  if (self->is_lower_) {
    if (node->parent_)
      return PyUnicode_FromFormat("%d", node->parent_->order_);
    else
      Py_RETURN_NONE;
  } else {
    if (node->parent_->InfNode())
      Py_RETURN_NONE;
    else
      return PyUnicode_FromFormat("%d", node->parent_->order_);
  }
}

static PyObject* MergeTree_node_is_essential(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;
  return PyBool_FromLong(node->parent_ == NULL);
}

static PyObject *MergeTree_node_children(MergeTree* self, PyObject *args) {
  const Node* node = self->NthNodeFromPyArg(args);
  if (!node) return NULL;

  PyObject* list = PyList_New(0);
  if (!list) return NULL;

  PyObject* child_id = NULL;

  for (int i = 0; i < (int)node->children_.size(); ++i) {
    const Node* child = node->children_[i];
    if (child->IsBoundary())
      continue;
    child_id = PyUnicode_FromFormat("%d", child->order_);
    if (!child_id) goto error;

    if (PyList_Append(list, child_id) < 0)
      goto error;
    Py_DECREF(child_id);
  }
  return list;
error:
  Py_XDECREF(list);
  Py_XDECREF(child_id);
  return NULL;
}

static PyMethodDef MergeTree_methods[] = {
  {"compute", (PyCFunction)MergeTree_compute, METH_NOARGS,
   "Compute trees"},
  {"degree", (PyCFunction)MergeTree_degree, METH_NOARGS,
   "Degree of PH"},
  {"num_nodes", (PyCFunction)MergeTree_num_nodes, METH_NOARGS,
   "Number of nodes"},
  {"node_id", (PyCFunction)MergeTree_node_id, METH_VARARGS,
   "Return the id of the n-th node"},
  {"node_is_trivial", (PyCFunction)MergeTree_node_is_trivial, METH_VARARGS,
   "Return true if the n-th node is trivial"},
  {"node_is_on_boundary", (PyCFunction)MergeTree_node_is_on_boundary, METH_VARARGS,
   "Return true if the n-th node is on boundary"},
  {"node_birth_time", (PyCFunction)MergeTree_node_birth_time, METH_VARARGS,
   "Return birth time of n-th node"},
  {"node_death_time", (PyCFunction)MergeTree_node_death_time, METH_VARARGS,
   "Return death time of n-th node"},
  {"node_birth_index", (PyCFunction)MergeTree_node_birth_id, METH_VARARGS,
   "Return birth time of n-th node by index"},
  {"node_death_index", (PyCFunction)MergeTree_node_death_id, METH_VARARGS,
   "Return death time of n-th node by index"},
  {"node_birth_pixel", (PyCFunction)MergeTree_node_birth_pixel, METH_VARARGS,
   "Return birth pixel of n-th node"},
  {"node_death_pixel", (PyCFunction)MergeTree_node_death_pixel, METH_VARARGS,
   "Return death pixel of n-th node"},
  {"node_volume", (PyCFunction)MergeTree_node_volume, METH_VARARGS,
   "Return pxiels in the volume of n-th node"},
  {"node_parent", (PyCFunction)MergeTree_node_parent, METH_VARARGS,
   "Return parent id of n-th node"},
  {"node_children", (PyCFunction)MergeTree_node_children, METH_VARARGS,
   "Return children ids of n-th node"},
  {"node_is_essential", (PyCFunction)MergeTree_node_is_essential, METH_VARARGS,
   "Return true if n-th node is essential"},
  {NULL}
};

static PyTypeObject MergeTreeType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.pict_tree.MergeTree", // tp_name
  sizeof(MergeTree), // tp_basicsize
  0, // tp_itemsize
  (destructor)MergeTree_dealloc, // tp_dealloc
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
  "MergeTree",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  MergeTree_methods,  // tp_methods 
  0, // tp_members
  0, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(MergeTree_init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 

static PyModuleDef pict_tree_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.pict_tree",
  "The module for fast pict.tree",
  -1,
  NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_pict_tree()
{
  if (PyType_Ready(&MergeTreeType) < 0)
    return NULL;
  
  PyObject* module = PyModule_Create(&pict_tree_Module);
  if (!module)
    return NULL;

  Py_INCREF(&MergeTreeType);
  PyModule_AddObject(module, "MergeTree", cast_PyObj(&MergeTreeType));

  import_array();

  return module;
}
