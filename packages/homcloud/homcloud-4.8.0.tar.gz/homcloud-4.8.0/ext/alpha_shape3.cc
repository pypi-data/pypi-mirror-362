#include "homcloud_common.h"
#include "homcloud_cgal.h"
#include "homcloud_numpy.h"
#include "alpha_shape_common.h"

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Regular_triangulation_3.h>
#include <CGAL/Alpha_shape_3.h>
#include <CGAL/Triangulation_vertex_base_with_info_3.h>
#include <CGAL/Alpha_shape_cell_base_3.h>
#include <CGAL/Alpha_shape_vertex_base_3.h>

#include <fstream>

struct VertexInfo {
  int vertex_index;
  int group_name;
};

typedef CGAL::Exact_predicates_inexact_constructions_kernel Kernel;
typedef CGAL::Regular_triangulation_vertex_base_3<Kernel>        Rvb;
typedef CGAL::Triangulation_vertex_base_with_info_3<VertexInfo, Kernel, Rvb> Vinfo;
typedef CGAL::Alpha_shape_vertex_base_3<Kernel,Vinfo>              Vb;
typedef CGAL::Regular_triangulation_cell_base_3<Kernel>          Rcb;
typedef CGAL::Alpha_shape_cell_base_3<Kernel,Rcb>                Cb;
typedef CGAL::Triangulation_data_structure_3<Vb,Cb>         Tds;
typedef CGAL::Regular_triangulation_3<Kernel,Tds>                Triangulation;
typedef CGAL::Alpha_shape_3<Triangulation>                CGAL_AlphaShape3;
typedef std::pair<CGAL_AlphaShape3::Weighted_point, VertexInfo> PointWithInfo;


typedef struct {
  PyObject_HEAD
  CGAL_AlphaShape3* alpha_shape_;
} AlphaShape3;

typedef struct {
  PyObject_HEAD
  AlphaShape3* alpha_;
  CGAL_AlphaShape3::Vertex_handle handle_;
  int vertex_index_;
  int group_name_;
  double birth_radius_;
} Vertex;

typedef struct {
  PyObject_HEAD
  AlphaShape3* alpha_;
  CGAL_AlphaShape3::Cell_handle handle_;
  double birth_radius_;
} Cell;

typedef struct {
  PyObject_HEAD
  AlphaShape3* alpha_;
  CGAL_AlphaShape3::Vertex_handle v1, v2;
  double birth_radius_;
} Edge;

typedef struct {
  PyObject_HEAD
  AlphaShape3* alpha_;
  CGAL_AlphaShape3::Cell_handle cell_;
  int v_;
  double birth_radius_;
} Facet;

struct AlphaShape3_Types {
  typedef CGAL_AlphaShape3 CGAL_ALphaShape;
  typedef AlphaShape3 AlphaShape;
  typedef ::Vertex Vertex;
  typedef ::Edge Edge;
  typedef ::Facet Facet;
  typedef ::Cell Cell;
};

