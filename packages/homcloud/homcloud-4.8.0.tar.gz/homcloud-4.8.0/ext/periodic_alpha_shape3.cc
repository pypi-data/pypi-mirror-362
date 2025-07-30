#pragma GCC diagnostic ignored "-Wunused-function"

#include "homcloud_common.h"
#include "homcloud_cgal.h"
#include "homcloud_numpy.h"

#include "alpha_shape_common.h"

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Triangulation_vertex_base_with_info_3.h>
#include <CGAL/Periodic_3_Delaunay_triangulation_traits_3.h>
#include <CGAL/Periodic_3_Delaunay_triangulation_3.h>
#include <CGAL/Periodic_3_regular_triangulation_traits_3.h>
#include <CGAL/Periodic_3_regular_triangulation_3.h>
#include <CGAL/Alpha_shape_3.h>
#include <CGAL/Alpha_shape_cell_base_3.h>
#include <CGAL/Alpha_shape_vertex_base_3.h>

#include <map>
#include <vector>
#include <tuple>
#include <iostream>
#include <fstream>

#define PERIODIC_ALPHA_SHAPE_WITH_WEIGHT 1

// Traits
typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
#ifdef PERIODIC_DELAUNAY
typedef CGAL::Periodic_3_Delaunay_triangulation_traits_3<K> PK;
#else
typedef CGAL::Periodic_3_regular_triangulation_traits_3<K> PK;
#endif

// Vertex type
typedef CGAL::Periodic_3_triangulation_ds_vertex_base_3<> DsVb;
#ifdef PERIODIC_DELAUNAY
typedef CGAL::Triangulation_vertex_base_3<PK,DsVb> Vb;
#else
typedef CGAL::Regular_triangulation_vertex_base_3<PK,DsVb> Vb;
#endif
typedef CGAL::Alpha_shape_vertex_base_3<PK,Vb> AsVb;

template < class PK, class Vb,
           class AsVb = CGAL::Alpha_shape_vertex_base_3<PK,Vb> >
class Periodic_vertex_base_3 : public AsVb{
public:
  template < class TDS2 >
  struct Rebind_TDS {
    typedef typename AsVb::template Rebind_TDS<TDS2>::Other Vb2;
    typedef Periodic_vertex_base_3<PK, Vb2> Other;
  };
  typename AsVb::Vertex_handle base;
  int vertex_index;
  int group_name;
};
// Cell type
typedef CGAL::Periodic_3_triangulation_ds_cell_base_3<> DsCb;
#ifdef PERIODIC_DELAUNAY
typedef CGAL::Triangulation_cell_base_3<PK,DsCb> Cb;
#else
typedef CGAL::Regular_triangulation_cell_base_3<PK,DsCb> Cb;
#endif
typedef CGAL::Alpha_shape_cell_base_3<PK,Cb> AsCb;
template < class PK, class Cb,
           class AsCb = CGAL::Alpha_shape_cell_base_3<PK,Cb> >
class Periodic_cell_base_3 : public AsCb{
public:
  template < class TDS2 >
  struct Rebind_TDS {
    typedef typename AsCb::template Rebind_TDS<TDS2>::Other Cb2;
    typedef Periodic_cell_base_3<PK, Cb2> Other;
  };
  bool original;
};

// Triangulation Structure
typedef CGAL::Triangulation_data_structure_3<Periodic_vertex_base_3<PK,Vb>,AsCb> Tds;
#ifdef PERIODIC_DELAUNAY
typedef CGAL::Periodic_3_Delaunay_triangulation_3<PK,Tds> P3T3;
#else
typedef CGAL::Periodic_3_regular_triangulation_3<PK,Tds> P3T3;
#endif

typedef CGAL::Alpha_shape_3<P3T3> CGAL_AlphaShape3;
typedef P3T3::Iso_cuboid Iso_cuboid;
typedef P3T3::Covering_sheets Covering_sheets;
typedef P3T3::Bare_point Bare_point;
typedef P3T3::Weighted_point Weighted_point;

// Debug
typedef CGAL_AlphaShape3::FT Alpha_value_type;
typedef CGAL::Object Object;
typedef CGAL::Dispatch_output_iterator<CGAL::cpp11::tuple<Object, Alpha_value_type>,\
                                       CGAL::cpp11::tuple<std::back_insert_iterator<std::vector<Object> >,\
                                       std::back_insert_iterator<std::vector<Alpha_value_type> > > > Dispatch;

typedef struct {
  PyObject_HEAD
  CGAL_AlphaShape3* alpha_shape_;
  std::vector<CGAL_AlphaShape3::Cell_handle> unique_cells;
} PeriodicAlphaShape3;

typedef struct {
  PyObject_HEAD
  PeriodicAlphaShape3* alpha_;
  CGAL_AlphaShape3::Vertex_handle handle_;
  int vertex_index_;
  int group_name_;
  double birth_radius_;
} Vertex;

