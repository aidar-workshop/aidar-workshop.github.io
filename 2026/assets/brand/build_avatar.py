"""Emit the AIDaR avatar: loose measurements taken up into a knowledge graph.

Four things had to be true at once, and each earlier attempt failed one of them.

  SCIENCE   the loose points are measurements
  DATA      the nodes are those measurements, kept
  READY     the transformation, left to right — the dashed edge is a point in
            the act of being taken up, which is what readiness actually is
  AI        the graph

The AI reading is the hard one. Nothing depicts AI on its own; a fitted line
reads as regression, and the only two symbols that carry it are the neural-net
node graph and the LLM sparkle. The graph is worth using here because it is not
borrowed — the site names "tables, graphs, or knowledge networks" and
"relational and graph-structured data" as the workshop's own subject. Drawn
sparse and irregular it reads as a knowledge graph rather than a layered
perceptron.

Ink on white, because the banner is ink on white: its only teal is a 104px rule
and one line of small caps, so a teal-dominant tile sits beside it as a
different brand.

Node positions are written out rather than generated. A scatter that has to
look deliberately irregular is easier to place by hand than to tune a hash into.

Run: python3 build_avatar.py
"""

from pathlib import Path

INK = "#202124"
MUTED = "#9aa0a6"

SIZE = 400.0
NODE_R = 16.0
EDGE_W = 6.5

# The hand-placed cloud sits low in the square; nudged so the ink is optically
# centred. check-avatar.html reports the margins the build actually produced.
Y_NUDGE = -0.025

# Normalised to the square. Kept asymmetric on purpose: a regular graph reads as
# a diagram of a neural network, which is the thing being avoided.
NODES = {
    "a": (0.50, 0.22),
    "b": (0.68, 0.42),
    "c": (0.46, 0.55),
    "d": (0.80, 0.68),
    "e": (0.86, 0.32),
    "f": (0.60, 0.82),
}
EDGES = (("a", "b"), ("b", "c"), ("b", "e"), ("b", "d"), ("c", "f"), ("d", "f"))

# Measurements not yet part of the graph.
LOOSE = ((0.15, 0.30), (0.12, 0.64), (0.25, 0.84), (0.22, 0.46))

# The one being taken up: a dashed edge, caught mid-formation.
JOINING = (((0.25, 0.84), "c"),)


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def px(pt):
    return pt[0] * SIZE, (pt[1] + Y_NUDGE) * SIZE


def build():
    label = (
        "AIDaR: loose measurements on the left taken up into a structured "
        "knowledge graph on the right"
    )
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(SIZE)} '
        f'{fmt(SIZE)}" role="img" aria-label="{label}">',
        f'  <rect width="{fmt(SIZE)}" height="{fmt(SIZE)}" fill="#ffffff"/>',
    ]

    for a, b in EDGES:
        x1, y1 = px(NODES[a])
        x2, y2 = px(NODES[b])
        out.append(
            f'  <line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" '
            f'stroke="{INK}" stroke-width="{fmt(EDGE_W)}" stroke-linecap="round"/>'
        )

    for loose_pt, target in JOINING:
        x1, y1 = px(loose_pt)
        x2, y2 = px(NODES[target])
        dash = EDGE_W * 2.4
        out.append(
            f'  <line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" '
            f'stroke="{MUTED}" stroke-width="{fmt(EDGE_W)}" stroke-linecap="round" '
            f'stroke-dasharray="{fmt(dash)} {fmt(dash)}"/>'
        )

    for pt in LOOSE:
        x, y = px(pt)
        out.append(
            f'  <circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(NODE_R * 0.72)}" '
            f'fill="{MUTED}"/>'
        )

    for pt in NODES.values():
        x, y = px(pt)
        out.append(
            f'  <circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(NODE_R)}" fill="{INK}"/>'
        )

    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    (here / "aidar-avatar.svg").write_text(build())
    print(f"wrote {here / 'aidar-avatar.svg'}")
