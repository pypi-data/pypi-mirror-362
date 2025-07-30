#ifndef HOMCCUBE3_LINK_FIND_HPP
#define HOMCCUBE3_LINK_FIND_HPP

#include <memory>

#include "bitmap.hpp"
#include "pd.hpp"

namespace homccube {

template<typename Policy>
struct LinkFind {
  using Level = typename Policy::Level;
  using CoordID = typename Policy::CoordID;
  using Shape = typename Policy::Shape;
  using Bitmap = homccube::Bitmap<Policy>;
  using PD = homccube::PD<Policy>;
  // template<int dim> using Coord = typename Policy::template Coord<dim>;
  template<int dim> using Cube = typename Policy::template Cube<dim>;

  static const CoordID ROOT = Policy::ROOT;

  LinkFind(const Bitmap& bitmap, PD* pd):
      bitmap_(bitmap), parents_(bitmap.shape_.num_pixels(), ROOT),
      pd_(pd), survivors_(std::make_shared<std::vector<Cube<1>>>())
  {
  }

  void compute() {
    pd_->add_ess_pair(0, 0);

    std::vector<Cube<1>> edges = bitmap_.template cubes<1>();
    std::sort(edges.begin(), edges.end());
    
    for (const Cube<1>& edge: edges) {
      CoordID x, y;
      bitmap_.shape_.vertices(edge, x, y);
      CoordID x_root = root(x);
      CoordID y_root = root(y);
      if (x_root == y_root) {
        set_root(x, x_root);
        set_root(y, x_root);
        survivors_->push_back(edge);
      } else {
        Level x_level = bitmap_.level(x_root);
        Level y_level = bitmap_.level(y_root);
        if (x_level > y_level) {
          pd_->add_pair(0, x_level, edge.level_);
          set_root(x, y_root);
          set_root(y, y_root);
        } else {
          pd_->add_pair(0, y_level, edge.level_);
          set_root(x, x_root);
          set_root(y, x_root);
        }
      }
    }
  }

  CoordID root(CoordID x) {
    for (;;) {
      CoordID parent = parents_[x];
      if (parent == ROOT) return x;
      x = parent;
    }
  }

  void set_root(CoordID x, CoordID root) {
    for (;;) {
      CoordID parent = parents_[x];
      if (parent == ROOT) break;
      parents_[x] = root;
      x = parent;
    }
    if (x != root)
      parents_[x] = root;
  }

  const Bitmap& bitmap_;
  std::vector<CoordID> parents_;
  PD* pd_;
  std::shared_ptr<std::vector<Cube<1>>> survivors_;
};

} // namespae homccube

#endif
