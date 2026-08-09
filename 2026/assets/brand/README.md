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

## The square forms

The cover carries type only, so the square is where the identity lives — which
means it is the wordmark itself rather than a companion to it. A stranger
landing on the Page needs to know whose it is.

- `aidar-avatar.svg` / `.png` — the lockup: tower, name, rule. **48px and up**,
  for the LinkedIn Page logo and the iOS touch icon
- `/favicon.svg` — the tower alone, set larger than it sits in the lockup.
  **32px and under**; the name is unreadable at 16px and the browser tab prints
  the page title beside it anyway
- built by `build_avatar.py`, which imports the tower's geometry from
  `build_logo.py` so the A in the logo and the A in the wordmark cannot drift

LinkedIn draws a Page logo at roughly 150px on desktop, not the 56px a feed
suggests, which is why the name fits there at all.

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

## The cover

Type only: the title, a rule, and where and when. No mark — the logo is drawn
over the cover at ~150px and carries the identity, so repeating it here said the
same thing twice and cost the type its size.

Everything sits clear of the left fifth of the cover, which the logo covers
entirely. A left-hand flank was tried and vanished behind it.

- `aidar-linkedin-banner.jpg`, built from `banner.html` by `build_og.sh`

## Retired

- **AI monogram** — the tower-A plus a drawn I, formerly the favicon. A third
  mark doing the companion mark's job with a different idea. The reduced graph
  reads better at 16px besides.
- **Radar plate** — a circular dial on the twelve avenues of the Place de
  l'Étoile. It punned on the acronym (AIDaR / RADAR) and depicted nothing about
  data.
- **Knowledge graph** — measurements resolving into a lattice. A good answer to
  a question that stopped existing: it was drawn so the square would not repeat
  the tower the cover was carrying. Once the cover became type only, nothing
  repeated, and a mark whose one remaining home was a 16px favicon is drift.
- **Croissant and escargot graphs** — a node layout shaped as a crescent, and
  one on the clockwise spiral of the twenty arrondissements. The escargot is a
  real fact about Paris and drew well; the cover reads better with nothing on
  it.

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
