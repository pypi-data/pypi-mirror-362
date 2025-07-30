// -*- mode: c++ -*-
#pragma GCC diagnostic ignored "-Wunused-function"
#include "homcloud_common.h"

#include <iostream>
#include <unordered_map>
#include <memory>

#include <msgpack.hpp>

using CellID = long;

struct EdgeTriple {
  CellID edge_id, begin, end;
};

class GraphLoader;

struct BaseParser {
  BaseParser(GraphLoader* loader): loader_(loader) {}

  virtual bool visit_positive_integer(uint64_t v) { return false; }
  virtual bool visit_str(const char* v, uint32_t size) { return false; }
  virtual bool start_array(uint32_t num_elements) { return false; }
  virtual bool start_array_item() { return false; }
  virtual bool end_array_item() { return false; }
  virtual bool end_array() { return false; }
  virtual bool start_map_value() { return false; }

  GraphLoader* loader_;
};


class GraphLoader {
 public:
  GraphLoader(CellID);
  bool load(const char* bytes, long len);

  void enter_parse_map() {
    stack_.push_back(map_parser_.get());
  }

  void enter_parse_cell(long current_cell) {
    current_cell_ = current_cell;
    stack_.push_back(cell_parser_.get());
  }

  void enter_parse_boundary(int dim) {
    if (dim == 1)
      stack_.push_back(dim1boundary_parser_.get());
    else
      stack_.push_back(skip_array_parser_.get());
  }

  void enter_parse_sign() {
    stack_.push_back(skip_array_parser_.get());
  }

  void leave() {
    stack_.pop_back();
  }

  BaseParser* current_parser() {
    return stack_.back();
  }

  std::unique_ptr<BaseParser>
  toplevel_parser_, map_parser_, cell_parser_, dim1boundary_parser_, skip_array_parser_;
  
  CellID birth_;
  std::vector<BaseParser*> stack_;
  long current_cell_;
  std::vector<EdgeTriple> edges_;
  bool finished_;
};

struct ToplevelParser: public BaseParser {
  ToplevelParser(GraphLoader* loader): BaseParser(loader), is_map_(false) {}

  bool visit_str(const char* v, uint32_t size) {
    is_map_ = std::string(v, size) == "map";
    return true;
  }

  bool start_map_value() {
    if (is_map_)
      loader_->enter_parse_map();
    return true;
  }

  // bool visit_positive_integer(uint64_t v) { return true; }
  // bool start_array(uint32_t num_elements) { return true; }
  // bool start_array_item() { return true; }
  // bool end_array_item() { return true; }
  // bool end_array() { return true; }
  
  bool is_map_;
};

struct MapParser: public BaseParser {
  MapParser(GraphLoader* loader): BaseParser(loader) {}

  bool start_array(uint32_t num_elements) {
    k_ = 0;
    return true;
  }

  bool start_array_item() {
    if (k_ > loader_->birth_) {
      loader_->finished_ = true;
      return false;
    }
    loader_->enter_parse_cell(k_);
    return true;
  }

  bool end_array_item() {
    ++k_;
    return true;
  }

  bool end_array() {
    loader_->leave();
    return true;
  }

  long k_;
};

struct CellParser: public BaseParser {
  CellParser(GraphLoader* loader): BaseParser(loader) {}

  bool start_array(uint32_t num_elements) {
    count_ = 0;
    return true;
  }

  bool start_array_item() {
    switch (count_) {
      case 0:
        return true;
      case 1:
        loader_->enter_parse_boundary(dim_);
        return true;
      case 2:
        loader_->enter_parse_sign();
        return true;
      default:
        return false;
    }
  }

  bool end_array_item() {
    ++count_;
    return true;
  }

  bool end_array() {
    loader_->leave();
    return true;
  }

  bool visit_positive_integer(uint64_t v) {
    dim_ = v;
    return true;
  }

  int count_;
  int dim_;
};

struct Dim1BoundaryParser: public BaseParser {
  Dim1BoundaryParser(GraphLoader* loader): BaseParser(loader) {}

  bool start_array(uint32_t num_elements) {
    if (num_elements != 2)
      return false;
    data_.clear();
    return true;
  }

  bool start_array_item() { return true; }
  bool end_array_item() { return true; }
    
  bool end_array() {
    loader_->edges_.push_back(EdgeTriple{loader_->current_cell_, data_[0], data_[1]});
    loader_->leave();
    return true;
  }

  bool visit_positive_integer(uint64_t v) {
    data_.push_back(v);
    return true;
  }
  
  std::vector<CellID> data_;
};

struct SkipArrayParser: public BaseParser {
  SkipArrayParser(GraphLoader* loader): BaseParser(loader) {}

  bool start_array(uint32_t) { return true; }
  bool start_array_item() { return true; }
  bool end_array_item() { return true; }
  
  bool end_array() {
    loader_->leave();
    return true;
  }

