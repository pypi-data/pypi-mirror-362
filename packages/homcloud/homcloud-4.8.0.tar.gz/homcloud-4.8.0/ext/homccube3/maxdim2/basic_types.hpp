#ifndef HOMCCUBE3_MAXDIM2_BASIC_TYPES_HPP
#define HOMCCUBE3_MAXDIM2_BASIC_TYPES_HPP

#include <cstdint>
#include <array>
#include <cassert>
#include <functional>
#include <algorithm>
#include <bitset>

namespace homccube { namespace maxdim2 {

using Level = std::uint32_t;
using Order = std::uint64_t;
using CoordID = std::uint32_t;
using Index = std::uint32_t;
using Periodicity = std::bitset<2>;

const Level INFINITE_LEVEL = 0xffffffffu;
const Level INVALID_LEVEL = 0xfffffffeu;

const CoordID ROOT = 0xffffffffu;

bool valid_shape(const std::vector<int>& shape) {
  return shape.size() == 2 &&
      (shape[0] < 32766) &&
      (shape[1] < 65534);
}

// m:
// dim0, 2: 0
// dim1:
//   0: X
//   1: Y
template<int d>
struct Coord {
  static const int dim = d;

  union {
    struct {
      unsigned int m_:1;
      unsigned int x_: 15;
      unsigned int y_: 16;
    };
    CoordID coord_id_;
  };

  Coord(){}
  Coord(unsigned m, unsigned x, unsigned y): m_(m), x_(x), y_(y) {}
  explicit Coord(CoordID id): coord_id_(id) {}

  friend std::ostream& operator<<(std::ostream& os, const Coord& coord) {
    os << "Coord<" << dim << ">[" << coord.m_ << ": "
       << coord.x_ << ", " << coord.y_ << "]";
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
  Cube(unsigned m, unsigned x, unsigned y, unsigned level):
      c_(Coord<dim>(m, x, y)), level_(level) {}

  static Cube invalid_cube() {
    return Cube(0, 0, 0, INVALID_LEVEL);
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
       << cube.c_.x_ << ", " << cube.c_.y_ 
       << ": " << cube.level_ << "]";
    return os;
  }
};


struct Shape {
  Shape(const std::vector<int>& shape) {
    assert(shape.size() == 2);
    std::copy(shape.begin(), shape.end(), data_.begin());
    num_pixels_ = shape[0] * shape[1];
  }

  Shape(const std::vector<int>& shape, Periodicity p): Shape(shape) {
    assert(p.none());
  }

  size_t num_pixels() const { return num_pixels_; }

  template<int dim>
  size_t num_cubes() const  {
    switch (dim) {
      case 0:
      case 2:
        return num_pixels_;
      case 1:
        return 2 * num_pixels_;
      default:
        assert(false);
    }
  }

  template<int dim>
  Index index0(const Coord<dim> coord) const {
    return coord.x_ * data_[1] + coord.y_;
  }

  template<int dim>
  Index index0(const Coord<dim> coord, int dx, int dy) const {
    return (coord.x_ + dx) * data_[1] + coord.y_ + dy;
  }

  template<int dim>
  Index index(const Coord<dim> coord) const {
    return coord.m_ * num_pixels_ + coord.x_ * data_[1] + coord.y_;
  }

  unsigned int operator[](int n) const { return data_[n]; }

  void vertices(const Cube<1> edge, Index& x, Index& y) const {
    Index index = index0(edge.c_);
    x = index;
    switch (edge.c_.m_) {
      case 0:
        y = index + data_[1];
        return;
      case 1:
        y = index + 1;
        return;
      default:
        assert(false);
    }
  }

  template<typename F>
  void foreach_coface(const Coord<1> coord, F func) const {
    switch (coord.m_) {
      case 0:
        if (coord.y_ != data_[1] - 1)
          func(Coord<2>(0, coord.x_, coord.y_));
        if (coord.y_ != 0)
          func(Coord<2>(0, coord.x_, coord.y_ - 1));
        break;
      case 1:
        if (coord.x_ != data_[0] - 1)
          func(Coord<2>(0, coord.x_, coord.y_));
        if (coord.x_ != 0)
          func(Coord<2>(0, coord.x_ - 1, coord.y_));
        break;
      default:
        assert(false);
    }
  }