typedef struct {
  PyObject_HEAD
  PeriodicAlphaShape3* alpha_;
  CGAL_AlphaShape3::Cell_handle handle_;
  double birth_radius_;
} Cell;

typedef struct {
  PyObject_HEAD
  PeriodicAlphaShape3* alpha_;
  CGAL_AlphaShape3::Vertex_handle v1, v2;
  double birth_radius_;
} Edge;

typedef struct {
  PyObject_HEAD
  PeriodicAlphaShape3* alpha_;
  CGAL_AlphaShape3::Cell_handle cell_;
  int v_;
  double birth_radius_;
} Facet;

struct PeriodicAlphaShape3_Types {
  typedef CGAL_AlphaShape3 CGAL_AlphaShape;
  typedef PeriodicAlphaShape3 AlphaShape;
  typedef ::Vertex Vertex;
  typedef ::Edge Edge;
  typedef ::Facet Facet;
  typedef ::Cell Cell;
};

static Vertex* Vertex_New(PeriodicAlphaShape3* alpha, CGAL_AlphaShape3::Vertex_handle handle);
static Cell* Cell_New(PeriodicAlphaShape3* alpha, CGAL_AlphaShape3::Cell_handle handle);
static Edge* Edge_New(PeriodicAlphaShape3* alpha, CGAL_AlphaShape3::Edge &e);
static Facet* Facet_New(PeriodicAlphaShape3* alpha, CGAL_AlphaShape3::Facet &f);
bool isUniqueCell(CGAL_AlphaShape3* as,CGAL_AlphaShape3::Cell_handle cell);
bool isOverlappingCell(CGAL_AlphaShape3::Cell_handle cell);

static double BirthRadius(const CGAL::Alpha_status<double>& status) {
  return status.is_Gabriel() ? status.alpha_min() : status.alpha_mid();
}

template<typename C>
static double AlphaValueCell(CGAL_AlphaShape3* alpha_shape,C c)
{
  return c->get_alpha();
}

template<typename F>
static double AlphaValueFacet(CGAL_AlphaShape3* alpha_shape,F f)
{
  return BirthRadius(alpha_shape->get_alpha_status(*f));
}

template<typename E>
static double AlphaValueEdge(CGAL_AlphaShape3* alpha_shape,E e)
{
  return BirthRadius(alpha_shape->get_alpha_status(*e));
}

/////////////// AlphaShape ///////////////////////////
static int PeriodicAlphaShape3_init(PeriodicAlphaShape3* self, PyObject* args, PyObject* kwds) {
  PyArrayObject* points;
  int weighted, rel_homology;
  double xmin;
  double xmax;
  double ymin;
  double ymax;
  double zmin;
  double zmax;

  if (!PyArg_ParseTuple(args, "O!ppdddddd", &PyArray_Type, &points,
                        &weighted, &rel_homology, 
                        &xmin, &xmax, &ymin, &ymax, &zmin, &zmax))
    return -1;

  if (!ArrayHasCorrectShape(points, 3, weighted, rel_homology))
    return -1;
  if (!ArrayIsDoubleType(points))
    return -1;

#if (CGAL_VERSION_NR < 1050601000)
  if (xmax - xmin != ymax - ymin || xmax - xmin != zmax - zmin) {
    PyErr_SetString(PyExc_ValueError, "Noncubic periodic condition is only supported CGAL >= 5.6.");
    return -1;
  }
#endif

  npy_intp* dims = PyArray_DIMS(points);

  std::vector<Weighted_point> points_array;
  npy_intp num_points = dims[0];
  
  for (npy_intp i=0; i<dims[0]; ++i){
    double x = *GETPTR2D<double>(points, i, 0);
    double y = *GETPTR2D<double>(points, i, 1);
    double z = *GETPTR2D<double>(points, i, 2);
    double w = (weighted==1) ? *GETPTR2D<double>(points, i, 3) : 0.0;
    points_array.push_back(Weighted_point(Bare_point(x,y,z),w));
  }

  Iso_cuboid domain(xmin, ymin, zmin, xmax, ymax, zmax);  // the fundamental domain

  P3T3 triangulation(points_array.begin(), points_array.end(), domain);

  // triangulation.convert_to_27_sheeted_covering();
  triangulation.convert_to_1_sheeted_covering();


  self->alpha_shape_ = new CGAL_AlphaShape3(triangulation, 0, CGAL_AlphaShape3::GENERAL);

  // Create a map from coordinates of vertices to indices
  std::map<CGAL_AlphaShape3::Weighted_point, int> coord2index;
  for (int i = 0; i < num_points; ++i)
    coord2index.insert(std::make_pair(points_array[i], i));

  // 代表系の vertex_handle を base で覚えておく
  std::map<CGAL_AlphaShape3::Weighted_point,CGAL_AlphaShape3::Vertex_handle> coord2original;
  for (auto it = self->alpha_shape_->unique_vertices_begin();
       it != self->alpha_shape_->unique_vertices_end();
       ++it) {
    CGAL_AlphaShape3::Periodic_point pp = self->alpha_shape_->periodic_point(it);
    coord2original.insert(std::make_pair(pp.first, it));
    it->vertex_index = coord2index.at(pp.first);
    it->group_name = GroupName(3, points, it->vertex_index, weighted, rel_homology);
  }

  // base を割り当てる
  for (auto it = self->alpha_shape_->vertices_begin(); it != self->alpha_shape_->vertices_end(); ++it) {
    CGAL_AlphaShape3::Periodic_point pp = self->alpha_shape_->periodic_point(it);
    auto piter = coord2original.find(pp.first);
    if (piter != coord2original.end()) {
      it->base = piter->second;
    } else {
      PyErr_SetString(PyExc_ValueError, "No original point.");
      return -1;
    }
  }

  // 代表系の cell を unique_cells で記憶しておく
  for (auto iter = self->alpha_shape_->cells_begin();
       iter != self->alpha_shape_->cells_end();
       ++iter) {
    if (isOverlappingCell(iter)) {
      PyErr_SetString(PyExc_ValueError, "Overlapping cells.");
      return -1;
    } else {
      self->unique_cells.push_back(iter);
    }
  }

  return 0;
}