  bool visit_positive_integer(uint64_t v) { return true; }
};

struct Visitor: public msgpack::null_visitor {
  Visitor(GraphLoader* loader): loader_(loader) {}

  bool visit_positive_integer(uint64_t v) {
    return loader_->current_parser()->visit_positive_integer(v);
  }
  bool visit_str(const char* v, uint32_t size) {
    return loader_->current_parser()->visit_str(v, size);
  }
  bool start_array(uint32_t num_elements) {
    return loader_->current_parser()->start_array(num_elements);
  }
  bool start_array_item() {
    return loader_->current_parser()->start_array_item();
  }
  bool end_array_item() {
    return loader_->current_parser()->end_array_item();
  }
  bool end_array() {
    return loader_->current_parser()->end_array();
  }
  bool start_map_value() {
    return loader_->current_parser()->start_map_value();
  }

  GraphLoader* loader_;
};

GraphLoader::GraphLoader(CellID birth):
    toplevel_parser_(new ToplevelParser(this)),
    map_parser_(new MapParser(this)),
    cell_parser_(new CellParser(this)),
    dim1boundary_parser_(new Dim1BoundaryParser(this)),
    skip_array_parser_(new SkipArrayParser(this)),
    birth_(birth),
    finished_(false) {
  stack_.push_back(toplevel_parser_.get());
}

bool GraphLoader::load(const char* bytes, long len) {
  std::size_t off = 0;
  Visitor visitor(this);
  return msgpack::parse(bytes, len, off, visitor);
}

struct Graph {
  struct Edge { CellID from, to; CellID id; };

  Graph(CellID birth): birth_(birth) {
  }
  
  bool load(const char* bytes, long len) {
    GraphLoader loader(birth_);
    loader.load(bytes, len);

    if (!loader.finished_) {
      PyErr_SetString(PyExc_ValueError, "boundary_map unpack/value error");
      return false;
    }
      
    for (const auto& edge: loader.edges_) {
      if (edge.edge_id == birth_) {
        begin_ = edge.begin;
        end_ = edge.end;
      } else {
        add_edge(edge.begin, edge.end, edge.edge_id);
        add_edge(edge.end, edge.begin, edge.edge_id);
      }
    }
    return true;
  }

  using Visited = std::unordered_map<CellID, Edge>;
  PyObject* search_shortest_loop() {
    std::deque<Edge> q;
    Visited visited;
    
    q.push_back(Edge{end_, begin_, birth_});
    
    for (;;) {
      if (q.empty())
        Py_RETURN_NONE;

      Edge e = q.front(); q.pop_front();
      if (visited.count(e.to))
        continue;
      
      visited.emplace(e.to, e);
      if (e.to == end_)
        return path(visited);
      
      for (const auto next: g_[e.to])
        q.push_back(next);
    }
  };

  void add_edge(CellID from, CellID to, CellID edge_id) {
    if (g_.count(from) == 0)
      g_.emplace(from, 0); // Initialize empty std::vector
    g_[from].push_back(Edge{from, to, edge_id});
  }

  PyObject* path(const Visited& visited) {
    CellID v = end_;
    PyObject* list = PyList_New(0);
    if (!list) return nullptr;
    
    for (;;) {
      Edge edge = visited.at(v);
      PyObject* py_edge = PyLong_FromLong(edge.id);
      if (!py_edge) goto error;
      if (PyList_Append(list, py_edge)) {
        Py_XDECREF(py_edge);
        goto error;
      }
      Py_XDECREF(py_edge);
      v = edge.from;
      if (v == end_)
        return list;
    }

 error:
    Py_XDECREF(list);
    return nullptr;
  }

  std::unordered_map<CellID, std::vector<Edge>> g_;
  CellID birth_;
  CellID begin_, end_;
};

static PyObject* search(PyObject* self, PyObject* args) {
  char* bytes;
  Py_ssize_t len_bytes;
  long birth;
  if (!PyArg_ParseTuple(args, "y#l", &bytes, &len_bytes, &birth))
    return nullptr;

  Graph graph(birth);
  if (!graph.load(bytes, len_bytes)) return nullptr;
  return graph.search_shortest_loop();
}

static PyMethodDef optimal_one_cycle_ext_Methods[] = {
  {"search", search, METH_VARARGS,
   "Computes optimal 1-cycle from boundary map chunk bytes"},
  {NULL, NULL, 0, NULL}
};

static PyModuleDef optimal_one_cycle_ext_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.optimal_one_cycle_ext",
  "The module for optimal 1-cycle from boundary map chunk bytes",
  -1,
  optimal_one_cycle_ext_Methods,
};

PyMODINIT_FUNC
PyInit_optimal_one_cycle_ext()
{
  PyObject* module = PyModule_Create(&optimal_one_cycle_ext_Module);
  if (!module)
    return NULL;
  
  return module;
}
