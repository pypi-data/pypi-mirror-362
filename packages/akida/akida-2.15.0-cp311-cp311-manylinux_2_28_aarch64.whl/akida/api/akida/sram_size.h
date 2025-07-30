#pragma once

#include <cstdint>

#include "infra/exports.h"

namespace akida {
/**
 * Size of shared SRAM
 */
struct AKIDASHAREDLIB_EXPORT SramSize final {
  SramSize() = default;

  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator==(const SramSize& other) const {
    return input_bytes == other.input_bytes &&
           weight_bytes == other.weight_bytes;
  }

  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator!=(const SramSize& other) const { return !(*this == other); }

  /**
   * Size of shared input packet SRAM in bytes available inside the mesh
   * for each two NPs.
   */
  uint32_t input_bytes{};
  /**
   * Size of shared filter SRAM in bytes available inside the mesh for each two
   * NPs.
   */
  uint32_t weight_bytes{};
};
}  // namespace akida
