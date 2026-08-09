# AIDaR identity

Two marks. Everything else is one of them at a different size.

## The wordmark

`AIDaR` set in the site's serif, with the Eiffel Tower drawn as the capital A.
The tower is already an A — splayed legs, a pointed apex, a platform where the
crossbar goes — so the letter beside it is the I the word already had, and
**AI** reads straight out of the Paris skyline.

It is drawn as the open lattice the tower actually is rather than a solid
silhouette, which is both what a capital A needs and what the tower looks like.

Use it wherever the name fits: the page hero, the share cards, the LinkedIn
cover.

- `aidar-a.svg` — the A alone, to set beside live type
- built by `build_logo.py`

## The companion mark

A knowledge graph: loose measurements at the left taken up into a structured
graph at the right.

- **SCIENCE** the loose points are measurements
- **DATA** the nodes are those measurements, kept
- **READY** the transformation — the dashed edge is a point in the act of being
  taken up, which is what readiness is
- **AI** the graph

The graph is not borrowed from the neural-network cliché: the workshop's own
call names "tables, graphs, or knowledge networks" and "relational and
graph-structured data" as its subject. Drawn sparse and asymmetric it reads as a
knowledge graph, not a layered perceptron.

Use it wherever there is only a square and no room for the name.

- `aidar-avatar.svg` / `.png` — full form, **48px and up**, with the name set
  beneath it
- `/favicon.svg` — reduced form, **32px and under**, graph only
- built by `build_avatar.py`

### Why two forms

A tab icon is drawn at 16px. At that size the full graph closes up into a
smudge: the loose points vanish and the edges merge. The reduced form keeps the
shape and drops what cannot survive — the loose points, the dashed edge, and two
nodes. Same mark, not a different one.

### Why the full form carries the name

LinkedIn draws a Page logo at roughly 150px on desktop, not the 56px a feed
suggests, so there is room for the name and a mark that names itself is more use
to a stranger than one that does not. The `a` is italic, exactly as in the
wordmark. The name is dropped from the reduced form because it is unreadable at
16px and the browser tab already shows the page title beside it.

Note that the name in `aidar-avatar.svg` is live text in Georgia. The exported
PNG bakes it, so the PNG is what should be uploaded anywhere the viewer's fonts
are unknown.

## Colour

Ink on white. The teal is an accent and never a field: across the whole system
it appears only on a rule, a set of small caps, and the theme colour. A
teal-dominant tile sits beside the banner as a different brand — this was tried
and rejected.

| | |
| --- | --- |
| `--ink` | `#202124` |
| `--muted` | `#5f6368` |
| `--line` | `#d8dadd` |
| `--wash` | `#f7f8f8` |
| `--accent` | `#2f6f73` |
| `--accent-deep` | `#26595c` |

## Retired

- **AI monogram** — the tower-A plus a drawn I, formerly the favicon. A third
  mark doing the companion mark's job with a different idea. The reduced graph
  reads better at 16px besides.
- **Radar plate** — a circular dial on the twelve avenues of the Place de
  l'Étoile. It punned on the acronym (AIDaR / RADAR) and depicted nothing about
  data.

## Building

```sh
./build_og.sh      # share cards, LinkedIn cover, avatar, touch icon
python3 build_logo.py     # the wordmark's A
python3 build_avatar.py   # the companion mark, both forms
```

`build_og.sh` stamps the share card's content hash into `og:image` so scrapers
cannot serve a stale card, fails if the LinkedIn cover exceeds their 3MB cap,
and asserts on the avatar's exported pixels — an earlier export looked correct
in every preview and shipped clipped, because the SVG was checked and the PNG
was not.

## Sizes these were built to

From LinkedIn's own image-specifications article, not the numbers blogs repeat:

| | |
| --- | --- |
| Page cover | 4200 × 700, JPEG preferred, 3MB cap |
| Page logo, as drawn | ~150px on desktop, ~56px in feeds |

The logo is drawn **over** the cover, at the left. Anything placed in the left
fifth of a cover is invisible on desktop — a left-hand flank was tried and
disappeared entirely behind it.
| Page logo | 400 × 400 recommended, 268 × 268 minimum |
| Share card | 1200 × 630, rendered at 2× |
