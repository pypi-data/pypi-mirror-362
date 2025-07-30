#ifndef HOMCCUBE3_REDUCER_HPP
#define HOMCCUBE3_REDUCER_HPP

#include "bitmap.hpp"
#include "pd.hpp"
#include "cubemap.hpp"
#include "config.hpp"

#include <memory>
#include <boost/range/adaptor/reversed.hpp>

namespace homccube {

template<int d, typename Policy>
struct Reducer {
  static const int dim = d;
  using Level = typename Policy::Level;
  using CoordID = typename Policy::CoordID;
  using Shape = typename Policy::Shape;
  using Bitmap = homccube::Bitmap<Policy>;
  using PD = homccube::PD<Policy>;
  template<int dim, typename T>
  using CubeMap = homccube::CubeMap<dim, T, Policy>;
  template<int dim> using Coord = typename Policy::template Coord<dim>;
  template<int dim> using Cube = typename Policy::template Cube<dim>;

  using Config = homccube::Config;
  using LCube = Cube<dim>;
  using UCube = Cube<dim + 1>;

  struct Column {
    using Record = CubeMap<dim + 1, Cube<dim>>;
  
    Column(const Bitmap& bitmap, const LCube& cube):
        data_(bitmap.cofaces(cube)) {
      std::sort(data_.begin(), data_.end());
    }

    Column(std::vector<Cube<dim + 1>>&& data): data_(data) {}

    bool empty() const { return data_.empty(); }

    Cube<dim + 1> front() const { return data_.front(); }

    void add(const Column& other) {
      merge(other.data_);
    }

    void add_cofaces(const Bitmap& bitmap, const LCube& cube) {
      std::vector<Cube<dim + 1>> cofaces = bitmap.cofaces(cube);
      std::sort(cofaces.begin(), cofaces.end());
      merge(cofaces);
    }

    void merge(const std::vector<UCube>& other) {
      std::vector<Cube<dim + 1>> ret;
      std::size_t i = 0;
      std::size_t j = 0;

      while (i < data_.size() || j < other.size()) {
        if (i == data_.size()) {
          ret.push_back(other[j]);
          ++j;
          continue;
        }
        if (j == other.size()) {
          ret.push_back(data_[i]);
          ++i;
          continue;
        }

        UCube cube_i = data_[i];
        UCube cube_j = other[j];

        if (cube_i == cube_j) {
          i++; j++; continue;
        }
        if (cube_i < cube_j) {
          ret.push_back(cube_i); ++i;
        } else {
          ret.push_back(cube_j); ++j;
        }
      }
      data_.swap(ret);
    }

    UCube find_apparent(const LCube& cube, const Record& record) const {
      for (const UCube ucube: data_) {
        if (ucube.level_ != cube.level_)
          return UCube::invalid_cube();
        if (record[ucube].invalid())
          return ucube;
      }
      return UCube::invalid_cube();
    }

    friend std::ostream& operator<<(std::ostream& os, const Column& column) {
      os << "Column(";
      for (const auto cube: column.data_) 
        os << cube << ",";
      os << ")";
      return os;
    }

    std::vector<Cube<dim + 1>> data_;
  };

  
  Reducer(const Bitmap& bitmap,
          const std::vector<Cube<dim>>& lower_survivors,
          const Config& config,
          PD* pd): 
      bitmap_(bitmap), lower_survivors_(lower_survivors),
      config_(config), pd_(pd),
      record_(bitmap.shape_, LCube::invalid_cube()),
      survival_cubes_(bitmap.shape_, true),
      cache_(bitmap.shape_) {}
  

  void compute() {
    using boost::adaptors::reverse;

    for (const LCube& cube: reverse(lower_survivors_)) {
      reduce(cube);
    }
  }

  void reduce(LCube cube) {
    Column column(bitmap_, cube);

    if (config_.check_apparent_) {
      UCube apparent_cube = column.find_apparent(cube, record_);
      if (apparent_cube.valid()) {
        record_[apparent_cube] = cube;
        survival_cubes_[apparent_cube] = false;
        return;
      }
    }

    for (int n = 0;; n++) {
      if (column.empty()) {
        pd_->add_ess_pair(d, cube.level_);
        return;
      }

      LCube pivot = record_[column.front()];

      if (pivot.invalid()) {
        record_[column.front()] = cube;
        survival_cubes_[column.front()] = false;
        pd_->add_pair(dim, cube.level_, column.front().level_);
        if (n >= config_.cache_threshold_)
          set_cache(cube, column);
        return;
      }

      if (cache_[pivot]) {
        column.add(*cache_[pivot]);
      } else {
        column.add_cofaces(bitmap_, pivot);
      }
    }
  }

  void set_cache(const Cube<dim>& cube, Column& column) {
    cache_[cube].reset(new Column(std::move(column)));
  }

  std::shared_ptr<std::vector<UCube>> upper_survivors() const {
    auto ret = std::make_shared<std::vector<UCube>>();
    for (const auto ucube: bitmap_.template cubes<dim + 1>()) {
      if (survival_cubes_[ucube]) {
        ret->push_back(ucube);
      }
    }
    std::sort(ret->begin(), ret->end());

    return ret;
  }

  const Bitmap& bitmap_;
  const std::vector<Cube<dim>>& lower_survivors_;
  const Config config_;
  PD* pd_;
  CubeMap<dim + 1, Cube<dim>> record_;
  CubeMap<dim + 1, char> survival_cubes_;
  CubeMap<dim, std::unique_ptr<Column>> cache_;
};


} // namespace homccube::maxdim3

#endif
