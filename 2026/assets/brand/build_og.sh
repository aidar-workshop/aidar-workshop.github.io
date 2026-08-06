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

"$chrome" \
  --headless \
  --disable-gpu \
  --hide-scrollbars \
  --force-device-scale-factor=2 \
  --window-size=1200,630 \
  --screenshot="$out" \
  --virtual-time-budget=4000 \
  "http://127.0.0.1:$port/2026/assets/brand/og-card.html" >/dev/null 2>&1

[ -s "$out" ] || { echo "render produced no file" >&2; exit 1; }
echo "wrote $out"

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
