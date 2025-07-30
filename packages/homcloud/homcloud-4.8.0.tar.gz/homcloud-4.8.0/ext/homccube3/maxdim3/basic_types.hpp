#ifndef HOMCCUBE3_MAXDIM3_BASIC_TYPES_HPP
#define HOMCCUBE3_MAXDIM3_BASIC_TYPES_HPP

#include <cstdint>
#include <array>
#include <cassert>
#include <functional>
#include <algorithm>
#include <bitset>

namespace homccube { namespace maxdim3 {

using Level = std::uint32_t;
using Order = std::uint64_t;
using CoordID = std::uint32_t;
using Index = std::uint32_t;
using Periodicity = std::bitset<3>;

const Level INFINITE_LEVEL = 0xffffffffu;
const Level INVALID_LEVEL = 0xfffffffeu;

const CoordID ROOT = 0xffffffffu;

bool valid_shape(const std::vector<int>& shape) {
  return shape.size() == 3 &&
      (shape[0] < 1022) &&
      (shape[1] < 1022) &&
      (shape[2] < 1022);
}

// m:
//   dim 0: 0
//   dim 1: 0 X
//          1 Y
//          2 Z
//   dim 2: 0 Y-Z
//          1 Z-X
//          2 X-Y
//   dim 3: 0
template<int d>
struct Coord {
  static const int dim = d;

  union {
    struct {
      unsigned int m_:2;
      unsigned int x_:10;
      unsigned int y_:10;
      unsigned int z_:10;
    };
    CoordID coord_id_;
  };

  Coord(){}
  Coord(unsigned m, unsigned x, unsigned y, unsigned z): m_(m), x_(x), y_(y), z_(z) {}
  explicit Coord(CoordID id): coord_id_(id) {}
  
  friend std::ostream& operator<<(std::ostream& os, const Coord& coord) {
    os << "Coord<" << dim << ">[" << coord.m_ << ": "
       << coord.x_ << ", " << coord.y_ << ", " << coord.z_ << "]";
    return os;
  }

  friend bool operator==(const Coord& x, const Coord& y) {
    return x.coord_id_ == y.coord_id_;
  }
};

template<int d>
struct Cube {
  static const int dim = d;

  union {
    struct {
      Coord<dim> c_;
      Level level_;
    };
    Order order_;
  };

  Cube(const Coord<dim> c, Level level): c_(c), level_(level) {}
  Cube(unsigned m, unsigned x, unsigned y, unsigned z, unsigned level):
      c_(Coord<dim>(m, x, y, z)), level_(level) {}

  static Cube invalid_cube() {
    return Cube(0, 0, 0, 0, INVALID_LEVEL);
  }

  bool invalid() const { return level_ == INVALID_LEVEL; }
  bool valid() const { return level_ != INVALID_LEVEL; }

  friend bool operator<(const Cube u, const Cube v) {
    return u.order_ < v.order_;
  }
  friend bool operator==(const Cube u, const Cube v) {
    return u.order_ == v.order_;
  }

  friend std::ostream& operator<<(std::ostream& os, const Cube cube) {
    os << "Cube<" << dim << ">[" << cube.c_.m_ << ": " 
       << cube.c_.x_ << ", " << cube.c_.y_ << ", " << cube.c_.z_ 
       << ": " << cube.level_ << "]";
    return os;
  }
};

struct Shape {
  Shape(const std::vector<int>& shape) {
    assert(shape.size() == 3);
    std::copy(shape.begin(), shape.end(), data_.begin());
    num_pixels_ = shape[0] * shape[1] * shape[2];
    shape12_ = shape[1] * shape[2];
  }
  Shape(const std::vector<int>& shape, Periodicity p): Shape(shape) {
    assert(p.none());
  }
  
  size_t num_pixels() const { return num_pixels_; }
  template<int d> 
  size_t num_cubes() const {
    switch (d) {
      case 0:
      case 3:
        return num_pixels_;
      case 1:
      case 2:
        return 3 * num_pixels_;
      default:
        assert(false);
    }
  }

  template<int dim>
  Index index(const Coord<dim> coord) const {
    return coord.m_ * num_pixels_ + coord.x_ * shape12_ + coord.y_ * data_[2] + coord.z_;
  }
  template<int dim>
  Index index0(const Coord<dim> coord) const {
    return coord.x_ * shape12_ + coord.y_ * data_[2] + coord.z_;
  }