static void PeriodicAlphaShape3_dealloc(PeriodicAlphaShape3* self) {
  delete self->alpha_shape_;
  self->alpha_shape_ = nullptr;
  self->unique_cells.clear();
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static PyObject* PeriodicAlphaShape3_num_vertices(PeriodicAlphaShape3* self) {
  return Py_BuildValue("i", self->alpha_shape_->number_of_vertices());
}

// Return all unique vertices
static PyObject* PeriodicAlphaShape3_vertices(PeriodicAlphaShape3* self) {
  return AlphaShape_tolist<PeriodicAlphaShape3_Types, Vertex>
    (
      self,
      self->alpha_shape_->unique_vertices_begin(),
      self->alpha_shape_->unique_vertices_end(),
      self->alpha_shape_->number_of_vertices(),
      Vertex_New
    );
}

bool isUniqueCell(CGAL_AlphaShape3* as,CGAL_AlphaShape3::Cell_handle cell){
  CGAL_AlphaShape3::Periodic_tetrahedron t = as->periodic_tetrahedron(cell);
  int min_offset_x = 3;
  int min_offset_y = 3;
  int min_offset_z = 3;
  for(int i=0;i<4;++i){
    auto p = t[i];
    if( min_offset_x > p.second.x() ){
      min_offset_x = p.second.x();
    }
    if( min_offset_y > p.second.y() ){
      min_offset_y = p.second.y();
    }
    if( min_offset_z > p.second.z() ){
      min_offset_z = p.second.z();
    }
  }
  if( min_offset_x==1 && min_offset_y==1 && min_offset_z==1 ){
    return true;
  }else{
    return false;
  }
}

bool isOverlappingCell(CGAL_AlphaShape3::Cell_handle cell){
  int v0 = cell->vertex(0)->base->vertex_index;
  int v1 = cell->vertex(1)->base->vertex_index;
  int v2 = cell->vertex(2)->base->vertex_index;
  int v3 = cell->vertex(3)->base->vertex_index;
  if(
    v0 != v1 &&
    v0 != v2 &&
    v0 != v3 &&
    v1 != v2 &&
    v1 != v3 &&
    v2 != v3
  ){
    return false;
  }else{
    return true;
  }
}

// Return all unique cells
static PyObject* PeriodicAlphaShape3_cells(PeriodicAlphaShape3* self) {
  PyObject* list = PyList_New(self->alpha_shape_->number_of_cells());
  if (!list) return NULL;
  
  int index = 0;
  for (auto iter = self->unique_cells.begin();
    iter != self->unique_cells.end();
    ++iter,++index)
  {
    Cell* element = Cell_New(self, *iter);
    if (!element) goto error;
    if (PyList_SetItem(list, index, cast_PyObj(element)) < 0)
      goto error;
  }
  return list;

error:
  Py_DECREF(list);
  return NULL;
}

class UniqueEdges{
public:
  std::map< std::tuple<int,int>, CGAL_AlphaShape3::Edge > edges;
  UniqueEdges(void){};
  std::tuple<int,int> sortedKey(int e0,int e1){
    if(e0<e1) return std::make_tuple(e0,e1);
    else return std::make_tuple(e1,e0);
  }
  void append(int e0,int e1,CGAL_AlphaShape3::Edge edge){
    std::tuple<int,int> k = sortedKey(e0,e1);
    auto e = edges.find(k);
    if( e == edges.end() ){
      edges.insert( std::make_pair(k,edge) );
    }
  }
};

class UniqueFacets{
public:
  std::map< std::tuple<int,int,int>, CGAL_AlphaShape3::Facet > facets;
  UniqueFacets(void){};
  std::tuple<int,int,int> sortedKey(int f0,int f1,int f2){
    if(f0<f1)
      if(f1<f2) return std::make_tuple(f0,f1,f2);
      else
        if(f0<f2) return std::make_tuple(f0,f2,f1);
        else return std::make_tuple(f2,f0,f1);
    else
      if(f0<f2) return std::make_tuple(f1,f0,f2);
      else
        if(f1<f2) return std::make_tuple(f1,f2,f0);
        else return std::make_tuple(f2,f1,f0);
  }
  void append(int f0,int f1,int f2,CGAL_AlphaShape3::Facet facet){
    std::tuple<int,int,int> k = sortedKey(f0,f1,f2);
    auto f = facets.find(k);
    if( f == facets.end() ){
      facets.insert( std::make_pair(k,facet) );
    }
  }
};

static PyObject* PeriodicAlphaShape3_edges(PeriodicAlphaShape3* self) {
  // Unique Cell を incident に持っていて、かつ重複しないものを登録する
  UniqueEdges uniqueEdges;
  for (
    auto iter = self->unique_cells.begin();
    iter != self->unique_cells.end();
    ++iter)
  {
    CGAL_AlphaShape3::Cell_handle cell = *iter;
    CGAL_AlphaShape3::Edge edge01 = CGAL_AlphaShape3::Edge(cell,0,1);
    CGAL_AlphaShape3::Edge edge02 = CGAL_AlphaShape3::Edge(cell,0,2);
    CGAL_AlphaShape3::Edge edge03 = CGAL_AlphaShape3::Edge(cell,0,3);
    CGAL_AlphaShape3::Edge edge12 = CGAL_AlphaShape3::Edge(cell,1,2);
    CGAL_AlphaShape3::Edge edge13 = CGAL_AlphaShape3::Edge(cell,1,3);
    CGAL_AlphaShape3::Edge edge23 = CGAL_AlphaShape3::Edge(cell,2,3);
    int v0 = cell->vertex(0)->base->vertex_index;
    int v1 = cell->vertex(1)->base->vertex_index;
    int v2 = cell->vertex(2)->base->vertex_index;
    int v3 = cell->vertex(3)->base->vertex_index;
    uniqueEdges.append( v0,v1,edge01 );
    uniqueEdges.append( v0,v2,edge02 );
    uniqueEdges.append( v0,v3,edge03 );
    uniqueEdges.append( v1,v2,edge12 );
    uniqueEdges.append( v1,v3,edge13 );
    uniqueEdges.append( v2,v3,edge23 );
  }
  size_t num_edges = self->alpha_shape_->number_of_edges();
  if( num_edges != uniqueEdges.edges.size() ){
    PyErr_SetString(PyExc_ValueError, "Duplicated edges.");
    return NULL;
  }

  int index = 0;
  PyObject* list = PyList_New(uniqueEdges.edges.size());
  if (!list) return NULL;

  for(
    auto miter = uniqueEdges.edges.begin();
    miter != uniqueEdges.edges.end();
    ++miter)
  {
    Edge* element = Edge_New(self, miter->second);
    if (!element) goto error;
    if (PyList_SetItem(list, index, cast_PyObj(element)) < 0)
      goto error;
    ++index;
  }

  return list;

error:
  Py_DECREF(list);
  return NULL;
}

static PyObject* PeriodicAlphaShape3_facets(PeriodicAlphaShape3* self) {
  // Unique Cell を incident に持っていて、かつ重複しないものを登録する
  UniqueFacets uniqueFacets;
  for (auto iter = self->unique_cells.begin();
    iter != self->unique_cells.end();
    ++iter)
  {
    CGAL_AlphaShape3::Cell_handle cell = *iter;
    CGAL_AlphaShape3::Facet facet0 = std::make_pair(cell,0);
    CGAL_AlphaShape3::Facet facet1 = std::make_pair(cell,1);
    CGAL_AlphaShape3::Facet facet2 = std::make_pair(cell,2);
    CGAL_AlphaShape3::Facet facet3 = std::make_pair(cell,3);
    int f0 = cell->vertex(0)->base->vertex_index;
    int f1 = cell->vertex(1)->base->vertex_index;
    int f2 = cell->vertex(2)->base->vertex_index;
    int f3 = cell->vertex(3)->base->vertex_index;
    uniqueFacets.append( f0,f1,f2,facet3 );
    uniqueFacets.append( f1,f2,f3,facet0 );
    uniqueFacets.append( f2,f3,f0,facet1 );
    uniqueFacets.append( f3,f0,f1,facet2 );
  }

  size_t num_facets = self->alpha_shape_->number_of_facets();
  if( num_facets != uniqueFacets.facets.size() ){
    PyErr_SetString(PyExc_ValueError, "Duplicated faces.");
    return NULL;
  }

  int index = 0;
  PyObject* list = PyList_New(uniqueFacets.facets.size());
  if (!list) return NULL;

  for(
    auto miter = uniqueFacets.facets.begin();
    miter != uniqueFacets.facets.end();
    ++miter)
  {
    Facet* element = Facet_New(self,miter->second);
    if (!element) goto error;
    if (PyList_SetItem(list, index, cast_PyObj(element)) < 0)
      goto error;
    ++index;
  }

  return list;

error:
  Py_DECREF(list);
  return NULL;
}

static PyObject* PeriodicAlphaShape3_dump_vtk(PeriodicAlphaShape3* self,PyObject* args){
  const char* filename;
  if( !PyArg_ParseTuple(args, "s", &filename) ){
    return NULL;
  }
  int numCells = self->alpha_shape_->number_of_stored_cells();
  int numFacets = self->alpha_shape_->number_of_stored_facets();
  int numEdges = self->alpha_shape_->number_of_stored_edges();
  int numVertices = self->alpha_shape_->number_of_stored_vertices();
  std::ofstream output(filename, std::ios_base::out);
  output << "# vtk DataFile Version 3.0" << std::endl;
  output << "Periodic Alpha Shape 3D Dump File by HomCloud" << std::endl;
  output << "ASCII" << std::endl;
  output << "DATASET UNSTRUCTURED_GRID" << std::endl;
  output << "POINTS " << numVertices << " double" << std::endl;
  std::map<CGAL_AlphaShape3::Vertex_handle, int> index_of_vertex;
  int index=0;
  for( CGAL_AlphaShape3::Vertex_iterator it = self->alpha_shape_->vertices_begin(); it != self->alpha_shape_->vertices_end(); ++it )
  {
    output << self->alpha_shape_->point(it).point() << std::endl;
    index_of_vertex[it] = index;
    ++index;
  }
  int numSimplices = numCells + numFacets + numEdges + numVertices;
  int numIndices = 5*numCells + 4*numFacets + 3*numEdges + 2*numVertices;
  output << "CELLS" << " " << numSimplices << " " << numIndices << std::endl;
  for( CGAL_AlphaShape3::Cell_iterator c=self->alpha_shape_->cells_begin();
      c!=self->alpha_shape_->cells_end();
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
  for( CGAL_AlphaShape3::Facet_iterator f=self->alpha_shape_->facets_begin();
      f!=self->alpha_shape_->facets_end();
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
  for( CGAL_AlphaShape3::Edge_iterator e=self->alpha_shape_->edges_begin();
      e!=self->alpha_shape_->edges_end();
      ++e)
  {
    CGAL_AlphaShape3::Vertex_handle v0 = e->first->vertex(e->second);
    CGAL_AlphaShape3::Vertex_handle v1 = e->first->vertex(e->third);
    int i0 = index_of_vertex[v0];
    int i1 = index_of_vertex[v1];
    output << 2 << " " << i0 << " " << i1 << std::endl;
  }
  for( CGAL_AlphaShape3::Vertex_iterator v = self->alpha_shape_->vertices_begin();
      v != self->alpha_shape_->vertices_end();
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
    output << "SCALARS offset int 3" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( CGAL_AlphaShape3::Vertex_iterator it = self->alpha_shape_->vertices_begin(); it != self->alpha_shape_->vertices_end(); ++it )
    {
      CGAL_AlphaShape3::Periodic_point pp = self->alpha_shape_->periodic_point(it);
      output << pp.second.x() << " " << pp.second.y() << " " << pp.second.z() << std::endl;
    }
  }
  {
    output << "SCALARS base int 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( CGAL_AlphaShape3::Vertex_iterator it = self->alpha_shape_->vertices_begin(); it != self->alpha_shape_->vertices_end(); ++it )
    {
      output << index_of_vertex[it->base] << std::endl;
    }
  }
  {
    output << "SCALARS degree int 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( CGAL_AlphaShape3::Vertex_iterator it = self->alpha_shape_->vertices_begin(); it != self->alpha_shape_->vertices_end(); ++it )
    {
      output << self->alpha_shape_->degree(it) << std::endl;
    }
  }
  {
    output << "SCALARS weight double 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( CGAL_AlphaShape3::Vertex_iterator it = self->alpha_shape_->vertices_begin(); it != self->alpha_shape_->vertices_end(); ++it )
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
    output << "SCALARS original int 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( CGAL_AlphaShape3::Cell_iterator c=self->alpha_shape_->cells_begin();
        c!=self->alpha_shape_->cells_end();
        ++c)
    {
      if( isUniqueCell(self->alpha_shape_,c) ){
        output << 1 << std::endl;
      }else{
        output << 0 << std::endl;
      }
    }
    for(int i=0;i<numFacets;++i){
      output << 0 << std::endl;
    }
    for(int i=0;i<numEdges;++i){
      output << 0 << std::endl;
    }
    for(int i=0;i<numVertices;++i){
      output << 0 << std::endl;
    }
  }
  {
    output << "SCALARS alpha double 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( CGAL_AlphaShape3::Cell_iterator c=self->alpha_shape_->cells_begin();
        c!=self->alpha_shape_->cells_end();
        ++c)
    {
      output << c->get_alpha() << std::endl;
    }
    for( CGAL_AlphaShape3::Facet_iterator f=self->alpha_shape_->facets_begin();
        f!=self->alpha_shape_->facets_end();
        ++f)
    {
      output << BirthRadius(self->alpha_shape_->get_alpha_status(*f)) << std::endl;
    }
    for( CGAL_AlphaShape3::Edge_iterator e=self->alpha_shape_->edges_begin();
        e!=self->alpha_shape_->edges_end();
        ++e)
    {
      P3T3::Point p1 = self->alpha_shape_->point(e->first->vertex(e->second));
      P3T3::Point p2 = self->alpha_shape_->point(e->first->vertex(e->third));
      double a = 0.25 * CGAL::squared_distance(p1,p2);
      output << a << std::endl;
    }
    for( CGAL_AlphaShape3::Vertex_iterator v = self->alpha_shape_->vertices_begin();
        v != self->alpha_shape_->vertices_end();
        ++v )
    {
      output << -(v->point().weight()) << std::endl;
    }
  }
  {
    output << "SCALARS alpha2 double 1" << std::endl;
    output << "LOOKUP_TABLE default" << std::endl;
    for( CGAL_AlphaShape3::Cell_iterator c=self->alpha_shape_->cells_begin();
        c!=self->alpha_shape_->cells_end();
        ++c)
    {
      output << AlphaValueCell(self->alpha_shape_,c) << std::endl;
    }
    for( CGAL_AlphaShape3::Facet_iterator f=self->alpha_shape_->facets_begin();
        f!=self->alpha_shape_->facets_end();
        ++f)
    {
      output << AlphaValueFacet(self->alpha_shape_,f) << std::endl;
    }
    for( CGAL_AlphaShape3::Edge_iterator e=self->alpha_shape_->edges_begin();
        e!=self->alpha_shape_->edges_end();
        ++e)
    {
      CGAL_AlphaShape3::Edge edge(e->first,e->second,e->third);
      output << AlphaValueEdge(self->alpha_shape_,&edge) << std::endl;
    }
    for( CGAL_AlphaShape3::Vertex_iterator v = self->alpha_shape_->vertices_begin();
        v != self->alpha_shape_->vertices_end();
        ++v )
    {
      output << -(v->point().weight()) << std::endl;
    }
  }
  output.close();
  return Py_BuildValue("i",0);
}

static PyMethodDef PeriodicAlphaShape3_methods[] = {
  {"num_vertices",
   (PyCFunction)PeriodicAlphaShape3_num_vertices, METH_NOARGS,
   "Return the number of vertices"},
  {"vertices",
   (PyCFunction)PeriodicAlphaShape3_vertices, METH_NOARGS,
   "Return vertices"},
  {"cells",
   (PyCFunction)PeriodicAlphaShape3_cells, METH_NOARGS,
   "Return cells"},
  {"edges",
   (PyCFunction)PeriodicAlphaShape3_edges, METH_NOARGS,
   "Return edges"},
  {"facets",
   (PyCFunction)PeriodicAlphaShape3_facets, METH_NOARGS,
   "Return facets"},
  // for debug
  {"dump_vtk",
   (PyCFunction)PeriodicAlphaShape3_dump_vtk, METH_VARARGS,
   "Save as a vtk format"},
  {NULL, NULL, 0 ,NULL}
};

static PyTypeObject PeriodicAlphaShape3Type = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.periodic_alpha_shape3.PeriodicAlphaShape3", // tp_name
  sizeof(PeriodicAlphaShape3), // tp_basicsize 
  0, // tp_itemsize
  (destructor)PeriodicAlphaShape3_dealloc, // tp_dealloc
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
  "3D Periodic Alpha Shape",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  PeriodicAlphaShape3_methods,   // tp_methods 
  0, // tp_members
  0, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(PeriodicAlphaShape3_init), // tp_init 
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 

/////////////// Vertex ///////////////////////////


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

static PyMethodDef Vertex_methods[] = {
  {"vertices", (PyCFunction)Vertex_vertices, METH_NOARGS,
   "Return the tuple whose element is self"},
  {"point", (PyCFunction)Vertex_point, METH_NOARGS,
   "Return the coordinate of the vertex"},
  {"weight", (PyCFunction)Vertex_weight, METH_NOARGS,
   "Return the weight of the vertex"},
  {"isvertex", (PyCFunction)method_return_true, METH_NOARGS, "Return True"},
  {NULL, NULL, 0 ,NULL}
};

static PyMemberDef Vertex_members[] = {
  {"vertex_index", T_INT, offsetof(Vertex, vertex_index_), READONLY,
   "The unique index of the vertex"},
  {"group_name", T_INT, offsetof(Vertex, group_name_), READONLY,
   "Group name of the vertex"},
  {"birth_radius", T_DOUBLE, offsetof(Vertex, birth_radius_), 0,
   "Birth radius of the vertex"},
  {NULL, 0, 0, 0, NULL}
};

static PyTypeObject VertexType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.periodic_alpha_shape3.Vertex", // tp_name 
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
  "Vertex class for PeriodicAlphaShape3",  // tp_doc
  (traverseproc)Vertex_traverse, // tp_traverse
  (inquiry)Vertex_clear, // tp_clear
  Vertex_compare, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Vertex_methods, // tp_methods 
  Vertex_members, // tp_members 
};