static void AlphaShape3_dealloc(AlphaShape3* self) {
  delete self->alpha_shape_;
  self->alpha_shape_ = NULL;
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static int Vertex_traverse(Vertex* vertex, visitproc visit, void* arg) {
  Py_VISIT(vertex->alpha_);
  return 0;
}

static int Vertex_clear(Vertex* vertex) {
  Py_CLEAR(vertex->alpha_);
  return 0;
}

static void Vertex_dealloc(Vertex* self) {
  PyObject_GC_UnTrack(self);
  Vertex_clear(self);
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static int Cell_traverse(Cell* cell, visitproc visit, void* arg) {
  Py_VISIT(cell->alpha_);
  return 0;
}
static int Cell_clear(Cell* cell) {
  Py_CLEAR(cell->alpha_);
  return 0;
}

static void Cell_dealloc(Cell* self) {
  PyObject_GC_UnTrack(self);
  Cell_clear(self);
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static int Edge_traverse(Edge* edge, visitproc visit, void* arg) {
  Py_VISIT(edge->alpha_);
  return 0;
}

static int Edge_clear(Edge* edge) {
  Py_CLEAR(edge->alpha_);
  return 0;
}

static void Edge_dealloc(Edge* self) {
  PyObject_GC_UnTrack(self);
  Edge_clear(self);
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static int Facet_traverse(Facet* facet, visitproc visit, void* arg) {
  Py_VISIT(facet->alpha_);
  return 0;
}

static int Facet_clear(Facet* facet) {
  Py_CLEAR(facet->alpha_);
  return 0;
}

static void Facet_dealloc(Facet* self) {
  PyObject_GC_UnTrack(self);
  Facet_clear(self);
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}


static Vertex* Vertex_New(AlphaShape3* alpha,
                          CGAL_AlphaShape3::Vertex_handle handle);
static Cell* Cell_New(AlphaShape3* alpha,
                      CGAL_AlphaShape3::Cell_handle handle);
static Edge* Edge_New(AlphaShape3* alpha,
                      CGAL_AlphaShape3::Finite_edges_iterator edge);
static Facet* Facet_New(AlphaShape3* alpha,
                        CGAL_AlphaShape3::Finite_facets_iterator facet);
static PyObject* AlphaShape3_dump_vtk(AlphaShape3* self,PyObject* args);

// Read n-th point from ndarray and create CGAL's Weighted_point 
static void InsertNthWeightedPoint(PyArrayObject* points,
                                   npy_intp n, int weighted, int rel_homology,
                                   std::vector<PointWithInfo>* points_vector) {
  typedef CGAL_AlphaShape3::Weighted_point Weighted_point;
  typedef CGAL_AlphaShape3::Bare_point Bare_point;

  double x = *GETPTR2D<double>(points, n, 0);
  double y = *GETPTR2D<double>(points, n, 1);
  double z = *GETPTR2D<double>(points, n, 2);
  double w = weighted ? *GETPTR2D<double>(points, n, 3) : 0.0;
  int group_name = GroupName(3, points, n, weighted, rel_homology);
  points_vector->emplace_back(Weighted_point(Bare_point(x, y, z), w),
                              VertexInfo{static_cast<int>(n), group_name});
}

static bool AllWeightsAreNonNegative(const std::vector<PointWithInfo>& points_vector) {
  for (unsigned i=0; i<points_vector.size(); ++i)
    if (points_vector[i].first.weight() < 0.0)
      return false;
  return true;
}

static int AlphaShape3_init(AlphaShape3* self,
                            PyObject* args,
                            PyObject* kwds) {
  PyArrayObject* points;
  int weighted, rel_homology;

  if (!PyArg_ParseTuple(args, "O!pp", &PyArray_Type, &points, &weighted, &rel_homology)) 
    return -1;

  if (!ArrayHasCorrectShape(points, 3, weighted, rel_homology))
    return -1;
  if (!ArrayIsDoubleType(points))
    return -1;

  npy_intp* dims = PyArray_DIMS(points);

  std::vector<PointWithInfo> points_vector;
  
  for (npy_intp i=0; i<dims[0]; ++i) 
    InsertNthWeightedPoint(points, i, weighted, rel_homology, &points_vector);

  if (!AllWeightsAreNonNegative(points_vector)) {
    PyErr_SetString(PyExc_ValueError, "Weight must be non-negative");
    return -1;
  }

  Triangulation triangulation(points_vector.begin(), points_vector.end());
  self->alpha_shape_ = new CGAL_AlphaShape3(triangulation, 0, CGAL_AlphaShape3::GENERAL);

  return 0;
}

// Return all finite vertices
static PyObject* AlphaShape3_vertices(AlphaShape3* self) {
  return AlphaShape_tolist<AlphaShape3_Types, Vertex>
      (
        self,
        self->alpha_shape_->finite_vertices_begin(),
        self->alpha_shape_->finite_vertices_end(),
        self->alpha_shape_->number_of_vertices(),
        Vertex_New
       );
}

// Return all finite cells
static PyObject* AlphaShape3_cells(AlphaShape3* self) {
    return AlphaShape_tolist<AlphaShape3_Types, Cell>
      (
        self,
        self->alpha_shape_->finite_cells_begin(),
        self->alpha_shape_->finite_cells_end(),
        self->alpha_shape_->number_of_finite_cells(),
        Cell_New
       );
}

static PyObject* AlphaShape3_edges(AlphaShape3* self) {
  return AlphaShape_tolist<AlphaShape3_Types, Edge>
      (
        self,
        self->alpha_shape_->finite_edges_begin(),
        self->alpha_shape_->finite_edges_end(),
        self->alpha_shape_->number_of_finite_edges(),
        Edge_New
       );
}

static PyObject* AlphaShape3_facets(AlphaShape3* self) {
  return AlphaShape_tolist<AlphaShape3_Types, Facet>
      (
        self,
        self->alpha_shape_->finite_facets_begin(),
        self->alpha_shape_->finite_facets_end(),
        self->alpha_shape_->number_of_finite_facets(),
        Facet_New
       );
}

static PyObject* Vertex_vertices(PyObject* self) {
  return Py_BuildValue("(O)", self);
}

static PyObject* Vertex_point(Vertex* self) {
  npy_intp dims[1] = {3};
  PyArrayObject* ary = reinterpret_cast<PyArrayObject*>(PyArray_SimpleNew(1, dims, NPY_DOUBLE));
  auto point = self->handle_->point();

  *GETPTR1D<double>(ary, 0) = point.x();
  *GETPTR1D<double>(ary, 1) = point.y();
  *GETPTR1D<double>(ary, 2) = point.z();

  return cast_PyObj(ary);
}

static PyObject* Vertex_weight(Vertex* self) {
  return Py_BuildValue("d", self->handle_->point().weight());
}

static bool Vertex_equal(PyObject* o1, PyObject* o2);

static PyObject* Vertex_compare(PyObject* o1, PyObject* o2, int op) {
  switch (op) {
    case Py_EQ:
      return PyBool_FromLong(Vertex_equal(o1, o2));
    case Py_NE:
      return PyBool_FromLong(!Vertex_equal(o1, o2));
    default:
      PyErr_SetString(PyExc_TypeError, "Inequality operators are not supported");
      return NULL;
  }
}

static Py_hash_t Vertex_hash(Vertex* self) {
  return reinterpret_cast<Py_hash_t>(self->alpha_) + self->vertex_index_;
}

static bool Cell_equal(PyObject* o1, PyObject* o2);

static PyObject* Cell_compare(PyObject* o1, PyObject* o2, int op) {
  switch (op) {
    case Py_EQ:
      return PyBool_FromLong(Cell_equal(o1, o2));
    case Py_NE:
      return PyBool_FromLong(!Cell_equal(o1, o2));
    default:
      PyErr_SetString(PyExc_TypeError, "Inequality operators are not supported");
      return NULL;
  }
}

static PyObject* Cell_vertices(Cell* self) {
  PyObject* vertices = PyTuple_New(4);
  if (!vertices) return NULL;
  
  for (int i=0; i<4; ++i) {
    CGAL_AlphaShape3::Vertex_handle v_handle = self->handle_->vertex(i);
    Vertex* vertex = Vertex_New(self->alpha_, v_handle);
    if (!vertex) goto error;
    PyTuple_SET_ITEM(vertices, i, cast_PyObj(vertex));
  }
  return vertices;
  
error:
  Py_DECREF(vertices);
  return NULL;
}

static PyObject* Edge_vertices(Edge* self) {
  Vertex* v1 = NULL;
  Vertex* v2 = NULL;
      
  v1 = Vertex_New(self->alpha_, self->v1);
  if (!v1) goto error;
  v2 = Vertex_New(self->alpha_, self->v2);
  if (!v2) goto error;

  return Py_BuildValue("NN", v1, v2);
  
error:
  Py_XDECREF(v1);
  Py_XDECREF(v2);
  return NULL;
}

static PyObject* Facet_vertices(Facet* self) {
  PyObject* vertices = PyTuple_New(3);
  if (!vertices) return NULL;

  for (int i=0; i<3; ++i) {
    CGAL_AlphaShape3::Vertex_handle v_handle = self->cell_->vertex((self->v_+i+1) % 4);
    Vertex* vertex = Vertex_New(self->alpha_, v_handle);
    if (!vertex) goto error;
    PyTuple_SET_ITEM(vertices, i, cast_PyObj(vertex));
  }
  return vertices;

error:
  Py_DECREF(vertices);
  return NULL;
}

static PyMethodDef AlphaShape3_methods[] = {
  {"vertices",
   (PyCFunction)AlphaShape3_vertices, METH_NOARGS,
   "Return vertices"},
  {"cells",
   (PyCFunction)AlphaShape3_cells, METH_NOARGS,
   "Return cells"},
  {"edges",
   (PyCFunction)AlphaShape3_edges, METH_NOARGS,
   "Return edges"},
  {"facets",
   (PyCFunction)AlphaShape3_facets, METH_NOARGS,
   "Return facets"},
  // for debug
  {"dump_vtk",
   (PyCFunction)AlphaShape3_dump_vtk, METH_VARARGS,
   "Save as a vtk format"},
  {NULL}
};

static PyTypeObject AlphaShape3Type = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.alpha_shape3.AlphaShape3", // tp_name
  sizeof(AlphaShape3), // tp_basicsize 
  0, // tp_itemsize
  (destructor)AlphaShape3_dealloc, // tp_dealloc 
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
  "3D Alpha Shape",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  AlphaShape3_methods,  // tp_methods 
  0, // tp_members
  0, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(AlphaShape3_init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 

static PyMethodDef Vertex_methods[] = {
  {"vertices", (PyCFunction)Vertex_vertices, METH_NOARGS,
   "Return the tuple whose element is self"},
  {"point", (PyCFunction)Vertex_point, METH_NOARGS,
   "Return the coordinate of the vertex"},
  {"weight", (PyCFunction)Vertex_weight, METH_NOARGS,
   "Return the weight of the vertex"},
  {"isvertex", (PyCFunction)method_return_true, METH_NOARGS, "Return True"},
  {NULL}
};

static PyMemberDef Vertex_members[] = {
  {"vertex_index", T_INT, offsetof(Vertex, vertex_index_), READONLY,
   "The unique index of the vertex"},
  {"group_name", T_INT, offsetof(Vertex, group_name_), READONLY,
   "Group name of the vertex"},
  {"birth_radius", T_DOUBLE, offsetof(Vertex, birth_radius_), 0,
   "Birth radius of the vertex"},
  {NULL}
};


static PyTypeObject VertexType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.alpha_shape3.AlphaShape3.Vertex", // tp_name
  sizeof(Vertex), // tp_basicsize 
  0, // tp_itemsize
  (destructor)Vertex_dealloc, // tp_dealloc 
  0, // tp_print
  0, // tp_getattr
  0, // tp_setattr
  0, // tp_reserved
  0, // tp_repr
  0, // tp_as_number
  0, // tp_as_sequence
  0, // tp_as_mapping
  (hashfunc)Vertex_hash, // tp_hash 
  0, // tp_call
  0, // tp_str
  0, // tp_getattro
  0, // tp_setattro
  0, // tp_as_buffer
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, // tp_flags 
  "Vertex class for AlphaShape3",  // tp_doc 
  (traverseproc)Vertex_traverse, // tp_traverse
  (inquiry)Vertex_clear, // tp_clear
  Vertex_compare, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Vertex_methods,  // tp_methods 
  Vertex_members,  // tp_members 
  0, // tp_getset 
};

static PyMethodDef Cell_methods[] = {
  {"vertices",
   (PyCFunction)Cell_vertices, METH_NOARGS,
   "Return vertices of the cell"},
  {"isvertex", (PyCFunction)method_return_false, METH_NOARGS, "Return False"},
  {NULL}
};
  
static PyMemberDef Cell_members[] = {
  {"birth_radius", T_DOUBLE, offsetof(Cell, birth_radius_), 0,
   "Birth radius of the cell"},
  {NULL}
};

static PyTypeObject CellType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.alpha_shape.AlphaShape3.Cell", // tp_name
  sizeof(Cell), // tp_basicsize 
  0, // tp_itemsize
  (destructor)Cell_dealloc, // tp_dealloc 
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
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, // tp_flags 
  "Cell class for AlphaShape3",  // tp_doc 
  (traverseproc)Cell_traverse, // tp_traverse
  (inquiry)Cell_clear, // tp_clear
  Cell_compare, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Cell_methods, // tp_methods 
  Cell_members, // tp_members 
  0, // tp_getset 
};

static PyMethodDef Edge_methods[] = {
  {"vertices", (PyCFunction)Edge_vertices, METH_NOARGS,
   "Return endpoint vertices of the edge"},
  {"isvertex", (PyCFunction)method_return_false, METH_NOARGS, "Return False"},
  {NULL}
};
  
static PyMemberDef Edge_members[] = {
  {"birth_radius", T_DOUBLE, offsetof(Edge, birth_radius_), 0,
   "Birth radius of the edge"},
  {NULL}
};

static PyTypeObject EdgeType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.alpha_shape.AlphaShape3.Edge", // tp_name
  sizeof(Edge), // tp_basicsize 
  0, // tp_itemsize
  (destructor)Edge_dealloc, // tp_dealloc 
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
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, // tp_flags 
  "Edge class for AlphaShape3",  // tp_doc 
  (traverseproc)Edge_traverse, // tp_traverse
  (inquiry)Edge_clear, // tp_clear
  0, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Edge_methods, // tp_methods 
  Edge_members, // tp_members 
  0, // tp_getset 
};

static PyMethodDef Facet_methods[] = {
  {"vertices", (PyCFunction)Facet_vertices, METH_NOARGS,
   "Return endpoint vertices of the edge"},
  {"isvertex", (PyCFunction)method_return_false, METH_NOARGS, "Return False"},
  {NULL}
};
  
static PyMemberDef Facet_members[] = {
  {"birth_radius", T_DOUBLE, offsetof(Facet, birth_radius_), 0,
   "Birth radius of the edge"},
  {NULL}
};

static PyTypeObject FacetType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.alpha_shape.AlphaShape3.Facet", // tp_name
  sizeof(Facet), // tp_basicsize 
  0, // tp_itemsize
  (destructor)Facet_dealloc, // tp_dealloc 
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
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, // tp_flags 
  "Facet class for AlphaShape3",  // tp_doc 
  (traverseproc)Facet_traverse, // tp_traverse
  (inquiry)Facet_clear, // tp_clear
  0, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Facet_methods, // tp_methods 
  Facet_members, // tp_members 
  0, // tp_getset 
};

static double BirthRadius(const CGAL::Alpha_status<double>& status) {
  return status.is_Gabriel() ? status.alpha_min() : status.alpha_mid();
}

static PyObject* AlphaShape3_dump_vtk(AlphaShape3* self,PyObject* args){
  const char* filename;
  if( !PyArg_ParseTuple(args, "s", &filename) ){
    return NULL;
  }
  int numCells = self->alpha_shape_->number_of_finite_cells();
  int numFacets = self->alpha_shape_->number_of_finite_facets();
  int numEdges = self->alpha_shape_->number_of_finite_edges();
  int numVertices = self->alpha_shape_->number_of_vertices();
  std::ofstream output(filename, std::ios_base::out);
  output << "# vtk DataFile Version 3.0" << std::endl;
  output << "Alpha Shape 3D Dump File by HomCloud" << std::endl;
  output << "ASCII" << std::endl;
  output << "DATASET UNSTRUCTURED_GRID" << std::endl;
  output << "POINTS " << numVertices << " double" << std::endl;
  std::map<CGAL_AlphaShape3::Vertex_handle, int> index_of_vertex;
  int index=0;
  for( auto it = self->alpha_shape_->finite_vertices_begin(); it != self->alpha_shape_->finite_vertices_end(); ++it )
  {
    output << self->alpha_shape_->point(it).point() << std::endl;
    index_of_vertex[it] = index;
    ++index;
  }
  int numSimplices = numCells + numFacets + numEdges + numVertices;
  int numIndices = 5*numCells + 4*numFacets + 3*numEdges + 2*numVertices;
  output << "CELLS" << " " << numSimplices << " " << numIndices << std::endl;
  for( auto c=self->alpha_shape_->finite_cells_begin();
      c!=self->alpha_shape_->finite_cells_end();
      ++c)
  {
    CGAL_AlphaShape3::Vertex_handle v0 = c->vertex(0);
    CGAL_AlphaShape3::Vertex_handle v1 = c->vertex(1);
    CGAL_AlphaShape3::Vertex_handle v2 = c->vertex(2);
    CGAL_AlphaShape3::Vertex_handle v3 = c->vertex(3);
    int i0 = index_of_vertex[v0];
    int i1 = index_of_vertex[v1];
    int i2 = index_of_vertex[v2];
    int i3 = index_of_vertex[v3];
    output << 4 << " " << i0 << " " << i1 << " " << i2 << " " << i3 << std::endl;
  }
  int facet_indices[4][3] = {
    {1,2,3},
    {2,3,0},
    {3,0,1},
    {0,1,2},
  };
  for( auto f=self->alpha_shape_->finite_facets_begin();
      f!=self->alpha_shape_->finite_facets_end();
      ++f)
  {
    CGAL_AlphaShape3::Vertex_handle v0 = f->first->vertex(facet_indices[f->second][0]);
    CGAL_AlphaShape3::Vertex_handle v1 = f->first->vertex(facet_indices[f->second][1]);
    CGAL_AlphaShape3::Vertex_handle v2 = f->first->vertex(facet_indices[f->second][2]);
    int i0 = index_of_vertex[v0];
    int i1 = index_of_vertex[v1];
    int i2 = index_of_vertex[v2];
    output << 3 << " " << i0 << " " << i1 << " " << i2 << std::endl;
  }
  for( auto e=self->alpha_shape_->finite_edges_begin();
      e!=self->alpha_shape_->finite_edges_end();
      ++e)
  {
    CGAL_AlphaShape3::Vertex_handle v0 = e->first->vertex(e->second);
    CGAL_AlphaShape3::Vertex_handle v1 = e->first->vertex(e->third);
    int i0 = index_of_vertex[v0];
    int i1 = index_of_vertex[v1];
    output << 2 << " " << i0 << " " << i1 << std::endl;
  }
  for( auto v = self->alpha_shape_->finite_vertices_begin();
      v != self->alpha_shape_->finite_vertices_end();
      ++v )
  {
    int i0 = index_of_vertex[v];
    output << 1 << " " << i0 << std::endl;
  }
  output << "CELL_TYPES" << " " << numSimplices << std::endl;
  for(int i=0;i<numCells;++i){
    output << 10 << std::endl;
  }
  for(int i=0;i<numFacets;++i){
    output << 5 << std::endl;
  }
  for(int i=0;i<numEdges;++i){
    output << 3 << std::endl;
  }
  for(int i=0;i<numVertices;++i){
    output << 1 << std::endl;
  }
  output << "POINT_DATA" << " " << numVertices << std::endl;
  {
    output << "SCALARS degree int 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( auto it = self->alpha_shape_->finite_vertices_begin(); it != self->alpha_shape_->finite_vertices_end(); ++it )
    {
      output << self->alpha_shape_->degree(it) << std::endl;
    }
  }
  {
    output << "SCALARS weight double 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( auto it = self->alpha_shape_->finite_vertices_begin(); it != self->alpha_shape_->finite_vertices_end(); ++it )
    {
      output << self->alpha_shape_->point(it).weight() << std::endl;
    }
  }
  output << "CELL_DATA" << " " << numSimplices << std::endl;
  {
    output << "SCALARS dim int 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for(int i=0;i<numCells;++i){
      output << 3 << std::endl;
    }
    for(int i=0;i<numFacets;++i){
      output << 2 << std::endl;
    }
    for(int i=0;i<numEdges;++i){
      output << 1 << std::endl;
    }
    for(int i=0;i<numVertices;++i){
      output << 0 << std::endl;
    }
  }
  {
    output << "SCALARS alpha double 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    std::cout << "cell alpha" << std::endl;
    for( auto c=self->alpha_shape_->finite_cells_begin();
        c!=self->alpha_shape_->finite_cells_end();
        ++c)
    {
      output << c->get_alpha() << std::endl;
    }
    std::cout << "facet alpha" << std::endl;
    for( auto f=self->alpha_shape_->finite_facets_begin();
        f!=self->alpha_shape_->finite_facets_end();
        ++f)
    {
      output << BirthRadius(self->alpha_shape_->get_alpha_status(*f)) << std::endl;
    }
    std::cout << "edge alpha" << std::endl;
    for( auto e=self->alpha_shape_->finite_edges_begin();
        e!=self->alpha_shape_->finite_edges_end();
        ++e)
    {
      output << BirthRadius(self->alpha_shape_->get_alpha_status(*e)) << std::endl;
    }
    std::cout << "vertex alpha" << std::endl;
    for( auto it = self->alpha_shape_->finite_vertices_begin(); it != self->alpha_shape_->finite_vertices_end(); ++it )
    {
      output << -it->point().weight() << std::endl;
    }
  }
/*
  {
    output << "SCALARS power_sphere double 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    std::cout << "cell power sphere" << std::endl;
    for( auto c=self->alpha_shape_->finite_cells_begin();
        c!=self->alpha_shape_->finite_cells_end();
        ++c)
    {
      output << AlphaValueCell(self->alpha_shape_,c) << std::endl;
    }
    std::cout << "facet power sphere" << std::endl;
    for( auto f=self->alpha_shape_->finite_facets_begin();
        f!=self->alpha_shape_->finite_facets_end();
        ++f)
    {
      output << AlphaValueFacet(self->alpha_shape_,f) << std::endl;
    }
    std::cout << "edge power sphere" << std::endl;
    for( auto e=self->alpha_shape_->finite_edges_begin();
        e!=self->alpha_shape_->finite_edges_end();
        ++e)
    {
      output << AlphaValueEdge(self->alpha_shape_,e) << std::endl;
    }
    std::cout << "vertex power sphere" << std::endl;
    for( auto it = self->alpha_shape_->finite_vertices_begin(); it != self->alpha_shape_->finite_vertices_end(); ++it )
    {
      output << -it->point().weight() << std::endl;
    }
  }
*/
  output.close();
  return Py_BuildValue("i",0);
}