  template<int d, typename F>
  struct ForeachCoords {
    void operator()(const Shape& shape, F func) {}
  };

  template<typename F>
  struct ForeachCoords<1, F> {
    void operator()(const Shape& shape, F func) {
      for (unsigned int x = 0; x < shape[0]; ++x) {
        for (unsigned int y = 0; y < shape[1]; ++y) {
          if (x != shape[0] - 1)
            func(Coord<1>(0, x, y));
          if (y != shape[1] - 1)
            func(Coord<1>(1, x, y));
        }
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
                          bitmap.levels_[shape.index0(coord, 1, 0)]);
        case 1:
          return std::max(bitmap.levels_[shape.index0(coord)],
                          bitmap.levels_[shape.index0(coord, 0, 1)]);
        default:
          assert(false);
          return 0; // To prevent a warning
      }
    }
  };

  template<typename Bitmap>
  struct GetLevel<Bitmap, 2> {
    Level operator()(const Shape& shape, const Bitmap& bitmap, Coord<2> coord) {
      return std::max({bitmap.levels_[shape.index0(coord)],
                       bitmap.levels_[shape.index0(coord, 1, 0)],
                       bitmap.levels_[shape.index0(coord, 0, 1)],
                       bitmap.levels_[shape.index0(coord, 1, 1)]});
    }
  };
  
  template<typename Bitmap, int d>
  Level get_level(const Bitmap& bitmap, Coord<d> coord) const {
    return GetLevel<Bitmap, d>()(*this, bitmap, coord);
  }

  std::array<unsigned int, 2> data_;
  size_t num_pixels_;
};

struct Policy2D {
  using Level = homccube::maxdim2::Level;
  using Order = homccube::maxdim2::Order;
  using CoordID = homccube::maxdim2::CoordID;
  using Index = homccube::maxdim2::Index;
  template<int dim> using Coord = homccube::maxdim2::Coord<dim>;
  template<int dim> using Cube = homccube::maxdim2::Cube<dim>;
  using Shape = homccube::maxdim2::Shape;

  static const Level INFINITE_LEVEL = homccube::maxdim2::INFINITE_LEVEL;
  static const Level INVALID_LEVEL = homccube::maxdim2::INVALID_LEVEL;
  static const CoordID ROOT = homccube::maxdim2::ROOT;

  using Periodicity = std::bitset<2>;
  static const bool PERIODIC = false;
};


struct PeriodicShape {
  PeriodicShape(const std::vector<int>& shape, const Periodicity periodicity) {
    assert(shape.size() == 2);
    std::copy(shape.begin(), shape.end(), data_.begin());
    num_pixels_ = shape[0] * shape[1];
    periodicity_ = periodicity;
  }

  size_t num_pixels() const { return num_pixels_; }

  template<int dim>
  size_t num_cubes() const  {
    switch (dim) {
      case 0:
      case 2:
        return num_pixels_;
      case 1:
        return 2 * num_pixels_;
      default:
        assert(false);
    }
  }

  template<int dim>
  Index index0(const Coord<dim> coord) const {
    return coord.x_ * data_[1] + coord.y_;
  }

  template<int dim>
  Index index0(const Coord<dim> coord, int dx, int dy) const {
    return (((int)coord.x_ + dx) % data_[0]) * data_[1] + (((int)coord.y_ + dy) % data_[1]);
  }

  template<int dim>
  Index index(const Coord<dim> coord) const {
    return coord.m_ * num_pixels_ + coord.x_ * data_[1] + coord.y_;
  }

  unsigned int operator[](int n) const { return data_[n]; }

  void vertices(const Cube<1> edge, Index& x, Index& y) const {
    x = index0(edge.c_);
    switch (edge.c_.m_) {
      case 0:
        y = index0(Coord<0>(0, (edge.c_.x_ + 1) % data_[0], edge.c_.y_));
        return;
      case 1:
        y = index0(Coord<0>(0, edge.c_.x_, (edge.c_.y_ + 1) % data_[1]));
        return;
      default:
        assert(false);
    }
  }