static Vertex* Vertex_New(PeriodicAlphaShape3* alpha,
                          CGAL_AlphaShape3::Vertex_handle handle) {
  Vertex* vertex = PyObject_GC_New(Vertex, &VertexType);

  if (!vertex) return NULL;

  vertex->alpha_ = alpha;
  vertex->handle_ = handle;
  vertex->vertex_index_ = handle->vertex_index;
  vertex->group_name_ = handle->group_name;
  vertex->birth_radius_ = -(handle->point().weight());
  Py_INCREF(alpha);
  PyObject_GC_Track(vertex);

  return vertex;
}

static bool Vertex_equal(PyObject* o1, PyObject* o2) {
  if (!PyObject_TypeCheck(o1, &VertexType) || !PyObject_TypeCheck(o1, &VertexType))
    return false;
  Vertex* v1 = reinterpret_cast<Vertex*>(o1);
  Vertex* v2 = reinterpret_cast<Vertex*>(o2);
  return v1->alpha_ == v2->alpha_ && v1->handle_ == v2->handle_;
}

/////////////// Cell ///////////////////////////

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
    Vertex* vertex = Vertex_New(self->alpha_, v_handle->base);
    if (!vertex) goto error;
    PyTuple_SET_ITEM(vertices, i, cast_PyObj(vertex));
  }
  return vertices;
  
