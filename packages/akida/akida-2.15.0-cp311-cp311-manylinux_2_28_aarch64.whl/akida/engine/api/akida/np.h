#pragma once
#include <vector>

#include "hardware_ident.h"
#include "hardware_type.h"

namespace akida::np {

constexpr bool is_cnp(hw::Type type) {
  return type == hw::Type::CNP1 || type == hw::Type::CNP2;
}

constexpr bool is_fnp(hw::Type type) {
  return type == hw::Type::FNP2 || type == hw::Type::FNP3;
}

struct Info {
  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator==(const Info& other) const {
    return ident == other.ident && types == other.types &&
           has_lut == other.has_lut;
  }

  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator!=(const Info& other) const { return !(*this == other); }

  hw::Ident ident;
  hw::Types types;
  bool has_lut;
};
}  // namespace akida::np
