#include "homcloud_common.h"
#include "homcloud_cgal.h"
#include "homcloud_numpy.h"
#include "alpha_shape_common.h"

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>


#include <CGAL/Periodic_2_Delaunay_triangulation_traits_2.h>
#include <CGAL/Periodic_2_Delaunay_triangulation_2.h>
 
#include <CGAL/Alpha_shape_2.h>
#include <CGAL/Alpha_shape_face_base_2.h>
#include <CGAL/Alpha_shape_vertex_base_2.h>
#include <CGAL/Triangulation_vertex_base_with_info_2.h>

struct VertexInfo {
  int vertex_index, group_name;
};

// Traits
typedef CGAL::Exact_predicates_inexact_constructions_kernel Kernel;
typedef CGAL::Periodic_2_Delaunay_triangulation_traits_2<Kernel> Gt;

// Vertex types
typedef CGAL::Periodic_2_triangulation_vertex_base_2<Gt> Vb;
typedef CGAL::Triangulation_vertex_base_with_info_2<VertexInfo, Gt, Vb> Vinfo;
typedef CGAL::Alpha_shape_vertex_base_2<Gt, Vinfo> AsVb;

// Cell types
typedef CGAL::Periodic_2_triangulation_face_base_2<Gt> Cb;
typedef CGAL::Alpha_shape_face_base_2<Gt, Cb> AsCb;


typedef CGAL::Triangulation_data_structure_2<AsVb, AsCb> Tds;
typedef CGAL::Periodic_2_Delaunay_triangulation_2<Gt, Tds> P2DT2;
typedef CGAL::Alpha_shape_2<P2DT2> CGAL_PeriodicAlphaShape2;

typedef std::pair<Gt::Point_2, VertexInfo> PointWithInfo;

typedef struct {
  PyObject_HEAD
  CGAL_PeriodicAlphaShape2* alpha_shape_;
} PeriodicAlphaShape2;

typedef struct {
  PyObject_HEAD
  PeriodicAlphaShape2* alpha_;
  CGAL_PeriodicAlphaShape2::Vertex_handle handle_;
  int vertex_index_;
  int group_name_;
  double birth_radius_;
} Vertex;

typedef struct {
  PyObject_HEAD
  PeriodicAlphaShape2* alpha_;
  CGAL_PeriodicAlphaShape2::Face_handle handle_;
  double birth_radius_;
} Face;

typedef struct {
  PyObject_HEAD
  PeriodicAlphaShape2* alpha_;
  CGAL_PeriodicAlphaShape2::Vertex_handle v1, v2;
  double birth_radius_;
} Edge;


struct PeriodicAlphaShape2_Types {
  typedef CGAL_PeriodicAlphaShape2 CGAL_ALphaShape;
  typedef PeriodicAlphaShape2 AlphaShape;
  typedef ::Vertex Vertex;
  typedef ::Edge Edge;
  typedef ::Face Face;
};

