#ifndef HOMCCUBE3_PD_HPP
#define HOMCCUBE3_PD_HPP

#include <vector>
#include <fstream>
#include <cstdint>

#include "dipha_format.hpp"

namespace homccube {

template<typename Policy>
struct PD {
  using Level = typename Policy::Level;
  static const Level INFINITE_LEVEL = Policy::INFINITE_LEVEL;
  using Bitmap = homccube::Bitmap<Policy>;

  void add_pair(char degree, Level birth, Level death) {
    if (birth != death) {
      degrees_.push_back(degree);
      births_.push_back(birth);
      deaths_.push_back(death);
    }
  }

  void add_ess_pair(char degree, Level birth) {
    degrees_.push_back(degree);
    births_.push_back(birth);
    deaths_.push_back(static_cast<Level>(INFINITE_LEVEL));
  }

  void write_dipha_format(const Bitmap& bitmap, std::ostream* out) {
    namespace dipha = homccube::dipha;

    dipha::skip_diagram_header(out);

    std::uint64_t npairs = 0;

    for (std::size_t n = 0; n < size(); ++n) {
      if (deaths_[n] == INFINITE_LEVEL) {
        double birth = bitmap.level2value_[births_[n]];
        dipha::write_essential_pair(degrees_[n], birth, out);
        ++npairs;
      } else {
        double birth = bitmap.level2value_[births_[n]];
        double death = bitmap.level2value_[deaths_[n]];
        if (birth != death) {
          dipha::write_pair(degrees_[n], birth, death, out);
          ++npairs;
        }
      }
    }

    out->seekp(0, std::ios_base::beg);
    dipha::write_diagram_header(npairs, out);
  }

  std::size_t size() const { return births_.size(); }

  std::vector<Level> births_;
  std::vector<Level> deaths_;
  std::vector<char> degrees_;
};

}

#endif