  template<int dim>
  Index index0(const Coord<dim> coord, int dx, int dy, int dz) const {
    return (coord.x_ + dx) * shape12_ + (coord.y_ + dy) * data_[2] + (coord.z_ + dz);
  }

  unsigned int operator[](int n) const { return data_[n]; }


  template<int dim, typename F> struct ForeachCoface;

  template<typename F>
  struct ForeachCoface<1, F> {
    void operator()(const Shape& shape, Coord<1> c, F func) {
      switch (c.m_) {
        case 0:
          if (c.z_ != shape[2] - 1)
            func(Coord<2>(1, c.x_, c.y_, c.z_));
          if (c.z_ != 0)
            func(Coord<2>(1, c.x_, c.y_, c.z_ - 1));
          if (c.y_ != shape[1] - 1)
            func(Coord<2>(2, c.x_, c.y_, c.z_));
          if (c.y_ != 0)
            func(Coord<2>(2, c.x_, c.y_ - 1, c.z_));
          break;
        case 1:
          if (c.x_ != shape[0] - 1)
            func(Coord<2>(2, c.x_, c.y_, c.z_));
          if (c.x_ != 0)
            func(Coord<2>(2, c.x_ - 1, c.y_, c.z_));
          if (c.z_ != shape[2] - 1)
            func(Coord<2>(0, c.x_, c.y_, c.z_));
          if (c.z_ != 0)
            func(Coord<2>(0, c.x_, c.y_, c.z_ - 1));
          break;
        case 2:
          if (c.y_ != shape[1] - 1)
            func(Coord<2>(0, c.x_, c.y_, c.z_));
          if (c.y_ != 0)
            func(Coord<2>(0, c.x_, c.y_ - 1, c.z_));
          if (c.x_ != shape[0] - 1)
            func(Coord<2>(1, c.x_, c.y_, c.z_));
          if (c.x_ != 0)
            func(Coord<2>(1, c.x_ - 1, c.y_, c.z_));
          break;
        default:
          assert(false);
      }
    }
  };

  template<typename F>
  struct ForeachCoface<2, F> {
    void operator()(const Shape& shape, Coord<2> c, F func) {
      switch (c.m_) {
        case 0:
          if (c.x_ != shape[0] - 1)
            func(Coord<3>(0, c.x_, c.y_, c.z_));
          if (c.x_ != 0)
            func(Coord<3>(0, c.x_ - 1, c.y_, c.z_));
          break;
        case 1:
          if (c.y_ != shape[1] - 1)
            func(Coord<3>(0, c.x_, c.y_, c.z_));
          if (c.y_ != 0)
            func(Coord<3>(0, c.x_, c.y_ - 1, c.z_));
          break;
        case 2:
          if (c.z_ != shape[2] - 1)
            func(Coord<3>(0, c.x_, c.y_, c.z_));
          if (c.z_ != 0)
            func(Coord<3>(0, c.x_, c.y_, c.z_ - 1));
          break;
        default:
          assert(false);
      }

    }
  };

  template<int dim, typename F>
  void foreach_coface(const Coord<dim> coord, F func) const {
    ForeachCoface<dim, F>()(*this, coord, func);
  }

  template<int d, typename F>
  struct ForeachCoords {
    void operator()(const Shape& shape, F func) {}
  };

  template<typename F>
  struct ForeachCoords<1, F> {
    void operator()(const Shape& shape, F func) {
      for (unsigned int x = 0; x < shape[0]; ++x)
        for (unsigned int y = 0; y < shape[1]; ++y)
          for (unsigned int z = 0; z < shape[2]; ++z) {
            if (x != shape[0] - 1)
              func(Coord<1>(0, x, y, z));
            if (y != shape[1] - 1)
              func(Coord<1>(1, x, y, z));
            if (z != shape[2] - 1)
              func(Coord<1>(2, x, y, z));
          }
    }
  };