static Vertex* Vertex_New(AlphaShape3* alpha,
                          CGAL_AlphaShape3::Vertex_handle handle) {
  Vertex* vertex = (Vertex*)VertexType.tp_alloc(&VertexType, 0);
  if (!vertex) return NULL;
  
  vertex->alpha_ = alpha;
  vertex->handle_ = handle;
  vertex->vertex_index_ = handle->info().vertex_index;
  vertex->group_name_ = handle->info().group_name;
  vertex->birth_radius_ = -(handle->point().weight());
  Py_INCREF(alpha);

  return vertex;
}

static Cell* Cell_New(AlphaShape3* alpha, CGAL_AlphaShape3::Cell_handle handle) {
  Cell* cell = (Cell*)CellType.tp_alloc(&CellType, 0);
  if (!cell) return NULL;

  cell->alpha_ = alpha;
  cell->handle_ = handle;
  cell->birth_radius_ = handle->get_alpha();
  Py_INCREF(alpha);

  return cell;
}

static Edge* Edge_New(AlphaShape3* alpha,
                      CGAL_AlphaShape3::Finite_edges_iterator iter) {
  Edge* edge = (Edge*)EdgeType.tp_alloc(&EdgeType, 0);
  if (!edge) return NULL;

  
  edge->alpha_ = alpha;
  edge->v1 = iter->first->vertex(iter->second);
  edge->v2 = iter->first->vertex(iter->third);
  edge->birth_radius_ =
      BirthRadius(alpha->alpha_shape_->get_alpha_status(*iter));
  Py_INCREF(alpha);

  return edge;
}

