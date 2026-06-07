#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# render.sh — turn a live-show-prep HTML file into a print-ready PDF.
#
# Uses headless Google Chrome so the embedded Google Fonts (Newsreader,
# Fraunces, IBM Plex Sans) and the CSS @page page-numbers render exactly.
#
# Usage:
#   ./render.sh "path/to/Research Brief.html"            # -> same name .pdf
#   ./render.sh "path/to/file.html" "path/to/out.pdf"    # explicit output
#
# Notes:
#   * Needs internet on first render (fonts are fetched from Google Fonts and
#     then embedded into the PDF, so the PDF itself is fully portable).
#   * Each call uses a throwaway Chrome profile, so you can render several
#     files back-to-back without the "profile in use" lock.
# ---------------------------------------------------------------------------
set -euo pipefail

HTML="${1:?usage: render.sh <input.html> [output.pdf]}"
OUT="${2:-${HTML%.html}.pdf}"

# Find a Chromium-family browser.
CHROME=""
for c in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  "$(command -v google-chrome 2>/dev/null || true)" \
  "$(command -v chromium 2>/dev/null || true)"; do
  if [ -n "$c" ] && [ -x "$c" ]; then CHROME="$c"; break; fi
done
if [ -z "$CHROME" ]; then
  echo "render.sh: no Chrome/Chromium/Edge found. Install Google Chrome and retry." >&2
  exit 1
fi

# Absolute file:// URL (Chrome needs an absolute path).
DIR="$(cd "$(dirname "$HTML")" && pwd)"
ABS="$DIR/$(basename "$HTML")"
PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE"' EXIT

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=22000 \
  --user-data-dir="$PROFILE" \
  --print-to-pdf="$OUT" \
  "file://$ABS" >/dev/null 2>&1

if [ -f "$OUT" ]; then
  PAGES="$(mdls -name kMDItemNumberOfPages -raw "$OUT" 2>/dev/null || echo '?')"
  echo "render.sh: wrote \"$OUT\" (${PAGES} pages)"
else
  echo "render.sh: render failed — no output produced." >&2
  exit 1
fi
