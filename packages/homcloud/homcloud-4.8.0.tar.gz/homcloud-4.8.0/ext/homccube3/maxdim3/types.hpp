#ifndef HOMCCUBE3_MAXDIM3_TYPES_HPP
#define HOMCCUBE3_MAXDIM3_TYPES_HPP

#include "../bitmap.hpp"
#include "../pd.hpp"
#include "../cubemap.hpp"
#include "../link_find.hpp"
#include "../reducer.hpp"


#include "basic_types.hpp"

namespace homccube { namespace maxdim3 {

namespace types {
template <int d> using Cube = homccube::maxdim3::Cube<d>;
template <int d> using Coord = homccube::maxdim3::Coord<d>;
using Bitmap = homccube::Bitmap<Policy3D>;
using PD = homccube::PD<Policy3D>;
using LinkFind = homccube::LinkFind<Policy3D>;
template<int d, typename T> using CubeMap = homccube::CubeMap<d, T, Policy3D>;
template<int dim> using Reducer = homccube::Reducer<dim, Policy3D>;
}
}}

#endif