static Facet* Facet_New(AlphaShape3* alpha,
                        CGAL_AlphaShape3::Finite_facets_iterator iter) {
  Facet* facet = (Facet*)FacetType.tp_alloc(&FacetType, 0);
  if (!facet) return NULL;

  facet->alpha_ = alpha;
  facet->cell_ = iter->first;
  facet->v_ = iter->second;
  facet->birth_radius_ =
      BirthRadius(alpha->alpha_shape_->get_alpha_status(*iter));
  Py_INCREF(alpha);

  return facet;
}

static bool Vertex_equal(PyObject* o1, PyObject* o2) {
  if (!PyObject_TypeCheck(o1, &VertexType) || !PyObject_TypeCheck(o1, &VertexType))
    return false;
  Vertex* v1 = reinterpret_cast<Vertex*>(o1);
  Vertex* v2 = reinterpret_cast<Vertex*>(o2);
  return v1->alpha_ == v2->alpha_ && v1->handle_ == v2->handle_;
}

static bool Cell_equal(PyObject* o1, PyObject* o2) {
  if (!PyObject_TypeCheck(o1, &CellType) || !PyObject_TypeCheck(o1, &CellType))
    return false;
  Cell* c1 = reinterpret_cast<Cell*>(o1);
  Cell* c2 = reinterpret_cast<Cell*>(o2);
  return c1->alpha_ == c2->alpha_ && c1->handle_ == c2->handle_;
}