error:
  Py_DECREF(vertices);
  return NULL;
}

static PyMethodDef Cell_methods[] = {
  {"vertices",
   (PyCFunction)Cell_vertices, METH_NOARGS,
   "Return vertices of the cell"},
  {"isvertex", (PyCFunction)method_return_false, METH_NOARGS, "Return False"},
  {NULL, NULL, 0 ,NULL}
};

static PyMemberDef Cell_members[] = {
  {"birth_radius", T_DOUBLE, offsetof(Cell, birth_radius_), 0,
   "Birth radius of the cell"},
  {NULL, 0, 0, 0, NULL}
};

static PyTypeObject CellType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.periodic_alpha_shape3.Cell", // tp_name 
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
  "Cell class for PeriodicAlphaShape3",  // tp_doc
  (traverseproc)Cell_traverse, // tp_traverse
  (inquiry)Cell_clear, // tp_clear
  Cell_compare, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Cell_methods, // tp_methods 
  Cell_members, // tp_members 
};

static Cell* Cell_New(PeriodicAlphaShape3* alpha, CGAL_AlphaShape3::Cell_handle handle) {
  Cell* cell = PyObject_GC_New(Cell, &CellType);
  if (!cell) return NULL;

  cell->alpha_ = alpha;
  cell->handle_ = handle;
  cell->birth_radius_ = AlphaValueCell(alpha->alpha_shape_,handle);
  Py_INCREF(alpha);
  PyObject_GC_Track(cell);

  return cell;
}

