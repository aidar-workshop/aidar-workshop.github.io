"""Emit the AIDaR mark as SVG.

The Eiffel Tower stands at the centre of a radar plate and transmits the scan.
That pairing is not decorative: the tower was slated for dismantling in 1909 and
survived because it proved useful for radio telegraphy — it is an antenna that
happens to be a landmark. So the tower transmits, the fanned beam is the scan, and
the plotted returns are the data coming back.

Drawn as an engraved plate rather than a screen, to sit with the site's hairlines
and serif. Geometry is computed rather than hand-typed so the taper stays exact.

Run: python3 build_mark.py
"""

import math
from pathlib import Path

# --- tokens (all but BRASS are the site's existing custom properties) ---
INK = "#202124"
TEAL = "#2f6f73"
TEAL_DEEP = "#26595c"
LINE = "#d8dadd"
BRASS = "#a9762f"

CX = CY = 100.0
R_PLATE = 94.0
GROUND_Y = 160.0

# Tower, in units of its own height, from the real structure:
# first platform 57/330, second 115/330, top platform 276/330, spire to 330.
# Sized so the antenna sits below centre, leaving the upper plate as open sky
# for the scan to cross.
TOWER_H = 100.0
TIP_Y = GROUND_Y - TOWER_H
BASE_HALF = 0.185
PLAT1_Y, PLAT1_HALF = 0.173, 0.101
PLAT2_Y, PLAT2_HALF = 0.348, 0.058
TOP_Y, TOP_HALF = 0.836, 0.020
SPIRE_HALF = 0.007

# The beam fans up out of the antenna, into open sky rather than across the tower.
SWEEP_FROM, SWEEP_TO = -122.0, -48.0
SWEEP_BANDS = 7

# Returns as (bearing from the tip, radius, dot radius, colour). Irregular on
# purpose: real returns cluster and leave gaps. Any that fall outside the plate
# are dropped at build time with a warning rather than silently clipped.
RETURNS = (
    (-100.0, 34.0, 2.4, INK),
    (-78.0, 42.0, 3.2, BRASS),
    (-58.0, 44.0, 2.2, INK),
    (-38.0, 52.0, 2.6, INK),
    (-12.0, 62.0, 2.1, BRASS),
    (-128.0, 40.0, 2.3, INK),
    (-152.0, 50.0, 2.0, INK),
    (-172.0, 58.0, 2.6, INK),
)


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def polar(origin, bearing_deg, radius):
    rad = math.radians(bearing_deg)
    return origin[0] + radius * math.cos(rad), origin[1] + radius * math.sin(rad)


def half_width(t):
    """Half-width of the tower at height fraction t, as a fraction of height.

    Below the second platform the legs curve inward the way the real ones do;
    above it the taper is close to linear.
    """
    if t <= PLAT2_Y:
        # exponential through (0, BASE_HALF) and (PLAT2_Y, PLAT2_HALF)
        k = math.log(BASE_HALF / PLAT2_HALF) / PLAT2_Y
        return BASE_HALF * math.exp(-k * t)
    if t <= TOP_Y:
        span = (t - PLAT2_Y) / (TOP_Y - PLAT2_Y)
        return PLAT2_HALF + (TOP_HALF - PLAT2_HALF) * span
    span = (t - TOP_Y) / (1 - TOP_Y)
    return TOP_HALF + (SPIRE_HALF - TOP_HALF) * span


def tower_point(t, side):
    return CX + side * half_width(t) * TOWER_H, GROUND_Y - t * TOWER_H


def tower_silhouette():
    """Outer outline, with the base arch cut out so the legs read as legs."""
    steps = 64
    left = [tower_point(i / steps, -1) for i in range(steps + 1)]
    right = [tower_point(i / steps, +1) for i in range(steps, -1, -1)]
    pts = left + right
    outline = "M" + " L".join(f"{fmt(x)},{fmt(y)}" for x, y in pts) + " Z"

    # The arch: springs from just inside each leg and meets under platform one.
    arch_half = BASE_HALF * TOWER_H * 0.60
    arch_top = GROUND_Y - PLAT1_Y * TOWER_H * 0.92
    arch = (
        f"M{fmt(CX - arch_half)},{fmt(GROUND_Y)} "
        f"C{fmt(CX - arch_half)},{fmt(arch_top + 6)} "
        f"{fmt(CX - arch_half * 0.52)},{fmt(arch_top)} {fmt(CX)},{fmt(arch_top)} "
        f"C{fmt(CX + arch_half * 0.52)},{fmt(arch_top)} "
        f"{fmt(CX + arch_half)},{fmt(arch_top + 6)} "
        f"{fmt(CX + arch_half)},{fmt(GROUND_Y)} Z"
    )
    return outline + " " + arch


def platform_bars():
    out = []
    for t, pad in ((PLAT1_Y, 3.0), (PLAT2_Y, 2.2)):
        w = half_width(t) * TOWER_H + pad
        y = GROUND_Y - t * TOWER_H
        out.append(
            f'    <rect x="{fmt(CX - w)}" y="{fmt(y - 1.5)}" width="{fmt(w * 2)}" '
            f'height="3" fill="{INK}"/>'
        )
    return out


