#pragma once

#include <set>

namespace akida::hw {

enum class BasicType { none, HRC, CNP, FNP, SKIP_DMA, TNP_B, TNP_R, DMA };
enum class Type {
  none,
  HRC,
  CNP1,
  CNP2,
  FNP2,
  FNP3,
  SKIP_DMA_STORE,
  TNP_B,
  TNP_R,
  SKIP_DMA_LOAD,
  DMA
};

inline BasicType to_basic_type(Type type) {
  switch (type) {
    case Type::HRC:
      return BasicType::HRC;
    case Type::CNP1:
    case Type::CNP2:
      return BasicType::CNP;
    case Type::FNP2:
    case Type::FNP3:
      return BasicType::FNP;
    case Type::SKIP_DMA_STORE:
    case Type::SKIP_DMA_LOAD:
      return BasicType::SKIP_DMA;
    case Type::TNP_B:
      return BasicType::TNP_B;
    case Type::TNP_R:
      return BasicType::TNP_R;
    case Type::DMA:
      return BasicType::DMA;
    default:
      return BasicType::none;
  }
}

using Types = std::set<Type>;

}  // namespace akida::hw