static PyModuleDef alpha_shape3_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.alpha_shape3",
  "The module for 3D Alpha shape",
  -1,
  NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_alpha_shape3()
{
  if (PyType_Ready(&AlphaShape3Type) < 0)
    return NULL;
  if (PyType_Ready(&VertexType) < 0)
    return NULL;
  if (PyType_Ready(&CellType) < 0)
    return NULL;
  if (PyType_Ready(&EdgeType) < 0)
    return NULL;
  if (PyType_Ready(&FacetType) < 0)
    return NULL;

  PyObject* module = PyModule_Create(&alpha_shape3_Module);

  if (!module)
    return NULL;

  Py_INCREF(&AlphaShape3Type);
  PyModule_AddObject(module, "AlphaShape3", cast_PyObj(&AlphaShape3Type));
  Py_INCREF(&VertexType);
  PyModule_AddObject(module, "Vertex", cast_PyObj(&VertexType));
  Py_INCREF(&CellType);
  PyModule_AddObject(module, "Cell", cast_PyObj(&CellType));
  Py_INCREF(&EdgeType);
  PyModule_AddObject(module, "Edge", cast_PyObj(&EdgeType));
  Py_INCREF(&FacetType);
  PyModule_AddObject(module, "Facet", cast_PyObj(&FacetType));
  
  import_array();

  return module;
}