  template<typename F>
  struct ForeachCoords<2, F> {
    void operator()(const Shape& shape, F func) {
      for (unsigned int x = 0; x < shape[0]; ++x)
        for (unsigned int y = 0; y < shape[1]; ++y)
          for (unsigned int z = 0; z < shape[2]; ++z) {
            if (y != shape[1] - 1 && z != shape[2] - 1)
              func(Coord<2>(0, x, y, z));
            if (z != shape[2] - 1 && x != shape[0] - 1)
              func(Coord<2>(1, x, y, z));
            if (x != shape[0] - 1 && y != shape[1] - 1)
              func(Coord<2>(2, x, y, z));
          }
    }
  };
  
  template<int d, typename F>
  void foreach_coords(F func) const {
    ForeachCoords<d, F>()(*this, func);
  }


  template<typename Bitmap, int d> struct GetLevel;

  template<typename Bitmap>
  struct GetLevel<Bitmap, 0> {
    Level operator()(const Shape& shape, const Bitmap& bitmap, Coord<0> coord) {
      return bitmap.levels_[shape.index0(coord)];
    }
  };

  template<typename Bitmap>
  struct GetLevel<Bitmap, 1> {
    Level operator()(const Shape& shape, const Bitmap& bitmap, Coord<1> coord) {
      switch (coord.m_) {
        case 0:
          return std::max(bitmap.levels_[shape.index0(coord)],
                          bitmap.levels_[shape.index0(coord, 1, 0, 0)]);
        case 1:
          return std::max(bitmap.levels_[shape.index0(coord)],
                          bitmap.levels_[shape.index0(coord, 0, 1, 0)]);
        case 2:
          return std::max(bitmap.levels_[shape.index0(coord)],
                          bitmap.levels_[shape.index0(coord, 0, 0, 1)]);
        default:
          assert(false);
          return 0; // To prevent a warning
      }
    }
  };

  template<typename Bitmap>
  struct GetLevel<Bitmap, 2> {
    Level operator()(const Shape& shape, const Bitmap& bitmap, Coord<2> coord) {
      switch (coord.m_) {
        case 0: // Y-Z
          return std::max({bitmap.levels_[shape.index0(coord)],
                           bitmap.levels_[shape.index0(coord, 0, 1, 0)],
                           bitmap.levels_[shape.index0(coord, 0, 0, 1)],
                           bitmap.levels_[shape.index0(coord, 0, 1, 1)]});
        case 1: // X-Z
          return std::max({bitmap.levels_[shape.index0(coord)],
                           bitmap.levels_[shape.index0(coord, 1, 0, 0)],
                           bitmap.levels_[shape.index0(coord, 0, 0, 1)],
                           bitmap.levels_[shape.index0(coord, 1, 0, 1)]});
        case 2: // X-Y
          return std::max({bitmap.levels_[shape.index0(coord)],
                           bitmap.levels_[shape.index0(coord, 1, 0, 0)],
                           bitmap.levels_[shape.index0(coord, 0, 1, 0)],
                           bitmap.levels_[shape.index0(coord, 1, 1, 0)]});
        default:
          assert(false);
          return 0; // To prevent a warning
      }
    }
  };

  template<typename Bitmap>
  struct GetLevel<Bitmap, 3> {
    Level operator()(const Shape& shape, const Bitmap& bitmap, Coord<3> coord) {
      return std::max({bitmap.levels_[shape.index0(coord)],
                       bitmap.levels_[shape.index0(coord, 1, 0, 0)],
                       bitmap.levels_[shape.index0(coord, 0, 1, 0)],
                       bitmap.levels_[shape.index0(coord, 0, 0, 1)],
                       bitmap.levels_[shape.index0(coord, 1, 1, 0)],
                       bitmap.levels_[shape.index0(coord, 0, 1, 1)],
                       bitmap.levels_[shape.index0(coord, 1, 0, 1)],
                       bitmap.levels_[shape.index0(coord, 1, 1, 1)],});
    }
  };
  
  template<typename Bitmap, int d>
  Level get_level(const Bitmap& bitmap, Coord<d> coord) const {
    return GetLevel<Bitmap, d>()(*this, bitmap, coord);
  }

  void vertices(const Cube<1> edge, Index& x, Index& y) const {
    Index index = index0(edge.c_);
    x = index;
    switch (edge.c_.m_) {
      case 0:
        y = index + shape12_;
        return;
      case 1:
        y = index + data_[2];
        return;
      case 2:
        y = index + 1;
        return;
      default:
        assert(false);
    }
  }
  