def sweep_bands():
    """Stepped screentone rather than a soft gradient — an engraving would hatch.

    Densest at the leading edge, fading back the way a phosphor trail decays.
    """
    out = []
    tip = (CX, TIP_Y)
    band = (SWEEP_TO - SWEEP_FROM) / SWEEP_BANDS
    reach = 240.0
    for i in range(SWEEP_BANDS):
        a1 = SWEEP_FROM + i * band
        x1, y1 = polar(tip, a1, reach)
        x2, y2 = polar(tip, a1 + band, reach)
        opacity = 0.07 + (i / (SWEEP_BANDS - 1)) ** 2 * 0.33
        out.append(
            f'    <path d="M{fmt(tip[0])},{fmt(tip[1])} L{fmt(x1)},{fmt(y1)} '
            f'L{fmt(x2)},{fmt(y2)} Z" fill="{TEAL}" opacity="{opacity:.3f}"/>'
        )
    ex, ey = polar(tip, SWEEP_TO, reach)
    out.append(
        f'    <line x1="{fmt(tip[0])}" y1="{fmt(tip[1])}" x2="{fmt(ex)}" '
        f'y2="{fmt(ey)}" stroke="{TEAL_DEEP}" stroke-width="1.8"/>'
    )
    return out


def returns():
    """Plotted returns, dropped loudly if they fall off the plate or underground."""
    out = []
    for bearing, r, dot, colour in RETURNS:
        x, y = polar((CX, TIP_Y), bearing, r)
        from_centre = math.hypot(x - CX, y - CY)
        if from_centre > R_PLATE - dot - 4 or y > GROUND_Y - dot - 2:
            print(f"  dropped return at bearing {bearing}, r={r}: outside the plate")
            continue
        out.append(
            f'    <circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(dot)}" fill="{colour}"/>'
        )
    return out


def build_mark():
    label = (
        "AIDaR mark: the Eiffel Tower, an antenna that survived demolition for "
        "radio telegraphy, transmitting a radar scan whose returns are plotted "
        "across the sky"
    )
    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" '
            f'role="img" aria-label="{label}">',
            "  <defs>",
            f'    <clipPath id="plate"><circle cx="{fmt(CX)}" cy="{fmt(CY)}" '
            f'r="{fmt(R_PLATE)}"/></clipPath>',
            "  </defs>",
            '  <g clip-path="url(#plate)">',
            "    <!-- the scan, transmitted from the antenna -->",
            *sweep_bands(),
            "    <!-- returns -->",
            *returns(),
            "    <!-- ground -->",
            f'    <line x1="0" y1="{fmt(GROUND_Y)}" x2="200" y2="{fmt(GROUND_Y)}" '
            f'stroke="{INK}" stroke-width="1"/>',
            "    <!-- the tower -->",
            f'    <path d="{tower_silhouette()}" fill="{INK}" fill-rule="evenodd"/>',
            *platform_bars(),
            "  </g>",
            "  <!-- horizon -->",
            f'  <circle cx="{fmt(CX)}" cy="{fmt(CY)}" r="{fmt(R_PLATE)}" fill="none" '
            f'stroke="{INK}" stroke-width="1.6"/>',
            "</svg>",
        ]
    ) + "\n"


def build_favicon():
    """Read at 16px: keep the plate and the tower, drop everything fine."""
    tip = (CX, TIP_Y)
    bands = []
    band = (SWEEP_TO - SWEEP_FROM) / 3
    for i in range(3):
        a1 = SWEEP_FROM + i * band
        x1, y1 = polar(tip, a1, 210)
        x2, y2 = polar(tip, a1 + band, 210)
        bands.append(
            f'    <path d="M{fmt(tip[0])},{fmt(tip[1])} L{fmt(x1)},{fmt(y1)} '
            f'L{fmt(x2)},{fmt(y2)} Z" fill="{TEAL}" opacity="{0.14 + i * 0.15:.2f}"/>'
        )
    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">',
            '  <rect width="200" height="200" rx="34" fill="#ffffff"/>',
            "  <defs>",
            f'    <clipPath id="f"><circle cx="{fmt(CX)}" cy="{fmt(CY)}" r="86"/>'
            "</clipPath>",
            "  </defs>",
            '  <g clip-path="url(#f)">',
            *bands,
            f'    <line x1="0" y1="{fmt(GROUND_Y)}" x2="200" y2="{fmt(GROUND_Y)}" '
            f'stroke="{INK}" stroke-width="6"/>',
            # Scaled up about its base: at 16px a faithful tower reads as a smudge.
            f'    <g transform="translate({fmt(CX)},{fmt(GROUND_Y)}) scale(1.22) '
            f'translate({fmt(-CX)},{fmt(-GROUND_Y)})">',
            f'      <path d="{tower_silhouette()}" fill="{INK}" fill-rule="evenodd"/>',
            *[b.replace("    <rect", "      <rect") for b in platform_bars()],
            "    </g>",
            "  </g>",
            f'  <circle cx="{fmt(CX)}" cy="{fmt(CY)}" r="86" fill="none" '
            f'stroke="{INK}" stroke-width="9"/>',
            "</svg>",
        ]
    ) + "\n"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    (here / "aidar-mark.svg").write_text(build_mark())
    # The favicon goes to the repo root so /favicon.svg resolves for both the
    # bare domain and the 2026 page.
    repo_root = here.parents[2]
    (repo_root / "favicon.svg").write_text(build_favicon())
    print(f"wrote {here / 'aidar-mark.svg'}")
    print(f"wrote {repo_root / 'favicon.svg'}")
