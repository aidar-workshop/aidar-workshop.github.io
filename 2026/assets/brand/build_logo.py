"""Emit the AIDaR letter-A: the Eiffel Tower drawn as a capital A.

The tower already is an A — splayed legs, a pointed apex, and a platform where
the crossbar goes. Setting it as the A of AIDaR means the next letter is the I
the word already has, so "AI" reads straight out of the Paris skyline, and one
tower carries the whole identity.

The proportions are the real tower's, widened horizontally so it holds the width
of a capital in the site's serif; a faithful 1:0.37 tower reads as a needle
beside Georgia. The curve of the legs, the base arch and the two platforms are
what make it recognisable, so those are kept exactly.

Run: python3 build_logo.py
"""

import math
from pathlib import Path

INK = "#202124"
TEAL = "#2f6f73"
TEAL_DEEP = "#26595c"
BRASS = "#a9762f"

CAP = 100.0            # cap height; everything else is expressed against it

# The real tower narrows to a needle by a third of its height. Held to that, it
# reads as a tower standing next to letters rather than as one of them. These
# anchors keep its curve, arch and platforms but taper gently enough to carry a
# capital's width — an A wearing the tower's details.
PROFILE = (
    (0.00, 0.360),
    (0.19, 0.284),   # first platform
    (0.42, 0.197),   # second platform, where the crossbar of an A sits
    (0.86, 0.074),
    (1.00, 0.020),
)
PLAT1_Y, PLAT2_Y = 0.19, 0.42

# Leg thickness, as a fraction of cap height: heavy enough to read as the
# diagonals of an A. Where the legs meet, the counter closes and the apex is solid.
LEG_BASE, LEG_TOP = 0.090, 0.034
COUNTER_TOP = 0.88

PAD_X = 4.0            # room for the platform bars, which overhang the legs


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def half_width(t):
    """Half-width at height fraction t, as a fraction of cap height.

    Interpolated exponentially between the profile anchors so the legs keep the
    inward curve of the real ones rather than reading as straight diagonals.
    """
    for (t0, w0), (t1, w1) in zip(PROFILE, PROFILE[1:]):
        if t <= t1:
            span = (t - t0) / (t1 - t0)
            return w0 * (w1 / w0) ** span
    return PROFILE[-1][1]


def leg_thickness(t):
    return LEG_BASE + (LEG_TOP - LEG_BASE) * min(t / COUNTER_TOP, 1.0)


