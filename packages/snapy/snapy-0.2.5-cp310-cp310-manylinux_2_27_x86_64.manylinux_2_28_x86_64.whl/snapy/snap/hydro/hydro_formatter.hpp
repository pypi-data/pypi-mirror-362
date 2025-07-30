#pragma once

// snap
#include <snap/eos/eos_formatter.hpp>
#include <snap/recon/recon_formatter.hpp>
#include <snap/riemann/riemann_formatter.hpp>

#include "hydro.hpp"

template <>
struct fmt::formatter<snap::HydroOptions> {
  constexpr auto parse(fmt::format_parse_context& ctx) { return ctx.begin(); }

  template <typename FormatContext>
  auto format(const snap::HydroOptions& p, FormatContext& ctx) const {
    return fmt::format_to(ctx.out(),
                          "(eos = {}; riemann = {}; recon1 = {}; recon23 = {})",
                          p.eos(), p.riemann(), p.recon1(), p.recon23());
  }
};

template <>
struct fmt::formatter<snap::PrimitiveProjectorOptions> {
  constexpr auto parse(fmt::format_parse_context& ctx) { return ctx.begin(); }

  template <typename FormatContext>
  auto format(const snap::PrimitiveProjectorOptions& p,
              FormatContext& ctx) const {
    return fmt::format_to(ctx.out(),
                          "(type = {}; grav = {}; nghost = {}; margin = {})",
                          p.type(), p.grav(), p.nghost(), p.margin());
  }
};
