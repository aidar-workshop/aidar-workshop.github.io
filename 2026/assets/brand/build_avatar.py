"""Emit the square forms of the wordmark: the Page logo and the favicon.

The cover carries the title and the date and no mark at all, so the square is
where the identity lives — which means it should be the wordmark itself rather
than a companion to it. A stranger landing on the Page needs to know whose it
is, and an abstract mark does not tell them.

  lockup   >= 48px   LinkedIn Page logo, iOS touch icon — the tower, the name,
                     and the rule beneath
  tower    <= 32px   favicon — the wordmark reduced to the one glyph that is
                     unmistakably ours; the name is unreadable at 16px and the
                     browser tab prints the page title beside it anyway

This replaces a knowledge-graph mark. The graph was a good answer to a question
that no longer exists: it was drawn so the square would not repeat the tower the
cover was carrying. With the cover reduced to type, nothing repeats, and a mark
whose only remaining home was a 16px favicon is drift rather than a system.

The tower geometry is imported from build_logo rather than restated, so the A in
the logo and the A in the wordmark can never drift apart.

Run: python3 build_avatar.py
"""

import re
from pathlib import Path

import build_logo

INK = "#202124"
TEAL_DEEP = "#26595c"

SIZE = 400.0

# Lockup: tower, name, rule.
TOWER_H = 0.545          # of the square
TOWER_TOP = 0.135
NAME_SIZE = 0.155
NAME_BASELINE = 0.885
RULE_W, RULE_Y, RULE_H = 0.28, 0.925, 0.014

# Favicon: the tower alone, set larger than it sits in the lockup because at
# 16px a faithful weight reads as a grey smudge.
FAVICON_TOWER_H = 0.86


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def tower_parts():
    """The letter A's own geometry, lifted out of its wrapper svg."""
    svg = build_logo.build_letter_a(cap=100.0)
    inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", svg, flags=re.S).strip()
    box = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    return inner, float(box.group(1)), float(box.group(2))


def placed_tower(height_frac, top_frac):
    inner, vw, vh = tower_parts()
    h = SIZE * height_frac
    scale = h / vh
    x = (SIZE - vw * scale) / 2
    y = SIZE * top_frac
    return [
        f'  <g transform="translate({fmt(x)},{fmt(y)}) scale({fmt(scale)})">',
        "  " + inner.replace("\n", "\n  "),
        "  </g>",
    ]


def build_lockup():
    label = "AIDaR, with the Eiffel Tower as its A"
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(SIZE)} '
            f'{fmt(SIZE)}" role="img" aria-label="{label}">',
            f'  <rect width="{fmt(SIZE)}" height="{fmt(SIZE)}" fill="#ffffff"/>',
            *placed_tower(TOWER_H, TOWER_TOP),
            # The a is italic, exactly as in the wordmark.
            f'  <text x="{fmt(SIZE / 2)}" y="{fmt(SIZE * NAME_BASELINE)}" '
            'text-anchor="middle" font-family="Georgia, ui-serif, serif" '
            f'font-size="{fmt(SIZE * NAME_SIZE)}" fill="{INK}" '
            'letter-spacing="-0.5">AID<tspan font-style="italic">a</tspan>R</text>',
            f'  <rect x="{fmt(SIZE * (1 - RULE_W) / 2)}" y="{fmt(SIZE * RULE_Y)}" '
            f'width="{fmt(SIZE * RULE_W)}" height="{fmt(SIZE * RULE_H)}" '
            f'fill="{TEAL_DEEP}"/>',
            "</svg>",
        ]
    ) + "\n"


def build_favicon():
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(SIZE)} '
            f'{fmt(SIZE)}" role="img" aria-label="AIDaR">',
            f'  <rect width="{fmt(SIZE)}" height="{fmt(SIZE)}" fill="#ffffff"/>',
            *placed_tower(FAVICON_TOWER_H, (1 - FAVICON_TOWER_H) / 2),
            "</svg>",
        ]
    ) + "\n"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    repo_root = here.parents[2]
    (here / "aidar-avatar.svg").write_text(build_lockup())
    (repo_root / "favicon.svg").write_text(build_favicon())
    print(f"wrote {here / 'aidar-avatar.svg'}  (lockup)")
    print(f"wrote {repo_root / 'favicon.svg'}  (tower alone)")