def counter_top():
    """Height at which the legs meet and the counter closes to a point.

    Solved rather than guessed: a hardcoded value leaves either a gap at the
    apex or a counter that stops short.
    """
    lo, hi = 0.0, 1.0
    for _ in range(48):
        mid = (lo + hi) / 2
        if half_width(mid) - leg_thickness(mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo


def geometry(cx, baseline, cap):
    """Outer profile plus the counter, so the tower is an open lattice — which is
    both what an A needs and what the tower actually is."""
    def point(t, side, inner=False):
        w = half_width(t) - (leg_thickness(t) if inner else 0.0)
        return cx + side * max(w, 0.0) * cap, baseline - t * cap

    steps = 80
    left = [point(i / steps, -1) for i in range(steps + 1)]
    right = [point(i / steps, +1) for i in range(steps, -1, -1)]
    outline = "M" + " L".join(f"{fmt(x)},{fmt(y)}" for x, y in left + right) + " Z"

    # The counter: up the inside of the left leg, down the inside of the right,
    # closed along the bottom by the arch the tower is known for. It has to be a
    # single non-crossing loop or the fill rule closes the letter up solid.
    top = counter_top()
    inner_steps = 60
    ts = [top * i / inner_steps for i in range(inner_steps + 1)]
    left_inner = [point(t, -1, inner=True) for t in ts]            # bottom to top
    right_inner = [point(t, +1, inner=True) for t in reversed(ts)]  # top to bottom
    lx = left_inner[0][0]
    rx = right_inner[-1][0]
    # Open all the way to the ground: you see straight through the archway on the
    # real tower, and an A's legs splay open below its crossbar.
    counter = (
        "M"
        + " L".join(f"{fmt(x)},{fmt(y)}" for x, y in left_inner + right_inner)
        + " Z"
    )

    # The arch itself, as a band springing between the legs.
    arch_top = baseline - PLAT1_Y * cap * 0.86
    shoulder = cap * 0.07
    arch = (
        f"M{fmt(lx)},{fmt(baseline)}"
        f" C{fmt(lx)},{fmt(arch_top + shoulder)}"
        f" {fmt(cx - (cx - lx) * 0.42)},{fmt(arch_top)} {fmt(cx)},{fmt(arch_top)}"
        f" C{fmt(cx + (rx - cx) * 0.42)},{fmt(arch_top)}"
        f" {fmt(rx)},{fmt(arch_top + shoulder)} {fmt(rx)},{fmt(baseline)}"
    )

    bars = []
    for t, pad, weight in ((PLAT1_Y, 0.028, 0.026), (PLAT2_Y, 0.024, 0.023)):
        w = half_width(t) * cap + pad * cap
        y = baseline - t * cap
        h = weight * cap
        bars.append((cx - w, y - h / 2, w * 2, h))
    return outline + " " + counter, bars, arch


def build_letter_a(cap=CAP, scan=False):
    """The A on its own, tight to its bounding box, for inlining beside type."""
    width = (PROFILE[0][1] * cap + PAD_X) * 2
    cx = width / 2
    baseline = cap
    path, bars, arch = geometry(cx, baseline, cap)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(width)} '
        f'{fmt(cap)}" role="img" aria-label="A, drawn as the Eiffel Tower">',
    ]
    if scan:
        # A single scan band off the antenna: the only thing on the letter that
        # is not architecture, so it reads as transmission rather than filigree.
        tip = (cx, baseline - cap)
        for i, (a1, a2, op) in enumerate(
            ((-118.0, -96.0, 0.10), (-96.0, -74.0, 0.20), (-74.0, -52.0, 0.32))
        ):
            reach = cap * 0.9
            x1 = tip[0] + reach * math.cos(math.radians(a1))
            y1 = tip[1] + reach * math.sin(math.radians(a1))
            x2 = tip[0] + reach * math.cos(math.radians(a2))
            y2 = tip[1] + reach * math.sin(math.radians(a2))
            parts.append(
                f'  <path d="M{fmt(tip[0])},{fmt(tip[1])} L{fmt(x1)},{fmt(y1)} '
                f'L{fmt(x2)},{fmt(y2)} Z" fill="{TEAL}" opacity="{op}"/>'
            )
    parts.append(f'  <path d="{path}" fill="{INK}" fill-rule="evenodd"/>')
    parts.append(
        f'  <path d="{arch}" fill="none" stroke="{INK}" '
        f'stroke-width="{fmt(cap * 0.046)}"/>'
    )
    for x, y, w, h in bars:
        parts.append(
            f'  <rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" '
            f'height="{fmt(h)}" fill="{INK}"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def serif_i(x, baseline, cap, stem=0.115, serif=0.34, bar=0.028):
    """A capital I with slab serifs, to sit beside the drawn A."""
    sw = stem * cap
    fw = serif * cap
    bh = bar * cap
    top = baseline - cap
    return [
        f'  <rect x="{fmt(x - sw / 2)}" y="{fmt(top)}" width="{fmt(sw)}" '
        f'height="{fmt(cap)}" fill="{INK}"/>',
        f'  <rect x="{fmt(x - fw / 2)}" y="{fmt(top)}" width="{fmt(fw)}" '
        f'height="{fmt(bh)}" fill="{INK}"/>',
        f'  <rect x="{fmt(x - fw / 2)}" y="{fmt(baseline - bh)}" width="{fmt(fw)}" '
        f'height="{fmt(bh)}" fill="{INK}"/>',
    ]


def build_ai_monogram(size=200.0):
    """AI in a square: the tower as A, a drawn I beside it. Used as the favicon,
    where no webfont is available and the letters have to be geometry."""
    cap = size * 0.56
    baseline = size * 0.78
    a_cx = size * 0.395
    i_x = size * 0.70
    path, bars, arch = geometry(a_cx, baseline, cap)

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(size)} '
            f'{fmt(size)}" role="img" aria-label="AIDaR: A drawn as the Eiffel '
            'Tower, beside I">',
            f'  <rect width="{fmt(size)}" height="{fmt(size)}" rx="{fmt(size * 0.17)}" '
            'fill="#ffffff"/>',
            "  <defs>",
            f'    <clipPath id="sq"><rect width="{fmt(size)}" height="{fmt(size)}" '
            f'rx="{fmt(size * 0.17)}"/></clipPath>',
            "  </defs>",
            f'  <path d="{path}" fill="{INK}" fill-rule="evenodd"/>',
            f'  <path d="{arch}" fill="none" stroke="{INK}" '
            f'stroke-width="{fmt(cap * 0.046)}"/>',
            *[
                f'  <rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" '
                f'height="{fmt(h)}" fill="{INK}"/>'
                for x, y, w, h in bars
            ],
            *serif_i(i_x, baseline, cap),
            "</svg>",
        ]
    ) + "\n"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    repo_root = here.parents[2]
    (here / "aidar-a.svg").write_text(build_letter_a())
    (repo_root / "favicon.svg").write_text(build_ai_monogram())
    print(f"wrote {here / 'aidar-a.svg'}")
    print(f"wrote {repo_root / 'favicon.svg'}")