static bool Cell_equal(PyObject* o1, PyObject* o2) {
  if (!PyObject_TypeCheck(o1, &CellType) || !PyObject_TypeCheck(o1, &CellType))
    return false;
  Cell* c1 = reinterpret_cast<Cell*>(o1);
  Cell* c2 = reinterpret_cast<Cell*>(o2);
  return c1->alpha_ == c2->alpha_ && c1->handle_ == c2->handle_;
}

/////////////// Edge ///////////////////////////

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

static PyObject* Edge_vertices(Edge* self) {
  Vertex* v1 = NULL;
  Vertex* v2 = NULL;

  v1 = Vertex_New(self->alpha_, self->v1->base);
  if (!v1) goto error;
  v2 = Vertex_New(self->alpha_, self->v2->base);
  if (!v2) goto error;

  return Py_BuildValue("NN", v1, v2);

error:
  Py_XDECREF(v1);
  Py_XDECREF(v2);
  return NULL;
}

static PyMethodDef Edge_methods[] = {
  {"vertices", (PyCFunction)Edge_vertices, METH_NOARGS,
   "Return endpoint vertices of the edge"},
  {"isvertex", (PyCFunction)method_return_false, METH_NOARGS, "Return False"},
  {NULL, NULL, 0 ,NULL}
};