  std::array<unsigned int, 3> data_;
  size_t num_pixels_, shape12_;
};


struct Policy3D {
  using Level = homccube::maxdim3::Level;
  using Order = homccube::maxdim3::Order;
  using CoordID = homccube::maxdim3::CoordID;
  using Index = homccube::maxdim3::Index;
  template<int dim> using Coord = homccube::maxdim3::Coord<dim>;
  template<int dim> using Cube = homccube::maxdim3::Cube<dim>;
  using Shape = homccube::maxdim3::Shape;

  static const Level INFINITE_LEVEL = homccube::maxdim3::INFINITE_LEVEL;
  static const Level INVALID_LEVEL = homccube::maxdim3::INVALID_LEVEL;
  static const CoordID ROOT = homccube::maxdim3::ROOT;

  using Periodicity = homccube::maxdim3::Periodicity;
  static const bool PERIODIC = false;
};


struct PeriodicShape {
  PeriodicShape(const std::vector<int>& shape, Periodicity periodicity) {
    assert(shape.size() == 3);
    std::copy(shape.begin(), shape.end(), data_.begin());
    periodicity_ = periodicity;
    num_pixels_ = shape[0] * shape[1] * shape[2];
    shape12_ = shape[1] * shape[2];
  }
  
  size_t num_pixels() const { return num_pixels_; }
  template<int d> 
  size_t num_cubes() const {
    switch (d) {
      case 0:
      case 3:
        return num_pixels_;
      case 1:
      case 2:
        return 3 * num_pixels_;
      default:
        assert(false);
    }
  }

  bool lower_bound_ok(unsigned int k, size_t select) const {
    return k > 0 || periodicity_[select];
  }

  bool upper_bound_ok(unsigned int k, size_t select) const {
    return k < data_[select] - 1 || periodicity_[select];
  }

  unsigned int minus_1_mod(unsigned int x, size_t select) const {
    return (x + data_[select] - 1) % data_[select];
  }

  template<int dim>
  Index index(const Coord<dim> coord) const {
    return coord.m_ * num_pixels_ + coord.x_ * shape12_ + coord.y_ * data_[2] + coord.z_;
  }
  template<int dim>
  Index index0(const Coord<dim> coord) const {
    return coord.x_ * shape12_ + coord.y_ * data_[2] + coord.z_;
  }

  template<int dim>
  Index index0(const Coord<dim> coord, int dx, int dy, int dz) const {
    return ((coord.x_ + dx) % data_[0]) * shape12_ +
        ((coord.y_ + dy) % data_[1]) * data_[2] +
        ((coord.z_ + dz) % data_[2]);
  }

  unsigned int operator[](int n) const { return data_[n]; }


  template<int dim, typename F> struct ForeachCoface;

  template<typename F>
  struct ForeachCoface<1, F> {
    void operator()(const PeriodicShape& shape, Coord<1> c, F func) {
      switch (c.m_) {
        case 0:
          if (shape.upper_bound_ok(c.z_, 2))
            func(Coord<2>(1, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.z_, 2))
            func(Coord<2>(1, c.x_, c.y_, shape.minus_1_mod(c.z_, 2)));
          if (shape.upper_bound_ok(c.y_, 1))
            func(Coord<2>(2, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.y_, 1))
            func(Coord<2>(2, c.x_, shape.minus_1_mod(c.y_, 1), c.z_));
          break;
        case 1:
          if (shape.upper_bound_ok(c.x_, 0))
            func(Coord<2>(2, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.x_, 0))
            func(Coord<2>(2, shape.minus_1_mod(c.x_, 0), c.y_, c.z_));
          if (shape.upper_bound_ok(c.z_, 2))
            func(Coord<2>(0, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.z_, 2))
            func(Coord<2>(0, c.x_, c.y_, shape.minus_1_mod(c.z_, 2)));
          break;
        case 2:
          if (shape.upper_bound_ok(c.y_, 1))
            func(Coord<2>(0, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.y_, 1))
            func(Coord<2>(0, c.x_, shape.minus_1_mod(c.y_, 1), c.z_));
          if (shape.upper_bound_ok(c.x_, 0))
            func(Coord<2>(1, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.x_, 0))
            func(Coord<2>(1, shape.minus_1_mod(c.x_, 0), c.y_, c.z_));
          break;
        default:
          assert(false);
      }
    }
  };

