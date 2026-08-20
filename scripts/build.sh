#!/usr/bin/env bash
# Build the CV from the single source of truth (CV_FILE) into rendercv_output/,
# then assemble a static site/ folder for GitHub Pages.
set -euo pipefail

cd "$(dirname "$0")/.."

CV_FILE="${CV_FILE:-Soheil_Koohi_CV.yaml}"
RENDERCV_VERSION="${RENDERCV_VERSION:-2.8}"
OUT_DIR="rendercv_output"
SITE_DIR="site"

if command -v rendercv >/dev/null 2>&1; then
  RENDERCV=(rendercv)
elif command -v uvx >/dev/null 2>&1; then
  RENDERCV=(uvx --python 3.12 --from "rendercv[full]==${RENDERCV_VERSION}" rendercv)
else
  echo "error: neither 'rendercv' nor 'uvx' found on PATH." >&2
  echo "install one of:" >&2
  echo "  uv tool install --python 3.12 'rendercv[full]==${RENDERCV_VERSION}'" >&2
  echo "  pipx install 'rendercv[full]==${RENDERCV_VERSION}'" >&2
  exit 1
fi

echo ">> rendering ${CV_FILE}"
"${RENDERCV[@]}" render "${CV_FILE}"

BASENAME="$(basename "${CV_FILE%.*}")"
PDF="${OUT_DIR}/${BASENAME}.pdf"
HTML="${OUT_DIR}/${BASENAME}.html"

[ -f "$PDF" ] || { echo "error: expected ${PDF} but it was not produced" >&2; exit 1; }

echo ">> assembling ${SITE_DIR}/"
rm -rf "$SITE_DIR"
mkdir -p "$SITE_DIR"
cp "$PDF" "$SITE_DIR/"
cp "$HTML" "$SITE_DIR/index.html"
cp "${OUT_DIR}/${BASENAME}.md" "$SITE_DIR/" 2>/dev/null || true
cp "${OUT_DIR}/${BASENAME}"_*.png "$SITE_DIR/" 2>/dev/null || true

# Prepend a small download bar to the HTML version.
python3 - "$SITE_DIR/index.html" "${BASENAME}.pdf" <<'PY'
import sys, pathlib
page, pdf = pathlib.Path(sys.argv[1]), sys.argv[2]
html = page.read_text(encoding="utf-8")
bar = (
    '<div style="font-family:system-ui,-apple-system,sans-serif;text-align:center;'
    'padding:12px;border-bottom:1px solid #ddd;margin-bottom:24px">'
    f'<a href="{pdf}" style="color:#0b5cad;text-decoration:none;font-weight:600">'
    'Download PDF</a></div>'
)
marker = "<body>"
if marker in html and "Download PDF" not in html:
    html = html.replace(marker, marker + bar, 1)
    page.write_text(html, encoding="utf-8")
PY

echo
echo "done:"
echo "  PDF   ${PDF}"
echo "  site  ${SITE_DIR}/index.html"