static PyMemberDef Edge_members[] = {
  {"birth_radius", T_DOUBLE, offsetof(Edge, birth_radius_), 0,
   "Birth radius of the edge"},
  {NULL, 0, 0, 0, NULL}
};

static PyTypeObject EdgeType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.periodic_alpha_shape3.Edge", // tp_name 
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
  "Edge class for PeriodicAlphaShape3", // tp_doc
  (traverseproc)Edge_traverse, // tp_traverse
  (inquiry)Edge_clear, // tp_clear
  0, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Edge_methods, // tp_methods 
  Edge_members, // tp_members 
};

static Edge* Edge_New(PeriodicAlphaShape3* alpha,
                      CGAL_AlphaShape3::Edge &e) {
  Edge* edge = PyObject_GC_New(Edge, &EdgeType);
  if (!edge) return NULL;

  // e.first : Cell_handle
  // e.second : int (0,1,2,3)
  // e.thrid : int (0,1,2,3)
  edge->alpha_ = alpha;
  edge->v1 = e.first->vertex(e.second);
  edge->v2 = e.first->vertex(e.third);
  edge->birth_radius_ = AlphaValueEdge(alpha->alpha_shape_,&e);

  Py_INCREF(alpha);
  PyObject_GC_Track(edge);

  return edge;
}