  template<typename F>
  struct ForeachCoface<2, F> {
    void operator()(const PeriodicShape& shape, Coord<2> c, F func) {
      switch (c.m_) {
        case 0:
          if (shape.upper_bound_ok(c.x_, 0))
            func(Coord<3>(0, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.x_, 0))
            func(Coord<3>(0, shape.minus_1_mod(c.x_, 0), c.y_, c.z_));
          break;
        case 1:
          if (shape.upper_bound_ok(c.y_, 1))
            func(Coord<3>(0, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.y_, 1))
            func(Coord<3>(0, c.x_, shape.minus_1_mod(c.y_, 1), c.z_));
          break;
        case 2:
          if (shape.upper_bound_ok(c.z_, 2))
            func(Coord<3>(0, c.x_, c.y_, c.z_));
          if (shape.lower_bound_ok(c.z_, 2))
            func(Coord<3>(0, c.x_, c.y_, shape.minus_1_mod(c.z_, 2)));
          break;
        default:
          assert(false);
      }

    }
  };

  template<int dim, typename F>
  void foreach_coface(const Coord<dim> coord, F func) const {
    ForeachCoface<dim, F>()(*this, coord, func);
  }

  template<int d, typename F>
  struct ForeachCoords {
    void operator()(const PeriodicShape& shape, F func) {}
  };

  template<typename F>
  struct ForeachCoords<1, F> {
    void operator()(const PeriodicShape& shape, F func) {
      for (unsigned int x = 0; x < shape[0]; ++x)
        for (unsigned int y = 0; y < shape[1]; ++y)
          for (unsigned int z = 0; z < shape[2]; ++z) {
            if (shape.upper_bound_ok(x, 0))
              func(Coord<1>(0, x, y, z));
            if (shape.upper_bound_ok(y, 1))
              func(Coord<1>(1, x, y, z));
            if (shape.upper_bound_ok(z, 2))
              func(Coord<1>(2, x, y, z));
          }
    }
  };

  template<typename F>
  struct ForeachCoords<2, F> {
    void operator()(const PeriodicShape& shape, F func) {
      for (unsigned int x = 0; x < shape[0]; ++x)
        for (unsigned int y = 0; y < shape[1]; ++y)
          for (unsigned int z = 0; z < shape[2]; ++z) {
            bool x_ok = shape.upper_bound_ok(x, 0);
            bool y_ok = shape.upper_bound_ok(y, 1);
            bool z_ok = shape.upper_bound_ok(z, 2);
            if (y_ok && z_ok)
              func(Coord<2>(0, x, y, z));
            if (z_ok && x_ok)
              func(Coord<2>(1, x, y, z));
            if (x_ok && y_ok)
              func(Coord<2>(2, x, y, z));
          }
    }
  };

  template<typename F>
  struct ForeachCoords<3, F> {
    void operator()(const PeriodicShape& shape, F func) {
      for (unsigned int x = 0; x < shape[0]; ++x)
        for (unsigned int y = 0; y < shape[1]; ++y)
          for (unsigned int z = 0; z < shape[2]; ++z) {
            bool x_ok = shape.upper_bound_ok(x, 0);
            bool y_ok = shape.upper_bound_ok(y, 1);
            bool z_ok = shape.upper_bound_ok(z, 2);
            if (x_ok && y_ok && z_ok)
              func(Coord<3>(0, x, y, z));
          }
    }
  };
  
  template<int d, typename F>
  void foreach_coords(F func) const {
    ForeachCoords<d, F>()(*this, func);
  }


  template<typename Bitmap, int d> struct GetLevel;

  template<typename Bitmap>
  struct GetLevel<Bitmap, 0> {
    Level operator()(const PeriodicShape& shape, const Bitmap& bitmap, Coord<0> coord) {
      return bitmap.levels_[shape.index0(coord)];
    }
  };

