#pragma once

#include "akida/hardware_device.h"
#include "akida/ip_version.h"
#include "akida/np.h"
#include "akida/sram_size.h"

namespace akida {
/**
 * The default SRAM size for v1.
 *
 * Input SRAM: each NP has 2 input SRAM block of 5.25 x 1024 x 32-bit words.
 * Weight SRAM: each NP has a weight SRAM of 7 x 1024 x 50-bit words.
 */
inline constexpr SramSize SramSize_v1 = {43008, 44800};

/**
 * The default SRAM size for v2.
 *
 * Input SRAM: each NP has 2 input SRAM blocks of 8 x 1024 x 32-bit words.
 * Weight SRAM: each NP has a weight SRAM of 4 x 1024 x 100-bit words.
 */
inline constexpr SramSize SramSize_v2 = {65536, 51200};

/**
 * The layout of a mesh of Neural Processors.
 */
struct AKIDASHAREDLIB_EXPORT Mesh final {
  /**
   * Discover the topology of a Device Mesh.
   */
  static std::unique_ptr<Mesh> discover(HardwareDevice* device);

  explicit Mesh(IpVersion version, const hw::Ident& dma_event,
                const hw::Ident& dma_conf, bool has_hrc,
                std::vector<np::Info> nps,
                std::vector<np::Info> skip_dmas = {});

  bool has_lut_on_all_nps() const;

  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator==(const Mesh& other) const {
    return version == other.version && dma_event == other.dma_event &&
           dma_conf == other.dma_conf && has_hrc == other.has_hrc &&
           nps == other.nps && skip_dmas == other.skip_dmas &&
           np_sram_size == other.np_sram_size;
  }

  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator!=(const Mesh& other) const { return !(*this == other); }

  IpVersion version;               /**< The IP version of the mesh (v1 or v2) */
  hw::Ident dma_event;             /**< The DMA event endpoint */
  hw::Ident dma_conf;              /**< The DMA configuration endpoint */
  bool has_hrc;                    /**< If HRC is installed */
  std::vector<np::Info> nps;       /**< The available Neural Processors */
  std::vector<np::Info> skip_dmas; /**< The available skip dmas */
  /**
   * Size of shared SRAM in bytes available inside the mesh
   * for each two NPs.
   */
  SramSize np_sram_size{};
};

}  // namespace akida
