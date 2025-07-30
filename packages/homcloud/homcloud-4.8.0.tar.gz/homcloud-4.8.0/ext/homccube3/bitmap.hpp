#ifndef HOMCCUBE3_BITMAP_HPP
#define HOMCCUBE3_BITMAP_HPP

#include "io.hpp"
#include <vector>
#include <numeric>
#include <algorithm>

namespace homccube {

template<typename Policy>
struct Bitmap {
  using Level = typename Policy::Level;
  using Index = typename Policy::Index;
  using Shape = typename Policy::Shape;
  using Periodicity = typename Policy::Periodicity;
  template<int dim> using Coord = typename Policy::template Coord<dim>;
  template<int dim> using Cube = typename Policy::template Cube<dim>;
  

  Bitmap(const std::vector<int>& shape): shape_(shape) {}
  Bitmap(const std::vector<int>& shape, Periodicity periodicity):
      shape_(shape, periodicity) {}

  void load(std::initializer_list<double> list) {
    assert(list.size() == shape_.num_pixels());
    values_.assign(list.begin(), list.end());
    update_levels();
  }

  void update_levels() {
    levels_.assign(shape_.num_pixels(), 0);
    level2value_.assign(shape_.num_pixels(), 0.0);

    std::vector<std::size_t> sorted_indices(shape_.num_pixels());
    
    std::iota(sorted_indices.begin(), sorted_indices.end(), 0);
    std::sort(sorted_indices.begin(), sorted_indices.end(),
              [this](std::size_t x, std::size_t y) {
                return values_[x] < values_[y];
              });
    for (std::size_t i = 0; i < shape_.num_pixels(); ++i)
      levels_[sorted_indices[i]] = i;

    for (std::size_t i = 0; i < shape_.num_pixels(); ++i)
      level2value_[i] = values_[sorted_indices[i]];
  }

  void load(std::istream* io) {
    for (std::size_t i = 0; i < shape_.num_pixels(); ++i)
      values_.push_back(binread<double>(io));
    update_levels();
  }

  double& value(const Coord<0> coord) {
    return values_[shape_.index0(coord)];
  }
  double value(const Coord<0> coord) const {
    return values_[shape_.index0(coord)];
  }
  Level& level(const Coord<0> coord) {
    return levels_[shape_.index0(coord)];
  }
  Level level(const Index index) const {
    return levels_[index];
  }
  template<int dim>
  Level level(const Coord<dim> coord) const {
    return shape_.get_level(*this, coord);
  }

  template<int d>
  Cube<d> coord2cube(const Coord<d> coord) const {
    return Cube<d>(coord, level(coord));
  }
  
  template<int d> std::vector<Cube<d>> cubes() const {
    std::vector<Cube<d>> ret;
    shape_.template foreach_coords<d>(
        [&ret, this](Coord<d> coord) {
          ret.push_back(coord2cube(coord));
        });
    
    return ret;
  }

  template<int d>
  std::vector<Cube<d + 1>> cofaces(Cube<d> cube) const {
    std::vector<Cube<d + 1>> ret;
    shape_.foreach_coface(cube.c_,
                          [&ret, this](Coord<d + 1> coord) {
                            ret.push_back(coord2cube(coord));
                          });
    return ret;
  }

  Shape shape_;
  std::vector<double> values_;
  std::vector<Level> levels_;
  std::vector<double> level2value_;
};


}

#endif
