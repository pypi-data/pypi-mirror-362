#ifndef HOMCCUBE3_CUBEMAP_HPP
#define HOMCCUBE3_CUBEMAP_HPP

#include <vector>

namespace homccube {

template<int d, typename T, typename Policy>
struct CubeMap {
  static const int dim = d;
  using Shape = typename Policy::Shape;
  template<int dim> using Coord = typename Policy::template Coord<dim>;
  template<int dim> using Cube = typename Policy::template Cube<dim>;

  CubeMap(const Shape& shape, T init):
      shape_(shape), data_(shape.template num_cubes<dim>(), init) {}
  CubeMap(const Shape& shape):
      shape_(shape), data_(shape.template num_cubes<dim>()) {}

  T& operator[](Coord<d> c) { return data_[shape_.index(c)]; }
  const T& operator[](Coord<d> c) const { return data_[shape_.index(c)]; }
  T& operator[](Cube<d> cube) { return data_[shape_.index(cube.c_)]; }
  const T& operator[](Cube<d> cube) const { return data_[shape_.index(cube.c_)]; }

  const Shape& shape_;
  std::vector<T> data_;
};

} // namespace homccube

#endif