/////////////// Facet ///////////////////////////


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

static PyObject* Facet_vertices(Facet* self) {
  PyObject* vertices = PyTuple_New(3);
  if (!vertices) return NULL;

  for (int i=0; i<3; ++i) {
    CGAL_AlphaShape3::Vertex_handle v_handle = self->cell_->vertex((self->v_+i+1) % 4);
    Vertex* vertex = Vertex_New(self->alpha_, v_handle->base);
    if (!vertex) goto error;
    PyTuple_SET_ITEM(vertices, i, cast_PyObj(vertex));
  }
  return vertices;

error:
  Py_DECREF(vertices);
  return NULL;
}

static PyMethodDef Facet_methods[] = {
  {"vertices", (PyCFunction)Facet_vertices, METH_NOARGS,
   "Return endpoint vertices of the edge"},
  {"isvertex", (PyCFunction)method_return_false, METH_NOARGS, "Return False"},
  {NULL, NULL, 0 ,NULL}
};

static PyMemberDef Facet_members[] = {
  {"birth_radius", T_DOUBLE, offsetof(Facet, birth_radius_), 0,
   "Birth radius of the edge"},
  {NULL, 0, 0, 0, NULL}
};

static PyTypeObject FacetType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.periodic_alpha_shape3.Facet", // tp_name 
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
  "Facet class for PeriodicAlphaShape3", // tp_doc
  (traverseproc)Facet_traverse, // tp_traverse
  (inquiry)Facet_clear, // tp_clear
  0, // tp_richcompare 
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  Facet_methods, // tp_methods 
  Facet_members, // tp_members 
};

static Facet* Facet_New(PeriodicAlphaShape3* alpha,
                        CGAL_AlphaShape3::Facet &f) {
  Facet* facet = PyObject_GC_New(Facet, &FacetType);
  if (!facet) return NULL;

  facet->alpha_ = alpha;
  facet->cell_ = f.first;
  facet->v_ = f.second;
  facet->birth_radius_ = AlphaValueFacet(alpha->alpha_shape_,&f);
  Py_INCREF(alpha);
  PyObject_GC_Track(facet);

  return facet;
}

/////////////// Module ///////////////////////////

static PyModuleDef periodic_alpha_shape3_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.periodic_alpha_shape3",
  "The module for 3D Periodic Alpha shape",
  -1,
};

PyMODINIT_FUNC
PyInit_periodic_alpha_shape3()
{
  if (PyType_Ready(&PeriodicAlphaShape3Type) < 0)
    return NULL;
  if (PyType_Ready(&VertexType) < 0)
    return NULL;
  if (PyType_Ready(&CellType) < 0)
    return NULL;
  if (PyType_Ready(&EdgeType) < 0)
    return NULL;
  if (PyType_Ready(&FacetType) < 0)
    return NULL;

  PyObject* module = PyModule_Create(&periodic_alpha_shape3_Module);

  if (!module)
    return NULL;

  Py_INCREF(&PeriodicAlphaShape3Type);
  PyModule_AddObject(module, "PeriodicAlphaShape3", cast_PyObj(&PeriodicAlphaShape3Type));
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