static void PeriodicAlphaShape2_dealloc(PeriodicAlphaShape2* self) {
  delete self->alpha_shape_;
  self->alpha_shape_ = NULL;
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static void Vertex_dealloc(Vertex* self) {
  Py_XDECREF(self->alpha_);
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static void Face_dealloc(Face* self) {
  Py_XDECREF(self->alpha_);
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static void Edge_dealloc(Edge* self) {
  Py_XDECREF(self->alpha_);
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static Vertex* Vertex_New(PeriodicAlphaShape2* alpha,
                          CGAL_PeriodicAlphaShape2::Vertex_handle handle);
static Face* Face_New(PeriodicAlphaShape2* alpha,
                      CGAL_PeriodicAlphaShape2::Face_handle handle);
static Edge* Edge_New(PeriodicAlphaShape2* alpha,
                      CGAL_PeriodicAlphaShape2::Finite_edges_iterator edge);


// Read n-th point from ndarray and create CGAL's point 
static void InsertNthPoint(PyArrayObject* points,
                           npy_intp n, int rel_homology,
                           std::vector<PointWithInfo>* points_vector) {
  double x = *GETPTR2D<double>(points, n, 0);
  double y = *GETPTR2D<double>(points, n, 1);
  int group_name = GroupName(2, points, n, 0, rel_homology);
  
   points_vector->emplace_back(Gt::Point_2(x, y), VertexInfo{static_cast<int>(n), group_name});
}

static int PeriodicAlphaShape2_init(PeriodicAlphaShape2* self,
                                    PyObject* args,
                                    PyObject* kwds) {
  PyArrayObject* points;
  int weighted, rel_homology;
  double xmin, xmax, ymin, ymax;

  if (!PyArg_ParseTuple(args, "O!ppdddd", &PyArray_Type, &points, &weighted, &rel_homology, &xmin, &xmax, &ymin, &ymax))
    return -1;

  if (weighted) {
    PyErr_SetString(PyExc_ValueError, "2D Periodic alpha shape does not accept weighted points");
    return -1;
  }
  if (!ArrayHasCorrectShape(points, 2, 0, rel_homology))
    return -1;
  if (!ArrayIsDoubleType(points))
    return -1;
  if (!((xmin < xmax) && (ymin < ymax))) {
    PyErr_SetString(PyExc_ValueError, "Periodic region invalid");
    return -1;
  }
  double ratio = (xmax - xmin) / (ymax - ymin);
  if (ratio > 1.6 || ratio < 1 / 1.6) {
    PyErr_SetString(PyExc_ValueError, "Too anistropic periodic region is invalid (1.6)");
    return -1;
  }

  npy_intp* dims = PyArray_DIMS(points);

  std::vector<PointWithInfo> points_vector;
  
  for (npy_intp i=0; i<dims[0]; ++i) {
    InsertNthPoint(points, i, rel_homology, &points_vector);
  }

  P2DT2::Iso_rectangle domain(xmin, ymin, xmax, ymax);
  P2DT2 triangulation(points_vector.begin(), points_vector.end(), domain);

  if (triangulation.is_triangulation_in_1_sheet())
    triangulation.convert_to_1_sheeted_covering();

  self->alpha_shape_ = new CGAL_PeriodicAlphaShape2(triangulation, 0, CGAL_PeriodicAlphaShape2::GENERAL);
  
  return 0;
}

// Return all finite vertices
static PyObject* PeriodicAlphaShape2_vertices(PeriodicAlphaShape2* self) {
  return AlphaShape_tolist<PeriodicAlphaShape2_Types, Vertex>
      (
        self,
        self->alpha_shape_->finite_vertices_begin(),
        self->alpha_shape_->finite_vertices_end(),
        self->alpha_shape_->number_of_vertices(),
        Vertex_New
       );
}

// Return all finite faces
static PyObject* PeriodicAlphaShape2_faces(PeriodicAlphaShape2* self) {
    return AlphaShape_tolist<PeriodicAlphaShape2_Types, Face>
      (
        self,
        self->alpha_shape_->finite_faces_begin(),
        self->alpha_shape_->finite_faces_end(),
        self->alpha_shape_->number_of_faces(),
        Face_New
       );
}

static PyObject* PeriodicAlphaShape2_edges(PeriodicAlphaShape2* self) {
  return AlphaShape_tolist<PeriodicAlphaShape2_Types, Edge>
      (
        self,
        self->alpha_shape_->finite_edges_begin(),
        self->alpha_shape_->finite_edges_end(),
        std::distance(self->alpha_shape_->finite_edges_begin(),
                      self->alpha_shape_->finite_edges_end()),
        Edge_New
       );
}


static PyObject* Vertex_vertices(PyObject* self) {
  return Py_BuildValue("(O)", self);
}

static PyObject* Vertex_point(Vertex* self) {
  npy_intp dims[1] = {2};
  PyArrayObject* ary = reinterpret_cast<PyArrayObject*>(PyArray_SimpleNew(1, dims, NPY_DOUBLE));
  auto point = self->handle_->point();

  *GETPTR1D<double>(ary, 0) = point.x();
  *GETPTR1D<double>(ary, 1) = point.y();

  return cast_PyObj(ary);
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

static bool Face_equal(PyObject* o1, PyObject* o2);

static PyObject* Face_compare(PyObject* o1, PyObject* o2, int op) {
  switch (op) {
    case Py_EQ:
      return PyBool_FromLong(Face_equal(o1, o2));
    case Py_NE:
      return PyBool_FromLong(!Face_equal(o1, o2));
    default:
      PyErr_SetString(PyExc_TypeError, "Inequality operators are not supported");
      return NULL;
  }
}

static PyObject* Face_vertices(Face* self) {
  PyObject* vertices = PyTuple_New(3);
  if (!vertices) return NULL;
  
  for (int i=0; i<3; ++i) {
    CGAL_PeriodicAlphaShape2::Vertex_handle v_handle = self->handle_->vertex(i);
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


static PyMethodDef PeriodicAlphaShape2_methods[] = {
  {"vertices",
   (PyCFunction)PeriodicAlphaShape2_vertices, METH_NOARGS,
   "Return vertices"},
  {"faces",
   (PyCFunction)PeriodicAlphaShape2_faces, METH_NOARGS,
   "Return faces"},
  {"edges",
   (PyCFunction)PeriodicAlphaShape2_edges, METH_NOARGS,
   "Return edges"},
  {NULL}
};

static PyTypeObject PeriodicAlphaShape2Type = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.periodic_alpha_shape2.PeriodicAlphaShape2", // tp_name
  sizeof(PeriodicAlphaShape2), // tp_basicsize 
  0, // tp_itemsize
  (destructor)PeriodicAlphaShape2_dealloc, // tp_dealloc 
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
  "2D Periodic Alpha Shape",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  PeriodicAlphaShape2_methods,  // tp_methods 
  0, // tp_members
  0, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(PeriodicAlphaShape2_init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 

static PyMethodDef Vertex_methods[] = {
  {"vertices", (PyCFunction)Vertex_vertices, METH_NOARGS,
   "Return the tuple whose element is self"},
  {"point", (PyCFunction)Vertex_point, METH_NOARGS,
   "Return the coordinate of the vertex"},
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
  "homcloud.periodic.alpha_shape2.PeriodicAlphaShape2.Vertex", // tp_name
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
  Py_TPFLAGS_DEFAULT, // tp_flags 
  "Vertex class for PeriodicAlphaShape2",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  Vertex_compare, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Vertex_methods,  // tp_methods 
  Vertex_members,  // tp_members 
  0, // tp_getset 
};

static PyMethodDef Face_methods[] = {
  {"vertices",
   (PyCFunction)Face_vertices, METH_NOARGS,
   "Return vertices of the face"},
  {"isvertex", (PyCFunction)method_return_false, METH_NOARGS, "Return False"},
  {NULL}
};
  
static PyMemberDef Face_members[] = {
  {"birth_radius", T_DOUBLE, offsetof(Face, birth_radius_), 0,
   "Birth radius of the face"},
  {NULL}
};

static PyTypeObject FaceType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.periodic_alpha_shape2.PeriodicAlphaShape2.Face", // tp_name
  sizeof(Face), // tp_basicsize 
  0, // tp_itemsize
  (destructor)Face_dealloc, // tp_dealloc 
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
  "Face class for PeriodicAlphaShape2",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  Face_compare, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Face_methods, // tp_methods 
  Face_members, // tp_members 
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
  "homcloud.periodic_alpha_shape2.PeriodicAlphaShape2.Edge", // tp_name
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
  Py_TPFLAGS_DEFAULT, // tp_flags 
  "Edge class for PeriodicAlphaShape2",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Edge_methods, // tp_methods 
  Edge_members, // tp_members 
  0, // tp_getset 
};


static Vertex* Vertex_New(PeriodicAlphaShape2* alpha,
                          CGAL_PeriodicAlphaShape2::Vertex_handle handle) {
  Vertex* vertex = PyObject_New(Vertex, &VertexType);
  if (!vertex) return NULL;
  
  vertex->alpha_ = alpha;
  vertex->handle_ = handle;
  vertex->vertex_index_ = handle->info().vertex_index;
  vertex->group_name_ = handle->info().group_name;
  vertex->birth_radius_ = 0.0;
  Py_INCREF(alpha);
  
  return vertex;
}

static Face* Face_New(PeriodicAlphaShape2* alpha, CGAL_PeriodicAlphaShape2::Face_handle handle) {
  Face* face = PyObject_New(Face, &FaceType);
  if (!face) return NULL;

  face->alpha_ = alpha;
  face->handle_ = handle;
  face->birth_radius_ = handle->get_alpha();
  Py_INCREF(alpha);

  return face;
}

static Edge* Edge_New(PeriodicAlphaShape2* alpha,
                      CGAL_PeriodicAlphaShape2::Finite_edges_iterator iter) {
  Edge* edge = PyObject_New(Edge, &EdgeType);
  if (!edge) return NULL;

  
  edge->alpha_ = alpha;
  edge->v1 = iter->first->vertex((iter->second + 1) % 3);
  edge->v2 = iter->first->vertex((iter->second + 2) % 3);
  //edge->birth_radius_ = CGAL::squared_distance(edge->v1->point(), edge->v2->point())/4;
  double a1 = iter->first->get_ranges(iter->second).get<0>();
  double a2 = iter->first->get_ranges(iter->second).get<1>();
  edge->birth_radius_ = (a1 > 0) ? a1 : a2;
  Py_INCREF(alpha);
  
  return edge;
}


static bool Vertex_equal(PyObject* o1, PyObject* o2) {
  if (!PyObject_TypeCheck(o1, &VertexType) || !PyObject_TypeCheck(o1, &VertexType))
    return false;
  Vertex* v1 = reinterpret_cast<Vertex*>(o1);
  Vertex* v2 = reinterpret_cast<Vertex*>(o2);
  return v1->alpha_ == v2->alpha_ && v1->handle_ == v2->handle_;
}

static bool Face_equal(PyObject* o1, PyObject* o2) {
  if (!PyObject_TypeCheck(o1, &FaceType) || !PyObject_TypeCheck(o1, &FaceType))
    return false;
  Face* c1 = reinterpret_cast<Face*>(o1);
  Face* c2 = reinterpret_cast<Face*>(o2);
  return c1->alpha_ == c2->alpha_ && c1->handle_ == c2->handle_;
}

static PyModuleDef periodic_alpha_shape2_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.periodic_alpha_shape2",
  "The module for 3D Alpha shape",
  -1,
  NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_periodic_alpha_shape2()
{
  if (PyType_Ready(&PeriodicAlphaShape2Type) < 0)
    return NULL;
  if (PyType_Ready(&VertexType) < 0)
    return NULL;
  if (PyType_Ready(&FaceType) < 0)
    return NULL;
  if (PyType_Ready(&EdgeType) < 0)
    return NULL;
  
  PyObject* module = PyModule_Create(&periodic_alpha_shape2_Module);
  if (!module)
    return NULL;

  Py_INCREF(&PeriodicAlphaShape2Type);
  PyModule_AddObject(module, "PeriodicAlphaShape2", cast_PyObj(&PeriodicAlphaShape2Type));
  Py_INCREF(&VertexType);
  PyModule_AddObject(module, "Vertex", cast_PyObj(&VertexType));
  Py_INCREF(&FaceType);
  PyModule_AddObject(module, "Face", cast_PyObj(&FaceType));
  Py_INCREF(&EdgeType);
  PyModule_AddObject(module, "Edge", cast_PyObj(&EdgeType));
  
  import_array();

  return module;
}
