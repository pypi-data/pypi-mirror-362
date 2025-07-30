#ifndef HOMCCUBE3_DIPHA_FORMAT_HPP
#define HOMCCUBE3_DIPHA_FORMAT_HPP

#include <iostream>
#include <numeric>
#include <cstdint>
#include "io.hpp"

namespace homccube { namespace dipha {

using std::uint64_t;
using std::int64_t;

bool read_header(std::istream* in) {
  uint64_t magic = binread<uint64_t>(in);
  uint64_t filetype = binread<uint64_t>(in);
  return magic == 8067171840 && filetype == 1;
}

std::vector<int> read_metadata(std::istream* in) {
  if (!read_header(in))
    throw std::runtime_error("Not a dipha bitmap file");

  uint64_t size = binread<uint64_t>(in);
  uint64_t ndim = binread<uint64_t>(in);
  std::vector<int> shape(ndim, 0);
  
  for (std::size_t k = 0; k < ndim; ++k)
    shape[ndim - k - 1] = binread<uint64_t>(in);

  uint64_t num_pixels = std::accumulate(shape.begin(), shape.end(), 1,
                                        std::multiplies<int>());
  
  if (num_pixels != size)
    throw std::runtime_error("File size inconsistent");

  return shape;
}

void skip_diagram_header(std::ostream* out) {
  for (int i = 0; i < 8 * 3; ++i)
    out->put(' ');
}

void write_diagram_header(uint64_t npairs, std::ostream* out) {
  binwrite<uint64_t>(8067171840ull, out);
  binwrite<uint64_t>(2, out);
  binwrite<uint64_t>(npairs, out);
}

void write_pair(uint64_t degree, double birth, double death, std::ostream* out) {
  binwrite<int64_t>(degree, out);
  binwrite<double>(birth, out);
  binwrite<double>(death, out);
}

void write_essential_pair(uint64_t degree, double birth, std::ostream* out) {
  binwrite<int64_t>(-degree - 1, out);
  binwrite<double>(birth, out);
  binwrite<double>(0.0, out);
}

} } // namespace homccube::dipha

#endif