  template<typename Bitmap>
  struct GetLevel<Bitmap, 1> {
    Level operator()(const PeriodicShape& shape, const Bitmap& bitmap, Coord<1> coord) {
      switch (coord.m_) {
        case 0:
          return std::max(bitmap.levels_[shape.index0(coord)],
                          bitmap.levels_[shape.index0(coord, 1, 0, 0)]);
        case 1:
          return std::max(bitmap.levels_[shape.index0(coord)],
                          bitmap.levels_[shape.index0(coord, 0, 1, 0)]);
        case 2:
          return std::max(bitmap.levels_[shape.index0(coord)],
                          bitmap.levels_[shape.index0(coord, 0, 0, 1)]);
        default:
          assert(false);
          return 0; // To prevent a warning
      }
    }
  };

  template<typename Bitmap>
  struct GetLevel<Bitmap, 2> {
    Level operator()(const PeriodicShape& shape, const Bitmap& bitmap, Coord<2> coord) {
      switch (coord.m_) {
        case 0: // Y-Z
          return std::max({bitmap.levels_[shape.index0(coord)],
                           bitmap.levels_[shape.index0(coord, 0, 1, 0)],
                           bitmap.levels_[shape.index0(coord, 0, 0, 1)],
                           bitmap.levels_[shape.index0(coord, 0, 1, 1)]});
        case 1: // X-Z
          return std::max({bitmap.levels_[shape.index0(coord)],
                           bitmap.levels_[shape.index0(coord, 1, 0, 0)],
                           bitmap.levels_[shape.index0(coord, 0, 0, 1)],
                           bitmap.levels_[shape.index0(coord, 1, 0, 1)]});
        case 2: // X-Y
          return std::max({bitmap.levels_[shape.index0(coord)],
                           bitmap.levels_[shape.index0(coord, 1, 0, 0)],
                           bitmap.levels_[shape.index0(coord, 0, 1, 0)],
                           bitmap.levels_[shape.index0(coord, 1, 1, 0)]});
        default:
          assert(false);
          return 0; // To prevent a warning
      }
    }
  };

  template<typename Bitmap>
  struct GetLevel<Bitmap, 3> {
    Level operator()(const PeriodicShape& shape, const Bitmap& bitmap, Coord<3> coord) {
      return std::max({bitmap.levels_[shape.index0(coord)],
                       bitmap.levels_[shape.index0(coord, 1, 0, 0)],
                       bitmap.levels_[shape.index0(coord, 0, 1, 0)],
                       bitmap.levels_[shape.index0(coord, 0, 0, 1)],
                       bitmap.levels_[shape.index0(coord, 1, 1, 0)],
                       bitmap.levels_[shape.index0(coord, 0, 1, 1)],
                       bitmap.levels_[shape.index0(coord, 1, 0, 1)],
                       bitmap.levels_[shape.index0(coord, 1, 1, 1)],});
    }
  };
  
  template<typename Bitmap, int d>
  Level get_level(const Bitmap& bitmap, Coord<d> coord) const {
    return GetLevel<Bitmap, d>()(*this, bitmap, coord);
  }

  void vertices(const Cube<1> edge, Index& x, Index& y) const {
    x = index0(edge.c_);
    switch (edge.c_.m_) {
      case 0:
        y = index0(edge.c_, 1, 0, 0);
        return;
      case 1:
        y = index0(edge.c_, 0, 1, 0);
        return;
      case 2:
        y = index0(edge.c_, 0, 0, 1);
        return;
      default:
        assert(false);
    }
  }
  
  std::array<unsigned int, 3> data_;
  Periodicity periodicity_;
  size_t num_pixels_, shape12_;
};


struct PolicyPeriodic3D {
  using Level = homccube::maxdim3::Level;
  using Order = homccube::maxdim3::Order;
  using CoordID = homccube::maxdim3::CoordID;
  using Index = homccube::maxdim3::Index;
  template<int dim> using Coord = homccube::maxdim3::Coord<dim>;
  template<int dim> using Cube = homccube::maxdim3::Cube<dim>;
  using Shape = homccube::maxdim3::PeriodicShape;

  static const Level INFINITE_LEVEL = homccube::maxdim3::INFINITE_LEVEL;
  static const Level INVALID_LEVEL = homccube::maxdim3::INVALID_LEVEL;
  static const CoordID ROOT = homccube::maxdim3::ROOT;

  using Periodicity = homccube::maxdim3::Periodicity;
  static const bool PERIODIC = true;
};

}} // namespae homccube::maxdim3

#endif