  template<typename F>
  void foreach_coface(const Coord<1> coord, F func) const {
    switch (coord.m_) {
      case 0:
        if (coord.y_ != data_[1] - 1 || periodicity_[1])
          func(Coord<2>(0, coord.x_, coord.y_));
        if (coord.y_ != 0 || periodicity_[1])
          func(Coord<2>(0, coord.x_, (coord.y_ + data_[1] - 1) % data_[1]));
        break;
      case 1:
        if (coord.x_ != data_[0] - 1 || periodicity_[0])
          func(Coord<2>(0, coord.x_, coord.y_));
        if (coord.x_ != 0 || periodicity_[0])
          func(Coord<2>(0, (coord.x_ + data_[0] - 1) % data_[0], coord.y_));
        break;
      default:
        assert(false);
    }
  }


  template<int d, typename F>
  struct ForeachCoords {
    void operator()(const PeriodicShape& shape, F func) {}
  };

  template<typename F>
  struct ForeachCoords<1, F> {
    void operator()(const PeriodicShape& shape, F func) {
      for (unsigned int x = 0; x < shape[0]; ++x) {
        for (unsigned int y = 0; y < shape[1]; ++y) {
          if (x != shape[0] - 1 || shape.periodicity_[0])
            func(Coord<1>(0, x, y));
          if (y != shape[1] - 1 || shape.periodicity_[1])
            func(Coord<1>(1, x, y));
        }
      }
    }
  };

  template<typename F>
  struct ForeachCoords<2, F> {
    void operator()(const PeriodicShape& shape, F func) {
      for (unsigned int x = 0; x < shape[0]; ++x) {
        for (unsigned int y = 0; y < shape[1]; ++y) {
          if ((x != shape[0] - 1 || shape.periodicity_[0]) &&
              (y != shape[1] - 1 || shape.periodicity_[1]))
            func(Coord<2>(0, x, y));
        }
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
                          bitmap.levels_[shape.index0(coord, 1, 0)]);
        case 1:
          return std::max(bitmap.levels_[shape.index0(coord)],
                          bitmap.levels_[shape.index0(coord, 0, 1)]);
        default:
          assert(false);
          return 0; // To prevent a warning
      }
    }
  };

  template<typename Bitmap>
  struct GetLevel<Bitmap, 2> {
    Level operator()(const PeriodicShape& shape, const Bitmap& bitmap, Coord<2> coord) {
      return std::max({bitmap.levels_[shape.index0(coord)],
                       bitmap.levels_[shape.index0(coord, 1, 0)],
                       bitmap.levels_[shape.index0(coord, 0, 1)],
                       bitmap.levels_[shape.index0(coord, 1, 1)]});
    }
  };

  template<typename Bitmap, int d>
  Level get_level(const Bitmap& bitmap, Coord<d> coord) const {
    return GetLevel<Bitmap, d>()(*this, bitmap, coord);
  }

  std::array<unsigned int, 2> data_;
  Periodicity periodicity_;
  size_t num_pixels_;
};


struct PolicyPeriodic2D {
  using Level = homccube::maxdim2::Level;
  using Order = homccube::maxdim2::Order;
  using CoordID = homccube::maxdim2::CoordID;
  using Index = homccube::maxdim2::Index;
  template<int dim> using Coord = homccube::maxdim2::Coord<dim>;
  template<int dim> using Cube = homccube::maxdim2::Cube<dim>;
  using Shape = homccube::maxdim2::PeriodicShape;

  static const Level INFINITE_LEVEL = homccube::maxdim2::INFINITE_LEVEL;
  static const Level INVALID_LEVEL = homccube::maxdim2::INVALID_LEVEL;
  static const CoordID ROOT = homccube::maxdim2::ROOT;

  using Periodicity = std::bitset<2>;
  static const bool PERIODIC = true;
};

}} // namespace homccube::maxdim2

#endif

