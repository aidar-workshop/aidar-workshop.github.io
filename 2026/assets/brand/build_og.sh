#!/usr/bin/env bash
# Render the social card to aidar-og.png at exactly 1200x630.
#
# og-card.html fetches aidar-mark.svg, so it has to be served over HTTP rather
# than opened as a file:// URL — a file:// fetch is blocked by CORS and the mark
# would silently render empty.
#
# Usage: ./build_og.sh
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$here/../../.." && pwd)"
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
port=8791
out="$here/aidar-og.png"

[ -x "$chrome" ] || { echo "Chrome not found at: $chrome" >&2; exit 1; }

# Served from the repo root so /favicon.svg resolves exactly as it will in production.
python3 -m http.server "$port" --bind 127.0.0.1 --directory "$repo_root" >/dev/null 2>&1 &
server=$!
trap 'kill "$server" 2>/dev/null || true' EXIT
sleep 1.5

lineup="$here/aidar-og-lineup.png"

render() {  # render <output> <query>
  "$chrome" \
    --headless \
    --disable-gpu \
    --hide-scrollbars \
    --force-device-scale-factor=2 \
    --window-size=1200,630 \
    --screenshot="$1" \
    --virtual-time-budget=5000 \
    "http://127.0.0.1:$port/2026/assets/brand/og-card.html$2" >/dev/null 2>&1
  [ -s "$1" ] || { echo "render produced no file: $1" >&2; exit 1; }
  echo "wrote $1"
}

render "$out" ""                        # clean
render "$lineup" "?variant=lineup"      # carrying the programme

# iOS home-screen icon: 180x180, rendered straight from the favicon.
touch_icon="$repo_root/apple-touch-icon.png"
"$chrome" \
  --headless \
  --disable-gpu \
  --hide-scrollbars \
  --force-device-scale-factor=1 \
  --window-size=180,180 \
  --screenshot="$touch_icon" \
  --virtual-time-budget=2000 \
  "http://127.0.0.1:$port/favicon.svg" >/dev/null 2>&1

[ -s "$touch_icon" ] || { echo "apple-touch-icon render produced no file" >&2; exit 1; }
echo "wrote $touch_icon"

# LinkedIn Page cover: 4200x700 is both their minimum and their recommended
# size, and they ask for "a high-resolution JPEG instead of a PNG", capped at
# 3MB. Rendered at 2100x350 with a 2x scale to land exactly on it.
banner_png="$here/.banner.tmp.png"
banner="$here/aidar-linkedin-banner.jpg"
"$chrome" \
  --headless \
  --disable-gpu \
  --hide-scrollbars \
  --force-device-scale-factor=2 \
  --window-size=2100,350 \
  --screenshot="$banner_png" \
  --virtual-time-budget=4000 \
  "http://127.0.0.1:$port/2026/assets/brand/banner.html" >/dev/null 2>&1

[ -s "$banner_png" ] || { echo "banner render produced no file" >&2; exit 1; }
sips -s format jpeg -s formatOptions 88 "$banner_png" --out "$banner" >/dev/null 2>&1
rm -f "$banner_png"

banner_bytes=$(stat -f%z "$banner")
if [ "$banner_bytes" -gt 3000000 ]; then
  echo "banner is ${banner_bytes}b, over LinkedIn's 3MB cap" >&2
  exit 1
fi
echo "wrote $banner ($((banner_bytes / 1024))KB)"

# LinkedIn Page logo: 400x400 recommended, 268x268 minimum.
avatar="$here/aidar-avatar.png"
"$chrome" \
  --headless \
  --disable-gpu \
  --hide-scrollbars \
  --force-device-scale-factor=1 \
  --window-size=400,400 \
  --screenshot="$avatar" \
  --virtual-time-budget=2500 \
  "http://127.0.0.1:$port/2026/assets/brand/avatar.html" >/dev/null 2>&1

[ -s "$avatar" ] || { echo "avatar render produced no file" >&2; exit 1; }

# Assert on the exported pixels, not on the SVG. The first export looked right
# in every HTML preview and was clipped off the right edge in the actual file.
report=$("$chrome" --headless --disable-gpu --virtual-time-budget=4000 --dump-dom \
  "http://127.0.0.1:$port/2026/assets/brand/check-avatar.html" 2>/dev/null \
  | grep -o '<title>.*</title>' | sed 's/<[^>]*>//g')
case "$report" in
  *'"clipped":[]'*) echo "wrote $avatar  $report" ;;
  *) echo "avatar is clipped or unreadable: $report" >&2; exit 1 ;;
esac

# Stamp the default card's content hash into og:image / twitter:image.
#
# Scrapers (LinkedIn, X, Slack, Facebook) cache by image URL and will happily
# serve bytes they fetched weeks ago. The filename stays put across rebuilds, so
# without this the card changes and every feed keeps showing the old one.
#
# Change these two lines together to switch which card a shared link picks up.
default_card="$lineup"
default_name="aidar-og-lineup.png"

ver="$(shasum -a 256 "$default_card" | cut -c1-8)"
base="https://aidar-workshop.github.io/2026/assets/brand/$default_name"
for f in "$repo_root/2026/index.html" "$repo_root/index.html"; do
  python3 - "$f" "$base" "$ver" <<'PY'
import re, sys
path, base, ver = sys.argv[1:4]
with open(path) as fh:
    html = fh.read()
# Rewrite whichever card is currently referenced, so switching the default
# does not need a hand edit of the meta tags.
html = re.sub(
    r'https://aidar-workshop\.github\.io/2026/assets/brand/aidar-og(?:-lineup)?\.png(?:\?v=[0-9a-f]+)?',
    f'{base}?v={ver}',
    html,
)
with open(path, 'w') as fh:
    fh.write(html)
PY
done
echo "stamped og:image ?v=$ver"
