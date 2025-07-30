#ifndef HOMCCUBE3_IO_HPP
#define HOMCCUBE3_IO_HPP

#include <iostream>
#include <iterator>

namespace homccube {

template<typename T>
T binread(std::istream* io) {
  T d;
  io->read(reinterpret_cast<char *>(&d), sizeof(T));
  return d;
}

template<typename T>
void binwrite(T data, std::ostream* io) {
  io->write(reinterpret_cast<char *>(&data), sizeof(T));
}

} // namespace homccube

#endif 
