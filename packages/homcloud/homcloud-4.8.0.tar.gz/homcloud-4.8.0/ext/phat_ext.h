// -*- mode: c++ -*-
#ifndef HOMCLOUD_PHAT_EXT_H
#define HOMCLOUD_PHAT_EXT_H

#include <phat/boundary_matrix.h>
#include <phat/representations/bit_tree_pivot_column.h>
#include <phat/algorithms/twist_reduction.h>
#ifdef HOMCLOUD_OPENMP
#include <phat/algorithms/chunk_reduction.h>
#endif
#include <msgpack.hpp>
#include <iostream>
#include <numeric>
#include <cassert>
#include <bitset>

namespace phat_ext {

struct Matrix {
  PyObject_HEAD

  using PhatMatrix = phat::boundary_matrix<phat::bit_tree_pivot_column>;

  PhatMatrix* matrix_;
  msgpack::sbuffer* boundary_map_buf_;
  msgpack::packer<msgpack::sbuffer>* bmap_packer_;

  void SetUp(int num_cols, std::string dstyle="none") {
    matrix_ = new PhatMatrix();
    matrix_->set_num_cols(num_cols);
    if (dstyle == "none") {
      boundary_map_buf_ = nullptr;
      bmap_packer_ = nullptr;
    } else {
      boundary_map_buf_ = new msgpack::sbuffer();
      bmap_packer_ = new msgpack::packer<msgpack::sbuffer>(boundary_map_buf_);
      bmap_packer_->pack_map(3);
      bmap_packer_->pack(std::string("chunktype"));
      bmap_packer_->pack(std::string("boundary_map"));
      bmap_packer_->pack(std::string("type"));
      bmap_packer_->pack(dstyle);
      bmap_packer_->pack(std::string("map"));
      bmap_packer_->pack_array(num_cols);
    }
  }

  void TearDown() {
    delete matrix_; matrix_ = nullptr;
    delete bmap_packer_; bmap_packer_ = nullptr;
    delete boundary_map_buf_; boundary_map_buf_ = nullptr;
  }

  void SetBoundaryMap(phat::dimension dim, const phat::column& col) {
    if (!bmap_packer_)
      return;

    bmap_packer_->pack_array(2);
    bmap_packer_->pack<int>(dim);
    bmap_packer_->pack_array(col.size());
    for (phat::index element: col)
      bmap_packer_->pack(element);
  }

  void SetDimCol(phat::index idx, phat::dimension dim, phat::column* col) {
    SetBoundaryMap(dim, *col);
    matrix_->set_dim(idx, dim);
    std::sort(col->begin(), col->end());
    matrix_->set_col(idx, *col);
  }

  void ReduceTwist() {
    phat::twist_reduction()(*matrix_);
  }

#ifdef HOMCLOUD_OPENMP
  void ReduceChunk() {
    phat::chunk_reduction()(*matrix_);
  }
#endif
  
  template<typename PairEncoder>
  void Pairs(PairEncoder* encoder) {
    std::vector<bool> free(matrix_->get_num_cols(), true);
    
    for (phat::index idx = 0; idx < matrix_->get_num_cols(); ++idx) {
      if (!matrix_->is_empty(idx)) {
        phat::index birth = matrix_->get_max_index(idx);
        phat::index death = idx;
        encoder->AddPair(matrix_->get_dim(idx) - 1, birth, death);
        free[birth] = free[death] = false;
      }
    }

    for (phat::index idx = 0; idx < matrix_->get_num_cols(); ++idx) {
      if (free[idx]) {
        encoder->AddEssentialPair(matrix_->get_dim(idx), idx);
      }  
    }

  }
}; // class Matrix

#ifdef HOMCLOUD_PHAT_EXT_MODULE
static void** API;

static int import() {
  PyImport_ImportModule("homcloud.phat_ext");
  API = (void**)PyCapsule_Import("homcloud.phat_ext._C_API", 0);
  return API ? 0 : -1;
}

static PyTypeObject* MatrixType() {
  return reinterpret_cast<PyTypeObject*>(API[0]);
}

static Matrix* MatrixNew(int num_cols, std::string dstyle) {
  Matrix* matrix = PyObject_New(Matrix, MatrixType());
  if (!matrix) return nullptr;
  matrix->SetUp(num_cols, dstyle);

  return matrix;
}
#endif

} // namespace phat_ext

#endif // HOMCLOUD_PHAT_EXT_H
